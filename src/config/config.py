
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Central configuration class
    Reads all required environment variables
    """

    DB_FOLDER = os.getenv("DB_FOLDER")
    DB_NAME = os.getenv("DB_NAME")
    BRONZE_BUCKET = os.getenv("BRONZE_BUCKET")
    API_BASE_URL = os.getenv("API_BASE_URL")
    WATERMARK_FILE = os.getenv("WATERMARK_FILE")

    @staticmethod
    def validate():
        """
        Validate that all required ENV variables are present
        """
        missing = []

        if not Config.DB_FOLDER:
            missing.append("DB_FOLDER")

        if not Config.DB_NAME:
            missing.append("DB_NAME")

        if not Config.BRONZE_BUCKET:
            missing.append("BRONZE_BUCKET")

        if not Config.API_BASE_URL:
            missing.append("API_BASE_URL")

        if missing:
            raise ValueError(f"❌ Missing ENV variables: {', '.join(missing)}")


# Run validation immediately
Config.validate()
