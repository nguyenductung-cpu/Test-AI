import React, { useState, useEffect } from 'react';
import { Search, Download, Calendar, Filter } from 'lucide-react';

const PBI1_TestScreen = () => {
  const [activeTab, setActiveTab] = useState('status'); // 'status' or 'activity'
  const [keyword, setKeyword] = useState('');
  const [statusFilter, setStatusFilter] = useState([]);
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [error, setError] = useState('');

  // 1. Mandatory Rule: Default range to "Start from today backward 1 month"
  useEffect(() => {
    const today = new Date();
    const lastMonth = new Date();
    lastMonth.setMonth(today.getMonth() - 1);
    
    setDateRange({
      start: lastMonth.toISOString().split('T')[0],
      end: today.toISOString().split('T')[0]
    });
  }, []);

  const statuses = ['Completed', 'Active', 'Pending Approval', 'Cancelled', 'Rejected', 'Expired'];

  // 2. Export Validation Logic
  const handleExport = (type) => {
    if (!dateRange.start || !dateRange.end) {
      setError("Error: Time Range filter is mandatory for exporting data.");
      return;
    }
    setError("");
    alert(`Exporting ${type === 'all' ? 'All' : 'Filtered'} data for period: ${dateRange.start} to ${dateRange.end}`);
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen font-sans">
      <div className="max-w-7xl mx-auto bg-white rounded-lg shadow-sm p-6">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">Goal Management Dashboard</h1>

        {/* Tab Selection */}
        <div className="flex border-b mb-6">
          <button 
            onClick={() => setActiveTab('status')}
            className={`px-6 py-2 font-medium ${activeTab === 'status' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
          >
            Goals Status
          </button>
          <button 
            onClick={() => setActiveTab('activity')}
            className={`px-6 py-2 font-medium ${activeTab === 'activity' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
          >
            Goals Activity
          </button>
        </div>

        {/* Filter Bar */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          {/* Keyword Search */}
          <div className="relative">
            <Search className="absolute left-3 top-3 text-gray-400 size-4" />
            <input 
              type="text"
              placeholder="Search ID, Name, Username..."
              className="pl-10 w-full p-2 border rounded-md"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
            />
          </div>

          {/* Date Picker (DD-MM-YYYY format in UI) */}
          <div className="flex items-center space-x-2 border rounded-md p-2">
            <Calendar className="text-gray-400 size-4" />
            <input 
              type="date" 
              className="outline-none text-sm"
              value={dateRange.start}
              onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
            />
            <span>-</span>
            <input 
              type="date" 
              className="outline-none text-sm"
              value={dateRange.end}
              onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
            />
          </div>

          {/* Multi-select Progress Status (Status Tab Only) */}
          {activeTab === 'status' && (
            <div className="relative">
              <select 
                multiple
                className="w-full p-2 border rounded-md text-sm h-10"
                onChange={(e) => setStatusFilter(Array.from(e.target.selectedOptions, option => option.value))}
              >
                {statuses.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
              <p className="text-[10px] text-gray-400 mt-1">Hold Ctrl/Cmd to select multiple</p>
            </div>
          )}

          {/* Export Buttons */}
          <div className="flex space-x-2">
            <button 
              onClick={() => handleExport('filter')}
              className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md flex items-center justify-center hover:bg-blue-700 transition"
            >
              <Download className="mr-2 size-4" /> Export by Filter
            </button>
          </div>
        </div>

        {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md text-sm">{error}</div>}

        {/* Mock Table */}
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full text-left text-sm">
            <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th className="p-3">Child ID</th>
                <th className="p-3">Nickname</th>
                <th className="p-3">Goal Name</th>
                {activeTab === 'status' ? (
                   <>
                    <th className="p-3">Current Allocated</th>
                    <th className="p-3">Status</th>
                    <th className="p-3">Created Date</th>
                   </>
                ) : (
                  <>
                    <th className="p-3">Amount</th>
                    <th className="p-3">Date & Time</th>
                  </>
                )}
              </tr>
            </thead>
            <tbody className="divide-y">
              <tr className="hover:bg-gray-50">
                <td className="p-3 text-blue-600 font-medium">C-8821</td>
                <td className="p-3">Alex</td>
                <td className="p-3">New Bike</td>
                {activeTab === 'status' ? (
                  <>
                    <td className="p-3">$150.00</td>
                    <td className="p-3"><span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-[10px]">Active</span></td>
                    <td className="p-3">12-01-2026</td>
                  </>
                ) : (
                  <>
                    <td className="p-3">$50.00</td>
                    <td className="p-3 text-gray-500">20-01-2026 14:30</td>
                  </>
                )}
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default PBI1_TestScreen;