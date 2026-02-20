import React from 'react';

const ChatMessage = ({ message, isUser }) => {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6 animate-fadeIn`}>
      <div className={`max-w-[75%] min-w-0`}>
        <div
          className={`rounded-3xl px-8 py-5 inline-block ${
            isUser
              ? 'bg-gradient-to-br from-blue-500 via-purple-600 to-violet-600 text-white'
              : 'bg-white/5 backdrop-blur-sm text-slate-100'
          }`}
        >
          <p className="text-base leading-relaxed whitespace-pre-wrap break-words overflow-hidden">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
