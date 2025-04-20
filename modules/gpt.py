from openai import OpenAI

def openai_init(api_key):
    client = OpenAI(api_key=api_key)

    return client

def render_requests(requests: str, history: list = []) -> dict:
    history.append({
        "role": "user",
        "content": requests
    })

    return history

def render_image(image_url: str, history: list = []) -> dict:
    history.append({
        "role": "user",
        "content": [{
            "type": "image_url",
            "image_url": {
                "url": image_url
            }
        }]
    })

    return history

def render_responses(responses: str, history: list = []) -> dict:
    history.append({
        "role": "assistant",
        "content": responses
    })

    return history

def gpt_request(client, model, history: list = []):
    completion = client.responses.create(
        model=model,
        input=history,
        stream=True
    )

    return completion