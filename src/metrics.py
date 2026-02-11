from prometheus_client import Gauge

# 1. Total Requests
requests_total = Gauge(
    "peak_assistant_requests_total",
    "Total number of Peak Assistant requests",
    ["status"],
)

# 2. Token Usage
tokens_total = Gauge(
    "peak_assistant_tokens_total",
    "Total tokens consumed",
    ["model", "token_type"],
)

# 3. Cost
cost_usd_total = Gauge(
    "peak_assistant_cost_usd_total",
    "Total estimated cost in USD",
    ["model"],
)

# 4. Tool Calls
tool_calls_total = Gauge(
    "peak_assistant_tool_calls_total",
    "Total number of tool calls by tool name and status",
    ["tool_name", "status"],
)

# 5. Request Duration (sum + count for avg calculation)
duration_seconds_sum = Gauge(
    "peak_assistant_duration_seconds_sum",
    "Sum of request durations in seconds",
    [],
)

duration_seconds_count = Gauge(
    "peak_assistant_duration_seconds_count",
    "Count of requests for duration calculation",
    [],
)

# 6. Context Size / Prompt Tokens (sum + count for avg calculation)
prompt_tokens_sum = Gauge(
    "peak_assistant_prompt_tokens_sum",
    "Sum of prompt tokens",
    ["model"],
)

prompt_tokens_count = Gauge(
    "peak_assistant_prompt_tokens_count",
    "Count of requests for prompt token calculation",
    ["model"],
)
