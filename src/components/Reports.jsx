import React, { useState, useEffect } from 'react';
import { RefreshCw, Trash2, AlertCircle } from 'lucide-react';
import { apiService } from '../api';

export default function Reports() {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState(null);

    useEffect(() => {
        fetchReports();
    }, []);

    const fetchReports = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await apiService.getReports();
            setReports(response.data || []);
        } catch (err) {
            setError('Failed to fetch reports');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleClearReports = async () => {
        if (window.confirm('Are you sure you want to clear all reports? This cannot be undone.')) {
            try {
                await apiService.clearReports();
                setReports([]);
                setMessage({ type: 'success', text: '✅ All reports cleared' });
                setTimeout(() => setMessage(null), 3000);
            } catch (err) {
                setMessage({ type: 'error', text: '❌ Failed to clear reports' });
            }
        }
    };

    if (error) {
        return (
            <div className="p-6">
                <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 text-red-200">
                    {error}
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6 fade-in">
            {message && (
                <div className={`p-4 rounded-lg border ${
                    message.type === 'success'
                        ? 'bg-green-900/30 border-green-700 text-green-200'
                        : 'bg-red-900/30 border-red-700 text-red-200'
                }`}>
                    {message.text}
                </div>
            )}

            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white">Report History</h2>
                    <p className="text-slate-400 mt-1">{reports.length} reports in database</p>
                </div>
                <div className="flex gap-3">
                    <button
                        onClick={fetchReports}
                        disabled={loading}
                        className="btn-secondary flex items-center gap-2 disabled:opacity-50"
                    >
                        <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                        Refresh
                    </button>
                    {reports.length > 0 && (
                        <button
                            onClick={handleClearReports}
                            className="btn-danger flex items-center gap-2"
                        >
                            <Trash2 className="w-4 h-4" />
                            Clear All
                        </button>
                    )}
                </div>
            </div>

            {/* Reports List */}
            {loading ? (
                <div className="flex items-center justify-center h-96">
                    <div className="text-center">
                        <RefreshCw className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
                        <p className="text-slate-400">Loading reports...</p>
                    </div>
                </div>
            ) : reports.length === 0 ? (
                <div className="card flex flex-col items-center justify-center py-12">
                    <AlertCircle className="w-12 h-12 text-slate-600 mb-4" />
                    <p className="text-slate-400 text-lg">No reports found</p>
                    <p className="text-slate-500 text-sm mt-2">Run an analysis to generate reports</p>
                </div>
            ) : (
                <div className="space-y-4">
                    {reports.map((report, idx) => (
                        <div key={idx} className="card hover:bg-slate-750 transition">
                            <div className="flex items-start justify-between mb-4">
                                <div>
                                    <p className="text-sm text-slate-400">
                                        {new Date(report.timestamp).toLocaleString()}
                                    </p>
                                    <h3 className="text-lg font-semibold text-white mt-1">
                                        Analysis Report #{idx + 1}
                                    </h3>
                                </div>
                                <span className="badge bg-blue-600">
                                    {report.data.total_inactive} inactive
                                </span>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                                <div className="bg-slate-700/50 rounded p-3">
                                    <p className="text-slate-400 text-sm">Inactive Users</p>
                                    <p className="text-2xl font-bold text-white">{report.data.total_inactive}</p>
                                </div>
                                <div className="bg-slate-700/50 rounded p-3">
                                    <p className="text-slate-400 text-sm">Estimated Savings</p>
                                    <p className="text-2xl font-bold text-green-400">₹{report.data.estimated_savings}</p>
                                </div>
                                <div className="bg-slate-700/50 rounded p-3">
                                    <p className="text-slate-400 text-sm">Cost Per User</p>
                                    <p className="text-2xl font-bold text-blue-400">₹125</p>
                                </div>
                            </div>

                            <div className="bg-slate-700/30 rounded p-3 border border-slate-600">
                                <p className="text-slate-300 text-sm line-clamp-3">{report.data.ai_insight}</p>
                            </div>

                            {report.data.inactive_users.length > 0 && (
                                <div className="mt-4 pt-4 border-t border-slate-700">
                                    <p className="text-sm font-semibold text-slate-300 mb-3">Inactive Users:</p>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                        {report.data.inactive_users.slice(0, 4).map((user, i) => (
                                            <div key={i} className="text-sm text-slate-400">
                                                • {user.name} ({user.days_inactive} days)
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
