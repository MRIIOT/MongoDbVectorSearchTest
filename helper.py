import requests


async def get_embedding(text, api_key):
    endpoint = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-embedding-ada-002",
        "input": text,
        "options": { "wait_for_model": True }
    }
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"ERR embedding response failure")
            return None
        response_json = response.json()
        data_field = response_json.get("data", [{}])
        first_data_item = data_field[0] if data_field else {}
        embedding = first_data_item.get("embedding", None)
        return embedding
    except:
        print(f"ERR embedding connection failure")
        return None