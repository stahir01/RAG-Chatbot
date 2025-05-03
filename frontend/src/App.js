// frontend/src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

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
    <div className="App">
      <header className="App-header">
        <h1>Medical Chatbot</h1>
      </header>
      <main className="chat-container">
        <div className="chat-history">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <strong>{msg.role === 'user' ? 'You:' : msg.role === 'assistant' ? 'Chatbot:' : 'Error:'}</strong> {msg.content}
            </div>
          ))}
          {loading && <div className="message assistant"><strong>Chatbot:</strong> Thinking...</div>}
        </div>
        <div className="input-area">
          <input
            type="text"
            value={message}
            onChange={handleInputChange}
            placeholder="Ask a question..."
            onKeyPress={(event) => event.key === 'Enter' && handleSendMessage()}
          />
          <button onClick={handleSendMessage} disabled={loading}>
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;