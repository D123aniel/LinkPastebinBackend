# test_connection.py
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
db_url = os.getenv("DATABASE_LINK")

if not db_url:
    print("❌ DATABASE_LINK not found in environment variables.")
else:
    try:
        # Create an engine to connect to the database
        engine = create_engine(db_url)

        # Try to establish a connection
        connection = engine.connect()

        print("✅ Connection Successful!")

        # Close the connection
        connection.close()

    except OperationalError as e:
        print("❌ Connection Failed.")
        print("-------------------------")
        print(f"Error: {e}")
        print("-------------------------")
        print("Troubleshooting Tips:")
        print("1. Is the Azure PostgreSQL server running?")
        print("2. Is your computer's IP address added to the Azure firewall rules?")
        print(
            "3. Are the credentials (user, password, host) in your .env file correct?"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
