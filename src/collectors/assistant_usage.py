from metrics import (
    requests_total,
    tokens_total,
    cost_usd_total,
    tool_calls_total,
    duration_seconds_sum,
    duration_seconds_count,
    prompt_tokens_sum,
    prompt_tokens_count,
)


def collect(collection):
    """Run MongoDB aggregations and update all Prometheus gauges."""

    # 1. Requests — group by status only (requestType doesn't exist in DB)
    for doc in collection.aggregate([
        {"$match": {"status": {"$ne": None}}},
        {"$group": {"_id": {"status": "$status"}, "count": {"$sum": 1}}},
    ]):
        requests_total.labels(
            status=doc["_id"].get("status", "unknown"),
        ).set(doc["count"])

    # 2. Tokens — group by model, sum prompt and completion
    for doc in collection.aggregate([
        {"$match": {"modelUsed": {"$ne": None}}},
        {"$group": {
            "_id": "$modelUsed",
            "prompt": {"$sum": "$promptTokens"},
            "completion": {"$sum": "$completionTokens"},
        }},
    ]):
        model = doc["_id"] or "unknown"
        tokens_total.labels(model=model, token_type="prompt").set(doc["prompt"])
        tokens_total.labels(model=model, token_type="completion").set(doc["completion"])

    # 3. Cost — group by model, sum estimatedCostUsd
    for doc in collection.aggregate([
        {"$match": {"modelUsed": {"$ne": None}}},
        {"$group": {"_id": "$modelUsed", "total": {"$sum": "$estimatedCostUsd"}}},
    ]):
        cost_usd_total.labels(model=doc["_id"] or "unknown").set(doc["total"])

    # 4. Tool Calls — unwind toolsUsed, group by tool + status
    for doc in collection.aggregate([
        {"$match": {"toolsUsed": {"$exists": True, "$ne": []}}},
        {"$unwind": "$toolsUsed"},
        {"$group": {"_id": {"tool": "$toolsUsed", "status": "$status"}, "count": {"$sum": 1}}},
    ]):
        tool_calls_total.labels(
            tool_name=doc["_id"].get("tool", "unknown"),
            status=doc["_id"].get("status", "unknown"),
        ).set(doc["count"])

    # 5. Duration — sum durationMs + count (no requestType in DB)
    for doc in collection.aggregate([
        {"$match": {"durationMs": {"$ne": None}}},
        {"$group": {
            "_id": None,
            "totalDurationMs": {"$sum": "$durationMs"},
            "count": {"$sum": 1},
        }},
    ]):
        duration_seconds_sum.set(doc["totalDurationMs"] / 1000)
        duration_seconds_count.set(doc["count"])

    # 6. Prompt Tokens — group by model, sum promptTokens + count
    for doc in collection.aggregate([
        {"$match": {"modelUsed": {"$ne": None}}},
        {"$group": {
            "_id": "$modelUsed",
            "totalPromptTokens": {"$sum": "$promptTokens"},
            "count": {"$sum": 1},
        }},
    ]):
        model = doc["_id"] or "unknown"
        prompt_tokens_sum.labels(model=model).set(doc["totalPromptTokens"])
        prompt_tokens_count.labels(model=model).set(doc["count"])
