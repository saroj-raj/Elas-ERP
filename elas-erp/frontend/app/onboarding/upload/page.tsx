'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function UploadPage() {
  const router = useRouter();
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [dragActive, setDragActive] = useState(false);
  const [useHistoricalData, setUseHistoricalData] = useState(false);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setUploadedFiles([...uploadedFiles, ...Array.from(e.dataTransfer.files)]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setUploadedFiles([...uploadedFiles, ...Array.from(e.target.files)]);
    }
  };

  const removeFile = (index: number) => {
    setUploadedFiles(uploadedFiles.filter((_, i) => i !== index));
  };

  const handleComplete = async () => {
    if (uploadedFiles.length === 0) {
      // No files uploaded - use historical data
      localStorage.setItem('useHistoricalData', 'true');
    } else {
      // Save uploaded files info
      localStorage.setItem('uploadedFiles', JSON.stringify(uploadedFiles.map(f => f.name)));
      localStorage.setItem('useHistoricalData', 'false');
    }
    
    // Redirect to dashboard
    router.push('/dashboard/admin');
  };

  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    switch (ext) {
      case 'pdf': return '📄';
      case 'xlsx': case 'xls': return '📊';
      case 'csv': return '📋';
      case 'doc': case 'docx': return '📝';
      default: return '📎';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link href="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">E</span>
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Elas ERP
            </h1>
          </Link>
        </div>
      </header>

      {/* Progress Bar */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-blue-600">Step 3 of 3</span>
            <span className="text-sm text-gray-600">Document Upload</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full" style={{ width: '100%' }}></div>
          </div>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Upload your documents</h2>
            <p className="text-gray-600">Upload financial statements, invoices, or other business documents for AI analysis</p>
          </div>

          {/* Upload Area */}
          <div
            className={`border-2 border-dashed rounded-lg p-12 text-center transition ${
              dragActive
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-blue-400'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="flex flex-col items-center">
              <div className="text-6xl mb-4">📁</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Drag and drop files here
              </h3>
              <p className="text-gray-600 mb-4">or</p>
              <label className="cursor-pointer">
                <span className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition inline-block">
                  Browse Files
                </span>
                <input
                  type="file"
                  multiple
                  onChange={handleFileChange}
                  className="hidden"
                  accept=".pdf,.xlsx,.xls,.csv,.doc,.docx"
                />
              </label>
              <p className="text-sm text-gray-500 mt-4">
                Supported formats: PDF, Excel, CSV, Word (Max 10MB per file)
              </p>
            </div>
          </div>

          {/* Uploaded Files List */}
          {uploadedFiles.length > 0 && (
            <div className="mt-6">
              <h4 className="font-semibold text-gray-900 mb-3">Uploaded Files ({uploadedFiles.length})</h4>
              <div className="space-y-2">
                {uploadedFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-between bg-gray-50 rounded-lg p-3 border border-gray-200">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">{getFileIcon(file.name)}</span>
                      <div>
                        <p className="font-medium text-gray-900">{file.name}</p>
                        <p className="text-sm text-gray-500">{(file.size / 1024).toFixed(2)} KB</p>
                      </div>
                    </div>
                    <button
                      onClick={() => removeFile(index)}
                      className="text-red-600 hover:text-red-800"
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Historical Data Option */}
          <div className="mt-8 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 border border-purple-200">
            <div className="flex items-start space-x-3">
              <span className="text-3xl">🤖</span>
              <div className="flex-1">
                <h4 className="font-semibold text-purple-900 mb-2">AI-Powered Smart Analysis</h4>
                <p className="text-sm text-purple-700 mb-4">
                  {uploadedFiles.length > 0 
                    ? "Our AI will analyze your uploaded documents and provide insights based on your specific data."
                    : "Don't have documents ready? No problem! Our AI can generate insights using industry patterns and historical data from similar businesses."
                  }
                </p>
                {uploadedFiles.length === 0 && (
                  <div className="bg-white rounded-lg p-4 border border-purple-200">
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={useHistoricalData}
                        onChange={(e) => setUseHistoricalData(e.target.checked)}
                        className="w-4 h-4 text-blue-600 rounded"
                      />
                      <span className="text-sm text-gray-700">
                        Use historical patterns from similar businesses in your industry
                      </span>
                    </label>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* What AI Can Do */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="text-2xl mb-2">📊</div>
              <h5 className="font-semibold text-blue-900 mb-1">Data Analysis</h5>
              <p className="text-xs text-blue-700">Extract and analyze financial data automatically</p>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <div className="text-2xl mb-2">💡</div>
              <h5 className="font-semibold text-green-900 mb-1">Smart Insights</h5>
              <p className="text-xs text-green-700">Get AI-powered recommendations and trends</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-4">
              <div className="text-2xl mb-2">📈</div>
              <h5 className="font-semibold text-purple-900 mb-1">Predictions</h5>
              <p className="text-xs text-purple-700">Forecast future performance based on patterns</p>
            </div>
          </div>

          {/* Navigation Buttons */}
          <div className="flex justify-between pt-8">
            <Link
              href="/onboarding/team"
              className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition"
            >
              Back
            </Link>
            <button
              onClick={handleComplete}
              disabled={uploadedFiles.length === 0 && !useHistoricalData}
              className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploadedFiles.length > 0 
                ? 'Complete Setup & Analyze'
                : useHistoricalData
                  ? 'Complete Setup with Historical Data'
                  : 'Skip & Complete Setup'
              }
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
