"use client";

import React from "react";
import Card from "../../components/Card";

export default function AdminDashboard() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Admin Dashboard
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Total Users
              </h3>
              <p className="text-3xl font-bold text-blue-600">1,234</p>
              <p className="text-sm text-gray-500 mt-2">+12% from last month</p>
            </div>
          </Card>

          <Card>
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Revenue
              </h3>
              <p className="text-3xl font-bold text-green-600">$45,678</p>
              <p className="text-sm text-gray-500 mt-2">+8% from last month</p>
            </div>
          </Card>

          <Card>
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Active Projects
              </h3>
              <p className="text-3xl font-bold text-purple-600">23</p>
              <p className="text-sm text-gray-500 mt-2">5 completed this week</p>
            </div>
          </Card>
        </div>

        <div className="mt-8">
          <Card>
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Quick Actions
              </h2>
              <div className="space-y-3">
                <a
                  href="/onboarding/documents"
                  className="block px-4 py-3 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                >
                  <span className="font-medium text-blue-900">📊 Upload Data</span>
                  <p className="text-sm text-blue-700">Upload CSV/Excel files for Quick Viz</p>
                </a>
                <div className="block px-4 py-3 bg-gray-50 rounded-lg">
                  <span className="font-medium text-gray-900">📈 View Reports</span>
                  <p className="text-sm text-gray-600">Coming soon...</p>
                </div>
                <div className="block px-4 py-3 bg-gray-50 rounded-lg">
                  <span className="font-medium text-gray-900">⚙️ Settings</span>
                  <p className="text-sm text-gray-600">Coming soon...</p>
                </div>
              </div>
            </div>
          </Card>
        </div>

        <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <h3 className="font-semibold text-yellow-900 mb-2">🔍 Debug Info:</h3>
          <p className="text-sm text-yellow-800">
            Groq AI responses are logged to: <code className="bg-yellow-100 px-2 py-1 rounded">elas-erp/GROQ_DEBUG.log</code>
          </p>
          <p className="text-sm text-yellow-800 mt-2">
            View with: <code className="bg-yellow-100 px-2 py-1 rounded">Get-Content elas-erp\GROQ_DEBUG.log -Tail 50</code>
          </p>
        </div>
      </div>
    </div>
  );
}
