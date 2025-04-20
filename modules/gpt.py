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

def render_image(base64_image: str, ext: str, history: list = []) -> dict:
    history.append({
        "role": "user",
        "content": [{
            "type": "input_image",
            "image_url": f"data:image/{ext};base64,{base64_image}"
        }]
    })

    return history

def render_pdf(base64_pdf: str, history: list = []) -> dict:
    history.append({
        "role": "user",
        "content": [{
            "type": "input_file",
            "filename": "file.pdf",
            "file_data": f"data:application/pdf;base64,{base64_pdf}"
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