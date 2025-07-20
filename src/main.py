import pickle
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.logging import setup_logger
from src.controllers.default import default_router
from src.controllers.handlers import register_exception_handlers
from src.resources.resources_config import MODEL_PATH

logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles the application's startup and shutdown events.
    """
    # --- Startup event ---
    logger.info("Application starting: Loading Iris.pkl model...")
    try:
        with open(MODEL_PATH, "rb") as file:
            app.state.ml_model = pickle.load(file)
        logger.info("Iris.pkl model loaded successfully!")

    except FileNotFoundError:
        logger.critical(f"CRITICAL ERROR: Model file not found at {MODEL_PATH}")
        raise

    yield
    app.state.ml_model = None


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)
app.include_router(default_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
