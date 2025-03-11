# MongoDb Vector Search Test 1

1. Create `VectorTest` database.
2. Create `test` collection.
3. Create vector index:

```
db.test.createSearchIndex(
  "vectorIndex",
  "vectorSearch",
  {
     "fields": [
        {
           "type": "vector",
           "path": "embedding",
           "numDimensions": 1536,
           "similarity": "cosine"
        }
     ]
  }
);
```

4. Run `ingest.py`.
5. Run `search.py`.

