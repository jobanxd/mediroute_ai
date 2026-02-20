import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import TypingIndicator from './TypingIndicator';

const ChatContainer = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => uuidv4());
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const sendMessage = async (userInput) => {
    const userMessage = { text: userInput, isUser: true };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await axios.post('/chat/message', {
        session_id: sessionId,
        user_input: userInput,
      });

      const aiMessage = { text: response.data.response, isUser: false };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        text: 'Sorry, something went wrong. Please try again.',
        isUser: false,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewSession = () => {
    setMessages([]);
    setSessionId(uuidv4());
  };

  return (
    <div className="flex flex-col w-full max-w-3xl h-full mx-auto">
      {/* Header */}
      <div className="flex-shrink-0 mb-6 text-center">
        <h1 className="text-4xl font-bold gradient-text mb-3">MediRoute AI</h1>
        <button
          onClick={handleNewSession}
          className="px-6 py-2.5 text-sm font-medium bg-white/5 hover:bg-white/10 text-slate-300 rounded-full transition-all backdrop-blur-sm"
        >
          New Session
        </button>
        <p className="text-slate-500 text-xs mt-2 font-mono">
          {sessionId.slice(0, 8)}...
        </p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-6 mb-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full">
            <div className="w-20 h-20 mb-6 bg-gradient-to-br from-blue-500 via-purple-600 to-violet-600 rounded-full flex items-center justify-center">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold text-slate-300">
              Welcome to MediRoute AI
            </h2>
          </div>
        )}
        
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg.text} isUser={msg.isUser} />
        ))}
        
        {isLoading && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex-shrink-0">
        <ChatInput onSend={sendMessage} disabled={isLoading} />
      </div>
    </div>
  );
};

export default ChatContainer;
