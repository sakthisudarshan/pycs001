"""
FastAPI application entry point — mirrors Program.cs
Wires REST API routes and starts the gRPC server in a background thread.
"""
import threading

from fastapi import FastAPI

from .routes import router
from .grpc_server import serve

app = FastAPI(
    title="CE Platform — Python Service A",
    description="FastAPI + gRPC + MongoDB service (Python 3.11+)",
    version="1.0.0",
)

app.include_router(router)


@app.on_event("startup")
def startup_grpc() -> None:
    """Launch gRPC server on startup in a daemon thread."""
    t = threading.Thread(target=serve, daemon=True)
    t.start()


if __name__ == "__main__":  # pragma: no cover
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)
