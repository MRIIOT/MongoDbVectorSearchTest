import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from PIL import Image
from io import BytesIO
from pdf2image import convert_from_path
import pytesseract
import asyncio
from helper import get_embedding
import secrets

ATLAS_DATABASE = "VectorTest"
ATLAS_COLLECTION = "test"
FILE = "/Users/chrismisztur/Downloads/fus_810348_manual.pdf"


async def main():
    os.environ['OMP_THREAD_LIMIT'] = '4'

    db_client = AsyncIOMotorClient(
        secrets.ATLAS_CONNECTION_STRING,
        maxPoolSize=5,
        minPoolSize=1,
        uuidRepresentation="standard",
    )
    db: AsyncIOMotorDatabase = db_client[ATLAS_DATABASE]

    print("converting pdf to image")
    pages = convert_from_path(f"{FILE}")

    for i, page in enumerate(pages):
        print("---")
        print(f"page {i}")
        image_buffer = BytesIO()
        page.save(image_buffer, 'JPEG')
        image_buffer.seek(0)
        image = Image.open(image_buffer)
        text = pytesseract.image_to_string(image)
        embedding = await get_embedding(text, secrets.OPENAI_API_KEY)
        print(f"inserting: {text}, {embedding}")
        await db[ATLAS_COLLECTION].insert_one({
            "file": FILE,
            "page": i,
            "text": text,
            "embedding": embedding
        })


asyncio.run(main())