// frontend/src/App.js
import React, { useState } from 'react';
import './App.css';
import ChatWidget from './ChatWidget';

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
        <h1>Your Website Title</h1> {/* Or keep "Medical Chatbot" if this is a dedicated chatbot page */}
      </header>
      {/* Your other website content can go here */}
      <ChatWidget /> {/* Add the chat widget here */}
    </div>
  );
}

export default App;