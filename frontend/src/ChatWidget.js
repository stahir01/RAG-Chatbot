// frontend/src/components/ChatWidget.js
import React, { useState, useEffect, useRef } from 'react';
import './ChatWidget.css';

const defaultAvatar = '/chatbot.jpeg';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatContainerRef = useRef(null);
  const [chatbotName] = useState('Doctor AI'); // Chatbot's name
  const [chatbotAvatar, setChatbotAvatar] = useState(defaultAvatar);
  const [onlineStatus] = useState('We are online!');

  useEffect(() => {
    if (isOpen && chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [isOpen, chatHistory]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleInputChange = (event) => {
    setMessage(event.target.value);
  };

  const handleSendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setChatHistory([...chatHistory, { role: 'user', content: message }]);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Something went wrong');
      }

      const data = await response.json();
      setChatHistory([...chatHistory, { role: 'user', content: message }, { role: 'assistant', content: data.response }]);
    } catch (error) {
      setChatHistory([...chatHistory, { role: 'user', content: message }, { role: 'error', content: `Error: ${error.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`chat-widget ${isOpen ? 'open' : ''}`}>
      <button className="widget-toggle" onClick={toggleChat}>
        {isOpen ? (
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="close-icon">
            <path fillRule="evenodd" d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 01-1.06-1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z" clipRule="evenodd" />
          </svg>
        ) : (
          <div className="toggle-info">
            <img src={chatbotAvatar} alt={chatbotName} className="toggle-avatar-closed" />
            <span className="chatbot-name">{chatbotName}</span>
          </div>
        )}
      </button>
      {isOpen && (
        <div className="chat-container">
          <div className="chat-header">
            <div className="header-info">
              <img src={chatbotAvatar} alt={`Chat with ${chatbotName}`} className="header-avatar" />
              <div className="header-text">
                <h3 className="header-title">Chat with {chatbotName}</h3>
                <p className="header-status">{onlineStatus}</p>
              </div>
            </div>
            <div className="header-actions">
              <button className="header-dots">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="dots-icon">
                  <path d="M12 10a2 2 0 100 4 2 2 0 000-4zm-6 0a2 2 0 100 4 2 2 0 000-4zm12 0a2 2 0 100 4 2 2 0 000-4z" />
                </svg>
              </button>
              <button className="header-close-button" onClick={toggleChat}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="close-icon">
                  <path fillRule="evenodd" d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 01-1.06-1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
          <div className="chat-history" ref={chatContainerRef}>
            {chatHistory.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                {msg.role === 'assistant' && (
                  <img src={chatbotAvatar} alt={chatbotName} className="avatar" />
                )}
                <span className="message-content">{msg.content}</span>
              </div>
            ))}
            {loading && (
              <div className="message assistant loading-indicator">
                <img src={chatbotAvatar} alt={chatbotName} className="avatar" />
                <span className="message-content">Thinking...</span>
              </div>
            )}
          </div>
          <div className="input-area">
            <div className="input-wrapper">
              <input
                type="text"
                value={message}
                onChange={handleInputChange}
                placeholder="Enter your message..."
                className="input-field"
                onKeyPress={(event) => event.key === 'Enter' && handleSendMessage()}
              />
            </div>
            <button 
              onClick={handleSendMessage} 
              disabled={loading} 
              className="send-button"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 24 24" 
                fill="currentColor" 
                className="send-icon"
              >
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;