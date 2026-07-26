# 🚀 소상공인 정책자금 안내 RAG AI 에이전트

소상공인 정책자금 공고문(PDF)을 기반으로 정확한 금융 지원 정보와 자격 요건을 안내하는 RAG(Retrieval-Augmented Generation) AI 챗봇입니다.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **LLM:** Google Gemini API (`google-genai` SDK)
- **Framework:** LangChain
- **Vector DB & Embedding:** Chroma DB, `jhgan/ko-sroberta-multitask`

## 🚀 Quick Start
1. 필요한 라이브러리 설치
   ```bash
   pip install langchain-community langchain-text-splitters langchain-huggingface langchain-chroma google-genai python-dotenv