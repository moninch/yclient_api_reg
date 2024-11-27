import logging
import asyncio

from bson import ObjectId
from typing import Iterable

from datetime import datetime
import motor
from pydantic import BaseModel, Field
from pymongo.database import Database
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_mongo import PydanticObjectId


class MongoObject(BaseModel):
    _id: PydanticObjectId

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._id = kwargs.get("_id")

    def model_dump(self, include_id: bool = False, **kwargs):
        dump = super().model_dump(**kwargs)
        if include_id:
            dump["_id"] = str(self._id)
        return dump


class Company(MongoObject):
    branch_id: int
    title: str
    email: str
    city: str


class MongoDB:
    client: AsyncIOMotorClient  # type: ignore
    db: Database

    @classmethod
    def setup(cls, mongodb_url: str, mongodb_db: str) -> None:
        cls.client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
        cls.db = cls.client.get_database(mongodb_db)
        try:
            cls.client.admin.command("ping")
            logging.info("Connected to MongoDB")
        except Exception as e:
            logging.error(f"Exception while connecting to MongoDB: {e}")

    @classmethod
    def get_database(cls) -> Database:
        if not hasattr(cls, "db"):
            raise RuntimeError("Database is not initialized. Call setup() first.")
        return cls.db

    @classmethod
    async def update_field(
        cls, collection: str, _id: ObjectId, path: Iterable[str], value: any
    ):
        """
        {a: {b: True} }\n
        path to `b`: ('a', 'b')
        """
        path_str = ".".join(path)
        collection = MongoDB.db.get_collection(collection)
        await collection.update_one(
            filter={"_id": _id}, update={"$set": {path_str: value}}
        )
