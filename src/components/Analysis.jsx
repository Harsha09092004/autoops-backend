import React, { useState } from 'react';
import { Send, FileText, Mail, Loader } from 'lucide-react';
import { apiService } from '../api';

export default function Analysis({ onAnalysisComplete }) {
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const [result, setResult] = useState(null);

    const handleAnalyzeWithEmail = async (e) => {
        e.preventDefault();
        if (!email.trim()) {
            setMessage({ type: 'error', text: 'Please enter an email address' });
            return;
        }

        setLoading(true);
        setMessage(null);

        try {
            const response = await apiService.analyzeWithEmail(email);
            setResult(response.data);
            setMessage({
                type: 'success',
                text: `✅ Analysis sent to ${email}!`
            });
            setEmail('');
            onAnalysisComplete();
        } catch (error) {
            setMessage({
                type: 'error',
                text: error.response?.data?.detail || 'Failed to send analysis'
            });
        } finally {
            setLoading(false);
        }
    };

    const handleSendEmail = async (e) => {
        e.preventDefault();
        if (!email.trim()) {
            setMessage({ type: 'error', text: 'Please enter an email address' });
            return;
        }

        setLoading(true);
        setMessage(null);

        try {
            const response = await apiService.sendEmail(email);
            setMessage({
                type: 'success',
                text: `✅ Report email sent to ${email}!`
            });
            setEmail('');
        } catch (error) {
            setMessage({
                type: 'error',
                text: error.response?.data?.detail || 'Failed to send email'
            });
        } finally {
            setLoading(false);
        }
    };

    const handleExportPDF = async () => {
        try {
            const response = await apiService.exportPDF();
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'AutoOps_Report.pdf');
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (error) {
            setMessage({
                type: 'error',
                text: 'Failed to export PDF'
            });
        }
    };

    return (
        <div className="space-y-6 fade-in">
            {/* Message Alert */}
            {message && (
                <div className={`p-4 rounded-lg border ${
                    message.type === 'success'
                        ? 'bg-green-900/30 border-green-700 text-green-200'
                        : 'bg-red-900/30 border-red-700 text-red-200'
                }`}>
                    {message.text}
                </div>
            )}

            {/* Action Cards */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Run Analysis & Email */}
                <div className="card">
                    <div className="flex items-center gap-3 mb-4">
                        <Send className="w-6 h-6 text-blue-400" />
                        <h3 className="text-lg font-semibold text-white">Analyze & Email</h3>
                    </div>
                    <p className="text-slate-400 text-sm mb-4">
                        Run analysis and send report directly to email
                    </p>
                    <form onSubmit={handleAnalyzeWithEmail} className="space-y-3">
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="your@email.com"
                            className="input-field"
                            disabled={loading}
                        />
                        <button
                            type="submit"
                            disabled={loading}
                            className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50"
                        >
                            {loading ? (
                                <>
                                    <Loader className="w-4 h-4 animate-spin" />
                                    Sending...
                                </>
                            ) : (
                                <>
                                    <Send className="w-4 h-4" />
                                    Send Analysis
                                </>
                            )}
                        </button>
                    </form>
                </div>

                {/* Send Email Report */}
                <div className="card">
                    <div className="flex items-center gap-3 mb-4">
                        <Mail className="w-6 h-6 text-green-400" />
                        <h3 className="text-lg font-semibold text-white">Email Report</h3>
                    </div>
                    <p className="text-slate-400 text-sm mb-4">
                        Send formatted report to any email address
                    </p>
                    <form onSubmit={handleSendEmail} className="space-y-3">
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="recipient@email.com"
                            className="input-field"
                            disabled={loading}
                        />
                        <button
                            type="submit"
                            disabled={loading}
                            className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50"
                        >
                            {loading ? (
                                <>
                                    <Loader className="w-4 h-4 animate-spin" />
                                    Sending...
                                </>
                            ) : (
                                <>
                                    <Mail className="w-4 h-4" />
                                    Send Email
                                </>
                            )}
                        </button>
                    </form>
                </div>

                {/* Export PDF */}
                <div className="card">
                    <div className="flex items-center gap-3 mb-4">
                        <FileText className="w-6 h-6 text-purple-400" />
                        <h3 className="text-lg font-semibold text-white">Export PDF</h3>
                    </div>
                    <p className="text-slate-400 text-sm mb-4">
                        Download professional PDF report
                    </p>
                    <button
                        onClick={handleExportPDF}
                        disabled={loading}
                        className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50"
                    >
                        {loading ? (
                            <>
                                <Loader className="w-4 h-4 animate-spin" />
                                Generating...
                            </>
                        ) : (
                            <>
                                <FileText className="w-4 h-4" />
                                Download PDF
                            </>
                        )}
                    </button>
                </div>
            </div>

            {/* Result Display */}
            {result && (
                <div className="card bg-gradient-to-r from-blue-900/40 to-purple-900/40 border-blue-700/50">
                    <h3 className="text-xl font-semibold text-white mb-4">Analysis Result</h3>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
                        <div className="bg-slate-700/50 rounded p-3">
                            <p className="text-slate-400 text-sm">Inactive Users</p>
                            <p className="text-2xl font-bold text-white">{result.data.total_inactive}</p>
                        </div>
                        <div className="bg-slate-700/50 rounded p-3">
                            <p className="text-slate-400 text-sm">Monthly Savings</p>
                            <p className="text-2xl font-bold text-green-400">₹{result.data.estimated_savings}</p>
                        </div>
                        <div className="bg-slate-700/50 rounded p-3">
                            <p className="text-slate-400 text-sm">Email Sent</p>
                            <p className="text-sm font-semibold text-blue-400">{result.email_sent ? '✅ Yes' : '❌ No'}</p>
                        </div>
                    </div>
                    <p className="text-slate-300">{result.data.ai_insight}</p>
                </div>
            )}

            {/* Information */}
            <div className="card">
                <h3 className="text-lg font-semibold text-white mb-4">How It Works</h3>
                <div className="space-y-4">
                    <div className="flex gap-4">
                        <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">1</div>
                        <div>
                            <p className="font-semibold text-white">Analyze Users</p>
                            <p className="text-slate-400 text-sm">System scans all users and identifies those inactive for 30+ days</p>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">2</div>
                        <div>
                            <p className="font-semibold text-white">Calculate Savings</p>
                            <p className="text-slate-400 text-sm">Estimates monthly cost savings based on inactive user count</p>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">3</div>
                        <div>
                            <p className="font-semibold text-white">Get Recommendations</p>
                            <p className="text-slate-400 text-sm">Receive AI-driven insights and actionable recommendations</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
