from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_pymongo import pymongo
from config import Config as SETTING

# Get Data from Database
client = pymongo.MongoClient(SETTING.MONGO_LINK)
GMusic = client["GMusic"]

Users = GMusic["users"]
Playlists = GMusic["playlists"]
Songs = GMusic["songs"]
Modifications = GMusic["modifications"]
