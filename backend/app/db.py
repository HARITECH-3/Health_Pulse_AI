import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

# We check if MONGODB_URI exists in .env
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    print("WARNING: MONGODB_URI is missing from your .env file!")
    client = MongoClient("mongodb://localhost:27017/")
else:
    # Use fast timeouts so requests fail fast if IP is not whitelisted
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)

db = client.pulse_health_db

def get_db():
    yield db
