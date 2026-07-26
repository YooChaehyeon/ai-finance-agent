import React, { useState } from 'react';
import './App.css';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'https://ai-finance-agent-1ign.onrender.com';

function App() {
  const initialGreeting =
    '안녕하세요! 소상공인 금융 지원 AI Agent입니다.\n궁금한 정책자금 및 지원사업에 대해 질문해 보세요!';

  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: initialGreeting,
    },
  ]);

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  // 새 대화 시작
  const handleNewChat = () => {
    setMessages([
      {
        sender: 'ai',
        text: initialGreeting,
      },
    ]);
    setInput('');
  };

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;

    if (!textToSend.trim() || loading) {
      return;
    }

    const userMsg = {
      sender: 'user',
      text: textToSend,
    };

    setMessages((prev) => [...prev, userMsg]);

    if (!queryText) {
      setInput('');
    }

    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: textToSend,
        }),
      });

      if (!res.ok) {
        throw new Error(`서버 응답 오류: ${res.status}`);
      }

      const data = await res.json();

      const reply =
        data.reply ||
        data.answer ||
        data.message ||
        '답변을 받아오지 못했습니다.';

      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: reply,
        },
      ]);
    } catch (err) {
      console.error('채팅 API 요청 오류:', err);

      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: '오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.nativeEvent.isComposing) {
      handleSend();
    }
  };

  return (
    <div className="app-container">
      {/* 상단 배너 */}
      <div className="top-banner">
        현직자 PICK 주제 | 소상공인 금융 지원 AI Challenge
      </div>

      <div className="main-content">
        {/* 좌측 사이드바 */}
        <div className="sidebar">
          <button className="new-chat-btn" onClick={handleNewChat}>
            + 새 대화
          </button>

          <div className="sidebar-section">
            <p className="sidebar-title">추천 질문 목록</p>

            <div
              className="chat-history-item"
              onClick={() =>
                handleSend(
                  '소상공인 정책자금 신청 자격과 제한 대상은 무엇인가요?'
                )
              }
            >
              📌 소상공인 정책자금 자격 조건
            </div>

            <div
              className="chat-history-item"
              onClick={() =>
                handleSend(
                  '대출 금리 우대 혜택을 받기 위한 요구 조건이 뭐야?'
                )
              }
            >
              💳 금리 우대 혜택 가이드
            </div>
          </div>
        </div>

        {/* 메인 대화 영역 */}
        <div className="chat-section">
          <div className="chat-header">
            <div className="header-info">
              <h2>🤖 금융 지원 AI 에이전트</h2>
              <span className="status-badge">● 실시간 작동 중</span>
            </div>
          </div>

          <div className="messages-list">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-row ${msg.sender}`}>
                <div className="avatar">
                  {msg.sender === 'ai' ? '🤖' : '😊'}
                </div>

                <div className="chat-content-box">
                  <span className="sender-name">
                    {msg.sender === 'ai' ? 'AI Agent' : '사용자'}
                  </span>

                  <div className="message-bubble">
                    {msg.text}
                  </div>
                </div>
              </div>
            ))}

            {loading && (
              <div className="chat-row ai">
                <div className="avatar">🤖</div>

                <div className="chat-content-box">
                  <span className="sender-name">AI Agent</span>

                  <div className="message-bubble loading-bubble">
                    답변 생성 중...
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="input-area">
            <input
              type="text"
              placeholder="AI 에이전트에게 질문해 보세요..."
              value={input}
              disabled={loading}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
            />

            <button
              onClick={() => handleSend()}
              disabled={loading || !input.trim()}
            >
              {loading ? '처리 중' : '전송'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;