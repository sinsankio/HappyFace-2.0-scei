from typing import Any

import pymongo
from dotenv import dotenv_values
from pymongo import MongoClient

MONGO_CLIENT: MongoClient | None = None
MONGO_DB: Any | None = None


def load_db_configs(config_file_path: str = "../mongodb.env"):
    return dotenv_values(config_file_path)


def get_db_connected(db_uri: str, db: str):
    global MONGO_CLIENT, MONGO_DB

    if MONGO_CLIENT is None or MONGO_DB is None:
        MONGO_CLIENT = MongoClient(db_uri)
        MONGO_DB = MONGO_CLIENT[db]


def get_db_disconnected():
    global MONGO_CLIENT

    if MONGO_CLIENT is not None:
        MONGO_CLIENT.close()


def find_one(condition: dict, project_vals: dict, collection: str = "entries") -> dict:
    if MONGO_DB is not None:
        return MONGO_DB[collection].find_one(condition, projection=project_vals)


def find_all(condition: dict, project_vals: dict, sort: list = None, collection: str = "entries") -> Any:
    if MONGO_DB is not None:
        if sort is None:
            sort = [("_id", pymongo.ASCENDING)]
        records = (
            MONGO_DB[collection]
            .find(condition, projection=project_vals)
            .sort(sort)
        )
        return [record for record in records]


def insert_one(model: dict, collection: str = "entries") -> Any:
    if MONGO_DB is not None:
        return MONGO_DB[collection].insert_one(model)


def update_one(condition: dict, new_values: dict, collection: str = "entries") -> Any:
    if MONGO_DB is not None:
        return MONGO_DB[collection].update_one(condition, new_values)


def delete_many(condition: dict, collection: str = "entries") -> Any:
    if MONGO_DB is not None:
        return MONGO_DB[collection].delete_many(condition)
