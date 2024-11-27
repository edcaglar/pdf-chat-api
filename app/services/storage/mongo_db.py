from pymongo import MongoClient
from bson import ObjectId
from app.exceptions import DocumentNotFoundError, InvalidObjectIdError
from pymongo.errors import PyMongoError

class MongoDBManager:
    def __init__(self, uri: str, database_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[database_name]

    def add(self, collection: str, data: dict):
        try:
            collection_ref = self.db[collection]
            result = collection_ref.insert_one(data)
            return result.inserted_id
        except PyMongoError as e:
            raise Exception(f"MongoDB'ye belge eklenirken bir hata oluştu: {str(e)}")

    def get_by_object_id(self, collection: str, _id: str | ObjectId):

        if not ObjectId.is_valid(_id):
            raise InvalidObjectIdError(f"Geçersiz ObjectId formatı: {_id}")
        try:
            _id = ObjectId(_id)
            collection_ref = self.db[collection]
            document = collection_ref.find_one({"_id": _id})
            if not document:
                raise DocumentNotFoundError(f"Belge {_id} bulunamadı.")
            return document
        except PyMongoError as e:
            raise Exception(f"Belge bulunurken bir hata oluştu: {str(e)}")
