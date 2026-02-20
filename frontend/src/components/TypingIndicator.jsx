import React from 'react';

const TypingIndicator = () => {
  return (
    <div className="flex justify-start mb-4 animate-fadeIn">
      <div className="bg-white/5 backdrop-blur-sm rounded-3xl px-6 py-4">
        <div className="flex space-x-2">
          <div className="w-2.5 h-2.5 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2.5 h-2.5 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2.5 h-2.5 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
