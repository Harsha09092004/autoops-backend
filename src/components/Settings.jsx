import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Server, Database, Mail, Bell, Shield } from 'lucide-react';
import { apiService } from '../api';

export default function Settings() {
    const [health, setHealth] = useState(null);
    const [loading, setLoading] = useState(true);
    const [settings, setSettings] = useState({
        costPerUser: 125,
        inactivityDays: 30,
        emailNotifications: true,
        autoArchive: false,
    });

    useEffect(() => {
        fetchHealth();
    }, []);

    const fetchHealth = async () => {
        setLoading(true);
        try {
            const response = await apiService.getHealth();
            setHealth(response.data);
        } catch (error) {
            console.error('Error fetching health:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSettingChange = (key, value) => {
        setSettings(prev => ({
            ...prev,
            [key]: value
        }));
    };

    const handleSaveSettings = () => {
        // Save to localStorage or API
        localStorage.setItem('autoops-settings', JSON.stringify(settings));
        alert('✅ Settings saved successfully!');
    };

    return (
        <div className="space-y-6 fade-in">
            {/* System Health */}
            {health && (
                <div className="card">
                    <div className="flex items-center gap-3 mb-6">
                        <Server className="w-6 h-6 text-blue-400" />
                        <h3 className="text-xl font-semibold text-white">System Health</h3>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Status */}
                        <div className="bg-slate-700/50 rounded-lg p-4">
                            <p className="text-slate-400 text-sm mb-2">API Status</p>
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                                <p className="text-white font-semibold capitalize">{health.status}</p>
                            </div>
                        </div>

                        {/* Last Update */}
                        <div className="bg-slate-700/50 rounded-lg p-4">
                            <p className="text-slate-400 text-sm mb-2">Last Updated</p>
                            <p className="text-white font-semibold">
                                {new Date(health.timestamp).toLocaleTimeString()}
                            </p>
                        </div>

                        {/* Services */}
                        <div className="bg-slate-700/50 rounded-lg p-4">
                            <p className="text-slate-400 text-sm mb-2">Services</p>
                            <div className="space-y-1">
                                {Object.entries(health.services || {}).map(([key, value]) => (
                                    <div key={key} className="flex items-center justify-between text-sm">
                                        <span className="text-slate-300 capitalize">{key}</span>
                                        <span className={`font-semibold ${value === 'running' || value === 'connected' || value === 'ready' ? 'text-green-400' : 'text-red-400'}`}>
                                            {value}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Application Settings */}
            <div className="card">
                <div className="flex items-center gap-3 mb-6">
                    <SettingsIcon className="w-6 h-6 text-purple-400" />
                    <h3 className="text-xl font-semibold text-white">Application Settings</h3>
                </div>

                <div className="space-y-6">
                    {/* Cost Per User */}
                    <div>
                        <label className="block text-white font-medium mb-2">Cost Per User (Monthly in ₹)</label>
                        <input
                            type="number"
                            value={settings.costPerUser}
                            onChange={(e) => handleSettingChange('costPerUser', Number(e.target.value))}
                            className="input-field"
                        />
                        <p className="text-slate-400 text-sm mt-2">Cost per inactive user per month</p>
                    </div>

                    {/* Inactivity Threshold */}
                    <div>
                        <label className="block text-white font-medium mb-2">Inactivity Threshold (Days)</label>
                        <input
                            type="number"
                            value={settings.inactivityDays}
                            onChange={(e) => handleSettingChange('inactivityDays', Number(e.target.value))}
                            className="input-field"
                        />
                        <p className="text-slate-400 text-sm mt-2">Days without login to mark as inactive</p>
                    </div>

                    {/* Email Notifications */}
                    <div>
                        <label className="flex items-center gap-3 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={settings.emailNotifications}
                                onChange={(e) => handleSettingChange('emailNotifications', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-600 bg-slate-700"
                            />
                            <span className="text-white font-medium">Email Notifications</span>
                        </label>
                        <p className="text-slate-400 text-sm mt-2 ml-8">Receive email updates on analysis</p>
                    </div>

                    {/* Auto Archive */}
                    <div>
                        <label className="flex items-center gap-3 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={settings.autoArchive}
                                onChange={(e) => handleSettingChange('autoArchive', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-600 bg-slate-700"
                            />
                            <span className="text-white font-medium">Auto Archive Old Reports</span>
                        </label>
                        <p className="text-slate-400 text-sm mt-2 ml-8">Automatically archive reports older than 30 days</p>
                    </div>

                    <button
                        onClick={handleSaveSettings}
                        className="btn-primary w-full mt-6"
                    >
                        Save Settings
                    </button>
                </div>
            </div>

            {/* API Configuration */}
            <div className="card">
                <div className="flex items-center gap-3 mb-6">
                    <Database className="w-6 h-6 text-green-400" />
                    <h3 className="text-xl font-semibold text-white">API Configuration</h3>
                </div>

                <div className="space-y-4">
                    <div>
                        <p className="text-slate-400 text-sm mb-1">Backend API</p>
                        <div className="bg-slate-700 rounded p-3 font-mono text-sm text-slate-300 break-all">
                            http://localhost:8000
                        </div>
                    </div>
                    <div>
                        <p className="text-slate-400 text-sm mb-1">API Documentation</p>
                        <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
                            http://localhost:8000/docs →
                        </a>
                    </div>
                </div>
            </div>

            {/* Info Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card">
                    <Mail className="w-8 h-8 text-blue-400 mb-3" />
                    <h4 className="font-semibold text-white mb-2">Email Integration</h4>
                    <p className="text-slate-400 text-sm">Send analysis reports via email using Resend API</p>
                </div>

                <div className="card">
                    <Database className="w-8 h-8 text-green-400 mb-3" />
                    <h4 className="font-semibold text-white mb-2">Database</h4>
                    <p className="text-slate-400 text-sm">Supabase integration for persistent data storage</p>
                </div>

                <div className="card">
                    <Shield className="w-8 h-8 text-purple-400 mb-3" />
                    <h4 className="font-semibold text-white mb-2">Security</h4>
                    <p className="text-slate-400 text-sm">CORS enabled for secure frontend communication</p>
                </div>
            </div>

            {/* Version Info */}
            <div className="card bg-slate-700/30 border-slate-600">
                <p className="text-slate-400 text-sm">AutoOps AI Frontend v1.0.0</p>
                <p className="text-slate-500 text-xs mt-2">© 2026 AutoOps AI. All rights reserved.</p>
            </div>
        </div>
    );
}
