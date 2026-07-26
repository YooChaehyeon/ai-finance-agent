import os
from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)

vectorstore = Chroma(persist_directory="data/vectordb", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
def chat(request: ChatRequest):
    query = request.message
    retrieved_docs = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    prompt = f"""당신은 소상공인을 위한 금융 지원 및 정책자금 전문 AI 에이전트입니다.
아래 제공된 [참고 문서]의 내용을 바탕으로 사용자의 질문에 친절하고 정확하게 답변해 주세요.

[참고 문서]:
{context}

질문: {query}"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return {"reply": response.text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)