import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

print("=== 사용 가능한 모델 목록 ===")
for m in client.models.list():
    if "generateContent" in m.supported_actions:
        print(m.name)