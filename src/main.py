import time
import threading
from http.server import ThreadingHTTPServer
from prometheus_client.exposition import MetricsHandler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class SilentMetricsHandler(MetricsHandler):
    def log_message(self, format, *args):
        pass  

    def handle(self):
        try:
            super().handle()
        except BrokenPipeError:
            pass  
        except Exception as e:
            if "Broken pipe" not in str(e):
                logging.error(f"Error handling request: {e}", exc_info=True)


from db import get_client, get_collection
from collectors.assistant_usage import collect

_collection = None
_lock = threading.Lock()


def _background_collect(interval: int = 15):
    """Background thread that refreshes metrics periodically."""
    while True:
        try:
            with _lock:
                collect(_collection)
            logging.info("Metrics refreshed")
        except Exception as e:
            logging.error(f"Error in collector: {e}", exc_info=True)
        time.sleep(interval)


def main():
    global _collection

    client = get_client()
    _collection = get_collection(client)

    collect(_collection)

    thread = threading.Thread(target=_background_collect, args=(15,), daemon=True)
    thread.start()

    logging.info("Exporter running on http://0.0.0.0:8000/metrics")
    server = ThreadingHTTPServer(("0.0.0.0", 8000), SilentMetricsHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        client.close()
        server.server_close()


if __name__ == "__main__":
    main()
