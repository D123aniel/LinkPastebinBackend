import os
import dotenv

dotenv.load_dotenv(f"{os.path.dirname(__file__)}/.env", verbose=True)


def getenv(variable: str) -> str:
    value = os.getenv(variable)
    if value is not None:
        return value
    raise ValueError(f"Environment variable '{variable}' not set.")
