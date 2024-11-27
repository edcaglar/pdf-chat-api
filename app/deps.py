from collections.abc import Generator
from fastapi import Depends
from fastapi import Depends, HTTPException
from app.services.storage.aws_s3 import S3Manager, NoCredentialsError
from app.services.storage.mongo_db import MongoDBManager
from app.services.llm_service import LLMService
from dotenv import load_dotenv
import os
from typing import Annotated
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, InvalidArgument

load_dotenv()

# AWS S3 Bağımlılığı
def get_s3_manager() -> Generator[S3Manager, None, None]:
    s3_manager = S3Manager(
        bucket_name=os.getenv("AWS_BUCKET_NAME"),
        aws_access_key=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_key=os.getenv("AWS_SECRET_KEY")
    )
    try:
        yield s3_manager
    except NoCredentialsError as e:
        raise HTTPException(status_code=500, detail=f"S3Manager başlatılırken hata oluştu {e}")


# MongoDB Bağımlılığı
def get_mongo_manager() -> Generator[MongoDBManager, None, None]:

    try:
        mongo_manager = MongoDBManager(
        uri=os.getenv("MONGODB_URI"),
        database_name=os.getenv("MONGO_DB_NAME")
        )
        yield mongo_manager
    except ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=500, detail="MongoDB'ye bağlanılamadı.")
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB Hatası: {str(e)}")


# MongoDB Bağımlılığı
def get_llm_service() -> Generator[LLMService, None, None]:
    try:
        llm_service = LLMService(api_key=os.getenv("GEMINI_API_KEY"))
        yield llm_service
    except TimeoutError as e:
        raise Exception(f"LLM servisi zaman aşımına uğradı: {str(e)}")
    except ResourceExhausted as e:
        raise Exception(f"Gemini API exceeds request per minute limit.: {str(e)}")
    except ServiceUnavailable as e:
        raise Exception(f"Gemini API Server isn't responding to the incoming requests.: {str(e)}")
    except InvalidArgument as e:
        raise Exception(f"Request exceeds the model's input token limit.: {str(e)}")


# Annotated Types
S3Dep = Annotated[S3Manager, Depends(get_s3_manager)]
MongoDep = Annotated[MongoDBManager, Depends(get_mongo_manager)]
LLMDep = Annotated[LLMService, Depends(get_llm_service)]
