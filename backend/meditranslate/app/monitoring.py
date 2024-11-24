
from typing import Callable
from fastapi import FastAPI
from prometheus_client import Counter, Info
from prometheus_fastapi_instrumentator import Instrumentator,metrics,middleware
from prometheus_client import CollectorRegistry, Counter



def setup_monitoring(app: FastAPI):
    instrumentator = Instrumentator(
        body_handlers=[r".*"],
    )
    instrumentator.add(
        metrics.request_size(
            should_include_handler=True,
            should_include_method=False,
            should_include_status=True,
            metric_namespace="a",
            metric_subsystem="b",
        ),
        metrics.requests(),
        metrics.combined_size(),
        metrics.response_size(
            should_include_handler=True,
            should_include_method=False,
            should_include_status=True,
            metric_namespace="namespace",
            metric_subsystem="subsystem",
        ),
        metrics.latency(),
        metrics.default(),
    )
    instrumentator.instrument(app)
    instrumentator.expose(app)



