export default function Home() {
  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8 text-center">AI Text Summarizer</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-semibold mb-4">Input</h2>
        <textarea 
          className="w-full h-40 p-3 border rounded-md mb-4 focus:ring-2 focus:ring-blue-500 outline-none"
          placeholder="Paste your text here..."
        ></textarea>
        
        <div className="flex items-center space-x-4 mb-4">
          <span className="text-gray-500">OR</span>
          <input type="file" accept=".pdf" className="file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
        </div>
        
        <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">
          Summarize
        </button>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Summary</h2>
        <div className="p-4 bg-gray-50 rounded-md min-h-[100px] text-gray-700">
          Your summary will appear here...
        </div>
      </div>
    </main>
  );
}
