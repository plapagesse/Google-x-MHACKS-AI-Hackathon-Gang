from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

load_dotenv()
database_url = os.getenv('mongodbURI')
client = MongoClient(database_url, server_api=ServerApi('1'))