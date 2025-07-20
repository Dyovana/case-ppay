from pathlib import Path

RESOURCES_DIR = Path(__file__).parent


def get_resource_path(filename: str) -> Path:
    """
    Returns the full path to a file inside the resources folder.
    """
    return RESOURCES_DIR / filename


MODEL_PATH = get_resource_path("Iris.pkl")
