import os
from pathlib import Path

from dotenv import load_dotenv
import pymongo

env_path = Path(__file__).parent.parent.parent.parent.joinpath(".env")
if env_path.is_file:
    print(env_path)
    load_dotenv(env_path)

MongoDB_USER = os.getenv('MongoDB_USER')
MongoDB_PASSWORD = os.getenv('MongoDB_PASSWORD')
MongoDB_HOST = os.getenv('MongoDB_HOST')

client = None

if MongoDB_USER:
    URI = f"mongodb+srv://{MongoDB_USER}:{MongoDB_PASSWORD}@{MongoDB_HOST}/?retryWrites=true&w=majority"
    try:
        client = pymongo.MongoClient(URI)
    except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    except pymongo.errors as e:
         print("pymongo error:",e)
else:
    print("not defined MongoDB_USER. Database not conected")

print(f"{URI=}")

if __name__ == "__main__":

    # client = pymongo.MongoClient(URI)

    print(f"{client=}")