"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface Widget {
  id: string;
  type: string;
  title: string;
  data: any;
  config?: any;
  vega_spec?: any;
  explanation?: string;
}

const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4'];

export default function AdminDashboard() {
  const [widgets, setWidgets] = useState<Widget[]>([]);
  const [previewData, setPreviewData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('🔍 AdminDashboard - Component mounted');
    
    try {
      const uploadResponseStr = localStorage.getItem('uploadResponse');
      console.log('📦 uploadResponse from localStorage:', uploadResponseStr ? 'Found' : 'Not found');
      
      if (uploadResponseStr) {
        const uploadResponse = JSON.parse(uploadResponseStr);
        console.log('📊 Loaded widgets from localStorage:', uploadResponse.widgets?.length || 0, 'widgets');
        console.log('🔍 Widget types:', uploadResponse.widgets?.map((w: Widget) => w.type).join(', '));
        
        if (uploadResponse.widgets && Array.isArray(uploadResponse.widgets)) {
          setWidgets(uploadResponse.widgets);
          setPreviewData(uploadResponse.preview || []);
          console.log('📈 Preview data rows:', uploadResponse.preview?.length || 0);
          setError(null);
        } else {
          console.warn('⚠️ No widgets found in uploadResponse');
          setError('No widgets available. Please upload data first.');
        }
      } else {
        console.warn('⚠️ No uploadResponse in localStorage');
        setError('No data found. Please upload and analyze your data first.');
      }
    } catch (err) {
      console.error('❌ Error loading widgets:', err);
      setError('Failed to load dashboard data.');
    } finally {
      setLoading(false);
    }
  }, []);

  const prepareChartData = (widget: Widget) => {
    if (!previewData || previewData.length === 0) return [];
    
    const xField = widget.config?.x_column || widget.vega_spec?.encoding?.x?.field;
    const yField = widget.config?.y_column || widget.vega_spec?.encoding?.y?.field;
    
    if (!xField || !yField) return [];
    
    // Take first 20 rows for chart
    return previewData.slice(0, 20).map(row => ({
      name: String(row[xField] || ''),
      value: Number(row[yField]) || 0,
      [xField]: row[xField],
      [yField]: row[yField],
    }));
  };

  const renderWidget = (widget: Widget) => {
    console.log('🎨 Rendering widget:', widget.type, '-', widget.title);
    
    switch (widget.type) {
      case 'bar_chart':
        const barData = prepareChartData(widget);
        return (
          <div key={widget.id} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{widget.title}</h3>
            {widget.explanation && (
              <p className="text-sm text-gray-600 mb-4">{widget.explanation}</p>
            )}
            {barData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={barData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="bg-gray-100 rounded p-4 text-center text-gray-500">
                No data available for this chart
              </div>
            )}
          </div>
        );

      case 'line_chart':
        const lineData = prepareChartData(widget);
        return (
          <div key={widget.id} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{widget.title}</h3>
            {widget.explanation && (
              <p className="text-sm text-gray-600 mb-4">{widget.explanation}</p>
            )}
            {lineData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={lineData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#8b5cf6" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="bg-gray-100 rounded p-4 text-center text-gray-500">
                No data available for this chart
              </div>
            )}
          </div>
        );

      case 'pie_chart':
        const pieData = prepareChartData(widget).slice(0, 6); // Limit to 6 slices
        return (
          <div key={widget.id} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{widget.title}</h3>
            {widget.explanation && (
              <p className="text-sm text-gray-600 mb-4">{widget.explanation}</p>
            )}
            {pieData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(entry) => entry.name}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="bg-gray-100 rounded p-4 text-center text-gray-500">
                No data available for this chart
              </div>
            )}
          </div>
        );

      case 'kpi':
        const value = widget.data?.value || widget.data?.metric_value || 'N/A';
        return (
          <div key={widget.id} className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow-md p-6 text-white">
            <h3 className="text-sm font-medium opacity-90 mb-2">{widget.title}</h3>
            <div className="text-4xl font-bold mb-2">{value}</div>
            {widget.config?.description && (
              <p className="text-sm opacity-80">{widget.config.description}</p>
            )}
          </div>
        );

      case 'table':
        const tableData = previewData.slice(0, 10); // Show first 10 rows
        const columns = tableData.length > 0 ? Object.keys(tableData[0]) : [];
        
        return (
          <div key={widget.id} className="bg-white rounded-lg shadow-md p-6 col-span-full">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{widget.title}</h3>
            {widget.explanation && (
              <p className="text-sm text-gray-600 mb-4">{widget.explanation}</p>
            )}
            {tableData.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      {columns.map((col) => (
                        <th
                          key={col}
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {tableData.map((row, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        {columns.map((col) => (
                          <td key={col} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {row[col] !== null && row[col] !== undefined ? String(row[col]) : '-'}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {previewData.length > 10 && (
                  <p className="text-sm text-gray-500 mt-3 text-center">
                    Showing 10 of {previewData.length} rows
                  </p>
                )}
              </div>
            ) : (
              <div className="bg-gray-100 rounded p-4 text-center text-gray-500">
                No data available
              </div>
            )}
          </div>
        );

      default:
        return (
          <div key={widget.id} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">{widget.title}</h3>
            <div className="bg-red-50 border border-red-200 rounded p-4">
              <p className="text-red-700 font-semibold mb-2">⚠️ Unsupported widget type: "{widget.type}"</p>
              <p className="text-xs text-gray-600 mb-2">Expected types: bar_chart, line_chart, pie_chart, kpi, table</p>
              <details className="text-xs">
                <summary className="cursor-pointer text-blue-600 hover:text-blue-800">Show widget data</summary>
                <pre className="mt-2 bg-gray-100 p-2 rounded overflow-x-auto">{JSON.stringify(widget, null, 2)}</pre>
              </details>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">🏢 Elas ERP</h1>
              <p className="text-sm text-gray-500">Admin Dashboard</p>
            </div>
            <Link
              href="/onboarding/upload"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Upload New Data
            </Link>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p className="text-gray-600">Loading dashboard...</p>
          </div>
        ) : error ? (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
            <svg className="w-12 h-12 text-yellow-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">No Data Available</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <Link
              href="/onboarding/upload"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Upload Data Now
            </Link>
            <div className="mt-8 bg-white border border-gray-200 rounded-lg p-4 text-left">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Debug Info:</h3>
              <ul className="text-xs text-gray-600 space-y-1">
                <li>• Check if you've uploaded data via <code className="bg-gray-100 px-1 rounded">/onboarding/upload</code></li>
                <li>• Ensure localStorage has <code className="bg-gray-100 px-1 rounded">uploadResponse</code> key</li>
                <li>• Backend should be running at <code className="bg-gray-100 px-1 rounded">http://localhost:8000</code></li>
                <li>• Check <code className="bg-gray-100 px-1 rounded">GROQ_DEBUG.log</code> in project root for API calls</li>
              </ul>
            </div>
          </div>
        ) : (
          <>
            {/* Widgets Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {widgets.map((widget) => renderWidget(widget))}
            </div>

            {/* AI Insights Section */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">🤖 AI Insights</h2>
              <p className="text-gray-600 mb-4">
                Your dashboard has been automatically generated using AI analysis of your uploaded data.
                Interactive visualizations powered by <strong>Recharts</strong> display your first 200 data rows.
              </p>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-3">
                <p className="text-sm text-blue-800">
                  <strong>💡 Transparency:</strong> All AI interactions are logged in <code className="bg-blue-100 px-1 rounded">GROQ_DEBUG.log</code> 
                  for full transparency into how your widgets were generated.
                </p>
              </div>
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-sm text-green-800">
                  <strong>📊 Data:</strong> Charts show up to 20 data points. Tables display up to 10 rows from your {previewData.length} loaded records.
                </p>
              </div>
            </div>

            {/* Debug Info */}
            <div className="bg-gray-100 rounded-lg p-4 text-sm text-gray-600">
              <strong>Debug Info:</strong> {widgets.length} widgets loaded • {previewData.length} data rows available
            </div>
          </>
        )}
      </div>
    </div>
  );
}
