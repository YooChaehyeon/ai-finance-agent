import os
from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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
    model="models/text-embedding-004", 
    google_api_key=api_key
)
vectorstore = Chroma(persist_directory="data/vectordb", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

class ChatRequest(BaseModel):
    message: str

# 1. 메인 주소 접속 시 바로 대화창 화면(HTML) 출력
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>KB 소상공인 금융 AI 에이전트</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; }
            #chat-box { height: 350px; overflow-y: scroll; border: 1px solid #eee; padding: 10px; margin-bottom: 10px; }
            .msg { margin: 8px 0; }
            .user { text-align: right; color: blue; }
            .bot { text-align: left; color: green; }
            input { width: 78%; padding: 10px; }
            button { width: 18%; padding: 10px; }
        </style>
    </head>
    <body>
        <h2>🤖 KB 소상공인 금융 AI 에이전트</h2>
        <div id="chat-box"></div>
        <input type="text" id="query" placeholder="질문을 입력하세요..." onkeypress="if(event.keyCode==13) sendMsg()">
        <button onclick="sendMsg()">전송</button>

        <script>
            async function sendMsg() {
                const input = document.getElementById('query');
                const box = document.getElementById('chat-box');
                const text = input.value;
                if(!text) return;

                box.innerHTML += `<div class="msg user"><b>나:</b> ${text}</div>`;
                input.value = '';
                box.scrollTop = box.scrollHeight;

                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                box.innerHTML += `<div class="msg bot"><b>AI:</b> ${data.reply}</div>`;
                box.scrollTop = box.scrollHeight;
            }
        </script>
    </body>
    </html>
    """

# 2. 기존 AI 답변 API Endpoint
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