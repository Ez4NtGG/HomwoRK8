import os
from pathlib import Path

from dotenv import load_dotenv
from mongoengine import connect, OperationError

MongoDB_USER = os.getenv('MongoDB_USER')
if not MongoDB_USER:
    env_path = Path(__file__).parent.parent.parent.parent.joinpath(".env")
    if env_path.is_file:
        # print(env_path)
        load_dotenv(env_path)

MongoDB_USER = os.getenv('MongoDB_USER')
MongoDB_PASSWORD = os.getenv('MongoDB_PASSWORD')
MongoDB_HOST = os.getenv('MongoDB_HOST')
MongoDB_NAME = os.getenv('MongoDB_NAME')

#client = None
connect_state = False
def connect_db():
    global connect_state
    if MongoDB_USER:
        URI = f"""mongodb+srv://{MongoDB_USER}:{MongoDB_PASSWORD}@{MongoDB_HOST}/{MongoDB_NAME}?retryWrites=true&w=majority"""
        try:
            connect(host=URI, ssl=True)
        except OperationError:
            print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        except Exception as e:
            print("error:",e)
        else:
            print("connect_db - ok")
            connect_state = True
    else:
        print("not defined MongoDB_USER from enviroment. Database not conected")
    return connect_state

    # print(f"{URI=}")
