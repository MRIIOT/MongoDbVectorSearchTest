import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from helper import get_embedding
import secrets

ATLAS_DATABASE = "VectorTest"
ATLAS_COLLECTION = "test"
QUERY_TEXT = "how much distance between tv and other objects"


async def main():
    embedding = await get_embedding(QUERY_TEXT, secrets.OPENAI_API_KEY)

    db_client = AsyncIOMotorClient(
            secrets.ATLAS_CONNECTION_STRING,
            maxPoolSize=5,
            minPoolSize=1,
            uuidRepresentation="standard",
        )

    db: AsyncIOMotorDatabase = db_client[ATLAS_DATABASE]
    result = db[ATLAS_COLLECTION].aggregate([
        {
            "$vectorSearch" : {
                "index": "vectorIndex",
                "path": "embedding",
                "queryVector": embedding,
                "numCandidates": 100,
                "limit": 10
            }
        },
        {
            "$project": {
                "file": 1,
                "page": 1,
                "text": 1
            }
        }
    ])

    async for document in result:
        print(document)


asyncio.run(main())
