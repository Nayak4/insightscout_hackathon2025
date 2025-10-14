import ssl
import httpx
import logging
from openai import AzureOpenAI
from config import API_KEY, API_ENDPOINT, CERT_PATH, MODEL_NAME

ctx = ssl.create_default_context(cafile=CERT_PATH)
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=API_ENDPOINT,
    api_key=API_KEY,
    http_client=httpx.Client(verify=ctx),
)


def azure_generate(prompt: str, model: str = MODEL_NAME, temperature: float = 0.1) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        logging.error(f"Azure OpenAI error: {exc}")
        return ""
