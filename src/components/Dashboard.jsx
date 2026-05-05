import React, { useState, useEffect } from 'react';
import { RefreshCw, TrendingUp, Users, DollarSign, CheckCircle } from 'lucide-react';
import { apiService } from '../api';

export default function Dashboard({ onRefresh }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchAnalysis();
    }, []);

    const fetchAnalysis = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await apiService.analyze();
            setData(response.data);
        } catch (err) {
            setError('Failed to fetch analysis data');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (error) {
        return (
            <div className="p-6">
                <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 text-red-200">
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="text-center">
                    <RefreshCw className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
                    <p className="text-slate-400">Loading analysis...</p>
                </div>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="p-6">
                <div className="bg-yellow-900/30 border border-yellow-700 rounded-lg p-4 text-yellow-200">
                    <p>No analysis data available</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6 fade-in">
            {/* Main Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Inactive Users */}
                <div className="stat-card">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-300 text-sm mb-1">Inactive Users</p>
                            <p className="text-4xl font-bold text-white">{data.total_inactive}</p>
                        </div>
                        <Users className="w-12 h-12 text-blue-400 opacity-20" />
                    </div>
                </div>

                {/* Monthly Savings */}
                <div className="stat-card bg-gradient-to-br from-green-900/50 to-green-800/50 border-green-700/50">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-300 text-sm mb-1">Monthly Savings</p>
                            <p className="text-4xl font-bold text-green-400">₹{data.estimated_savings.toLocaleString()}</p>
                        </div>
                        <DollarSign className="w-12 h-12 text-green-400 opacity-20" />
                    </div>
                </div>

                {/* Optimization Level */}
                <div className="stat-card bg-gradient-to-br from-purple-900/50 to-purple-800/50 border-purple-700/50">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-300 text-sm mb-1">Optimization</p>
                            <p className="text-4xl font-bold text-purple-400">{Math.min(data.total_inactive * 2, 30)}%</p>
                        </div>
                        <TrendingUp className="w-12 h-12 text-purple-400 opacity-20" />
                    </div>
                </div>

                {/* Status */}
                <div className="stat-card bg-gradient-to-br from-emerald-900/50 to-emerald-800/50 border-emerald-700/50">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-300 text-sm mb-1">Status</p>
                            <p className="text-lg font-bold text-emerald-400 flex items-center gap-2">
                                <CheckCircle className="w-5 h-5" />
                                Active
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* AI Insight */}
            <div className="card bg-gradient-to-r from-blue-900/40 to-purple-900/40 border-blue-700/50">
                <div className="flex gap-4">
                    <div className="flex-shrink-0 w-12 h-12 bg-blue-600/30 rounded-lg flex items-center justify-center">
                        <TrendingUp className="w-6 h-6 text-blue-400" />
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold text-white mb-2">AI Insight</h3>
                        <p className="text-slate-300 leading-relaxed">{data.ai_insight}</p>
                    </div>
                </div>
            </div>

            {/* Inactive Users Table */}
            <div className="card">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl font-semibold text-white">Inactive Users</h3>
                    <button
                        onClick={fetchAnalysis}
                        className="btn-secondary"
                    >
                        <RefreshCw className="w-4 h-4" />
                    </button>
                </div>

                {data.inactive_users.length > 0 ? (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-slate-700">
                                    <th className="text-left py-3 px-4 text-slate-400 font-medium">Name</th>
                                    <th className="text-left py-3 px-4 text-slate-400 font-medium">Email</th>
                                    <th className="text-left py-3 px-4 text-slate-400 font-medium">Days Inactive</th>
                                    <th className="text-left py-3 px-4 text-slate-400 font-medium">Cost</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data.inactive_users.map((user, idx) => (
                                    <tr key={idx} className="border-b border-slate-700/50 hover:bg-slate-700/30 transition">
                                        <td className="py-3 px-4 text-white font-medium">{user.name}</td>
                                        <td className="py-3 px-4 text-slate-400">{user.email}</td>
                                        <td className="py-3 px-4">
                                            <span className="badge bg-red-600">{user.days_inactive} days</span>
                                        </td>
                                        <td className="py-3 px-4 text-green-400 font-semibold">₹125/mo</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <p className="text-slate-400 text-center py-8">No inactive users found. Great job!</p>
                )}
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <button className="card card-hover flex items-center justify-center gap-3">
                    <TrendingUp className="w-6 h-6 text-blue-400" />
                    <div className="text-left">
                        <p className="text-sm text-slate-400">Run Full</p>
                        <p className="font-semibold text-white">Analysis</p>
                    </div>
                </button>
                <button className="card card-hover flex items-center justify-center gap-3">
                    <DollarSign className="w-6 h-6 text-green-400" />
                    <div className="text-left">
                        <p className="text-sm text-slate-400">View Detailed</p>
                        <p className="font-semibold text-white">Savings Report</p>
                    </div>
                </button>
                <button className="card card-hover flex items-center justify-center gap-3">
                    <Users className="w-6 h-6 text-purple-400" />
                    <div className="text-left">
                        <p className="text-sm text-slate-400">Manage</p>
                        <p className="font-semibold text-white">Users</p>
                    </div>
                </button>
            </div>
        </div>
    );
}
