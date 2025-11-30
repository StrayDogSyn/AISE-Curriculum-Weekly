from prometheus_client import Counter, Histogram

request_counter = Counter(
    "request_count",
    "Total number of requests",
    ["endpoint", "method", "status"],
)

request_latency = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["endpoint", "method"],
)