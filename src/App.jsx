import React, { useState, useEffect } from 'react';
import { Activity, BarChart3, Mail, FileDown, Settings, Menu, X } from 'lucide-react';
import Dashboard from './components/Dashboard';
import Analysis from './components/Analysis';
import Reports from './components/Reports';
import Settings as SettingsPage from './components/Settings';
import { apiService } from './api';

export default function App() {
    const [currentPage, setCurrentPage] = useState('dashboard');
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const response = await apiService.getStats();
            setStats(response.data);
        } catch (error) {
            console.error('Error fetching stats:', error);
        } finally {
            setLoading(false);
        }
    };

    const navigation = [
        { id: 'dashboard', name: 'Dashboard', icon: Activity },
        { id: 'analysis', name: 'Analysis', icon: BarChart3 },
        { id: 'reports', name: 'Reports', icon: FileDown },
        { id: 'settings', name: 'Settings', icon: Settings },
    ];

    return (
        <div className="flex h-screen bg-slate-900">
            {/* Sidebar */}
            <div className={`${mobileMenuOpen ? 'block' : 'hidden'} md:block fixed md:relative z-40 w-64 h-screen bg-slate-800 border-r border-slate-700 transition-all`}>
                <div className="p-6">
                    <div className="flex items-center gap-3 mb-8">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                            <Activity className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-white">AutoOps AI</h1>
                            <p className="text-xs text-slate-400">Cost Optimizer</p>
                        </div>
                    </div>

                    <nav className="space-y-2">
                        {navigation.map((item) => {
                            const Icon = item.icon;
                            return (
                                <button
                                    key={item.id}
                                    onClick={() => {
                                        setCurrentPage(item.id);
                                        setMobileMenuOpen(false);
                                    }}
                                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                                        currentPage === item.id
                                            ? 'bg-blue-600 text-white'
                                            : 'text-slate-300 hover:bg-slate-700'
                                    }`}
                                >
                                    <Icon className="w-5 h-5" />
                                    <span className="font-medium">{item.name}</span>
                                </button>
                            );
                        })}
                    </nav>
                </div>

                {/* Stats in Sidebar */}
                {stats && (
                    <div className="absolute bottom-6 left-6 right-6 p-4 bg-gradient-to-br from-blue-900/50 to-blue-800/50 rounded-lg border border-blue-700/50">
                        <p className="text-xs text-slate-400 mb-2">Quick Stats</p>
                        <div className="space-y-1">
                            <p className="text-sm font-semibold text-white">{stats.total_json_reports} Reports</p>
                            <p className="text-xs text-slate-400">Local Storage</p>
                        </div>
                    </div>
                )}
            </button>

            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Header */}
                <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                            className="md:hidden p-2 hover:bg-slate-700 rounded-lg"
                        >
                            {mobileMenuOpen ? (
                                <X className="w-6 h-6" />
                            ) : (
                                <Menu className="w-6 h-6" />
                            )}
                        </button>
                        <h2 className="text-2xl font-bold text-white capitalize">
                            {navigation.find(n => n.id === currentPage)?.name}
                        </h2>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="hidden md:block">
                            <p className="text-sm text-slate-400">Last updated: {new Date().toLocaleTimeString()}</p>
                        </div>
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                            <Activity className="w-5 h-5 text-white" />
                        </div>
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 overflow-auto p-6">
                    {loading ? (
                        <div className="flex items-center justify-center h-full">
                            <div className="text-center">
                                <div className="animate-spin mb-4">
                                    <Activity className="w-12 h-12 text-blue-500" />
                                </div>
                                <p className="text-slate-400">Loading...</p>
                            </div>
                        </div>
                    ) : (
                        <>
                            {currentPage === 'dashboard' && <Dashboard onRefresh={fetchStats} />}
                            {currentPage === 'analysis' && <Analysis onAnalysisComplete={fetchStats} />}
                            {currentPage === 'reports' && <Reports />}
                            {currentPage === 'settings' && <SettingsPage />}
                        </>
                    )}
                </main>
            </div>
        </div>
    );
}
