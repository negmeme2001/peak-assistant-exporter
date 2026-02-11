# Peak Assistant Exporter ⛰️

A Prometheus exporter for the Peak Assistant service, extracting usage metrics from MongoDB logs.

## Features

- **Real-time Metrics**: Exposes API usage, latency, cost, and token consumption.
- **Efficient**: Uses a background thread to cache aggregations every 15s (non-blocking scrapes).
- **Production Ready**: Robust error handling, logging, and Docker support.
- **Grafana Dashboard**: Includes a pre-built JSON dashboard for visualization.

## 🛠️ Prerequisites

- **Python 3.10+** (managed via `uv` recommended)
- **MongoDB** instance with `peak` database.

## ⚙️ Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd peak-assistant-exporter
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   
3. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   MONGODB_URI=DB_URI
   MONGODB_DATABASE=DB_NAME
   ```

### Local Development
Run the exporter directly using `uv`:
```bash
uv run python src/main.py
```
The exporter will start on `http://0.0.0.0:8000/metrics`.

### Docker
Build and run the container:
```bash
docker build -t peak-assistant-exporter .
docker run -d -p 8000:8000 --env-file .env peak-assistant-exporter
```

## 📊 Metrics Overview

| Metric | Type | Description |
|--------|------|-------------|
| `peak_assistant_requests_total` | Gauge | Total requests (success/error) |
| `peak_assistant_duration_seconds` | Gauge | Avg response latency (sum/count) |
| `peak_assistant_cost_usd_total` | Gauge | Total estimated cost (by model) |
| `peak_assistant_tokens_total` | Gauge | Token usage (prompt/completion) |
| `peak_assistant_tool_calls_total` | Gauge | Tool usage counts |

## Grafana Dashboard

Import the dashboard JSON located at `grafana/dashboards/peak-assistant.json` into your Grafana instance to visualize these metrics instantly.
