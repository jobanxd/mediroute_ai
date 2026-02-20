import React, { useState } from 'react';

const ChatInput = ({ onSend, disabled }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 p-4 bg-black/10 backdrop-blur-md rounded-3xl">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Describe your symptoms, location, and insurance..."
        disabled={disabled}
        className="flex-1 px-5 py-4 text-base bg-white/5 rounded-2xl text-slate-100 placeholder-slate-400 focus:outline-none focus:bg-white/10 disabled:opacity-50 transition-all"
      />
      <button
        type="submit"
        disabled={disabled || !input.trim()}
        className="px-8 py-4 text-base font-medium bg-gradient-to-br from-blue-500 via-purple-600 to-violet-600 hover:from-blue-600 hover:via-purple-700 hover:to-violet-700 text-white rounded-2xl disabled:opacity-50 transition-all"
      >
        Send
      </button>
    </form>
  );
};

export default ChatInput;
