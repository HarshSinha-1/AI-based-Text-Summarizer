"use client";

import { useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Backend API URL

export default function Home() {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSummarize = async () => {
    // Reset states
    setError("");
    setSummary("");
    
    if (!text.trim() && !file) {
      setError("Please provide text or upload a PDF file.");
      return;
    }

    setIsLoading(true);

    try {
      if (file) {
        // Handle PDF Upload
        const formData = new FormData();
        formData.append("file", file);
        
        const response = await axios.post(`${API_BASE_URL}/api/summarize/pdf`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setSummary(response.data.summary);
      } else {
        // Handle Text Input
        const response = await axios.post(`${API_BASE_URL}/api/summarize/text`, { text });
        setSummary(response.data.summary);
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        "An error occurred while connecting to the backend. Make sure the FastAPI server is running."
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8 text-center">AI Text Summarizer</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-semibold mb-4">Input Data</h2>
        
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-3 rounded-md mb-4 text-sm">
            {error}
          </div>
        )}

        <div className="mb-4 text-sm text-gray-600">
          Option 1: Paste text directly
        </div>
        <textarea 
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={!!file || isLoading}
          className="w-full h-40 p-3 border rounded-md mb-4 focus:ring-2 focus:ring-blue-500 outline-none disabled:bg-gray-100 disabled:text-gray-400"
          placeholder="Paste your text here..."
        ></textarea>
        
        <div className="flex items-center space-x-4 mb-4">
          <span className="text-gray-500 font-medium">OR</span>
          <div className="flex flex-col">
             <span className="text-sm text-gray-600 mb-1">Option 2: Upload a PDF document</span>
             <input 
              type="file" 
              accept=".pdf" 
              onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
              disabled={text.length > 0 || isLoading}
              className="file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50 cursor-pointer" 
            />
          </div>
        </div>
        
        <button 
          onClick={handleSummarize}
          disabled={isLoading || (!text && !file)}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:bg-blue-400 flex justify-center items-center font-medium mt-6"
        >
          {isLoading ? (
            <span className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing via AI...
            </span>
          ) : (
            "Generate Summary"
          )}
        </button>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Summary Result</h2>
        <div className="p-4 bg-gray-50 border border-gray-100 rounded-md min-h-[150px] text-gray-800 whitespace-pre-wrap leading-relaxed shadow-inner">
          {summary || <span className="text-gray-400 italic">Your AI-generated summary will appear here.</span>}
        </div>
      </div>
    </main>
  );
}
