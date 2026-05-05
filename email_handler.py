#!/usr/bin/env python3
"""
Advanced Email Handler with Multiple Templates
Production-ready email system for AutoOps AI
"""

from typing import List, Dict
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime

class EmailRequest(BaseModel):
    to_email: str
    template_type: str  # 'analysis', 'alert', 'welcome', 'digest'
    data: Dict

class EmailService:
    def __init__(self, api_key: str, from_email: str = "noreply@autoops.ai"):
        self.api_key = api_key
        self.from_email = from_email
        self.api_url = "https://api.resend.com/emails"
    
    def get_template(self, template_type: str, data: Dict) -> tuple:
        """Get email template and subject"""
        templates = {
            'analysis': self._analysis_template,
            'alert': self._alert_template,
            'welcome': self._welcome_template,
            'digest': self._digest_template,
            'scheduled': self._scheduled_template,
        }
        
        if template_type not in templates:
            raise ValueError(f"Unknown template: {template_type}")
        
        return templates[template_type](data)
    
    def _analysis_template(self, data: Dict) -> tuple:
        """Analysis report email"""
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; margin: 0; padding: 20px; }}
                    .container {{ max-width: 650px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; }}
                    .header h1 {{ margin: 0; font-size: 28px; }}
                    .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
                    .content {{ padding: 40px 30px; }}
                    .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0; }}
                    .stat-box {{ background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; }}
                    .stat-value {{ font-size: 32px; font-weight: bold; color: #667eea; margin: 10px 0 5px 0; }}
                    .stat-label {{ color: #666; font-size: 14px; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    th {{ background: #f0f0f0; padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #ddd; }}
                    td {{ padding: 12px; border-bottom: 1px solid #eee; }}
                    .insight {{ background: #e8f4f8; border-left: 4px solid #0ea5e9; padding: 15px; margin: 20px 0; border-radius: 5px; color: #0c7a9d; }}
                    .action-btn {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 20px; }}
                    .footer {{ background: #f8f9fa; padding: 20px 30px; text-align: center; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📊 AutoOps AI Analysis Report</h1>
                        <p>SaaS Cost Optimization Summary</p>
                    </div>
                    
                    <div class="content">
                        <p>Hello,</p>
                        <p>Here's your latest <strong>AutoOps AI</strong> analysis showing cost optimization opportunities:</p>
                        
                        <div class="stats">
                            <div class="stat-box">
                                <div class="stat-label">Inactive Users</div>
                                <div class="stat-value">{data.get('total_inactive', 0)}</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">Monthly Savings</div>
                                <div class="stat-value">₹{data.get('estimated_savings', 0):,}</div>
                            </div>
                        </div>
                        
                        <h3>Inactive Users Breakdown</h3>
                        <table>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Days Inactive</th>
                                <th>Cost/Month</th>
                            </tr>
                            {self._generate_user_rows(data.get('inactive_users', []))}
                        </table>
                        
                        <div class="insight">
                            <strong>💡 AI Insight:</strong> {data.get('ai_insight', 'Review inactive users for potential cost savings')}
                        </div>
                        
                        <p>Ready to optimize? Take action now:</p>
                        <a href="https://autoops.ai/dashboard" class="action-btn">Go to Dashboard</a>
                        
                        <p style="margin-top: 30px; color: #999; font-size: 13px;">
                            Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                        </p>
                    </div>
                    
                    <div class="footer">
                        <p>© 2026 AutoOps AI. All rights reserved.</p>
                        <p>You received this because you're using AutoOps AI | <a href="#">Unsubscribe</a></p>
                    </div>
                </div>
            </body>
        </html>
        """
        return "📊 Your AutoOps Analysis Report", html
    
    def _alert_template(self, data: Dict) -> tuple:
        """Alert email for threshold exceeded"""
        html = f"""
        <html>
            <body style="font-family: Arial; margin: 0; padding: 20px; background: #fff3cd;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; border-left: 5px solid #ff6b6b;">
                    <h2 style="color: #ff6b6b; margin-top: 0;">⚠️ Cost Alert</h2>
                    <p>Your inactive user costs have exceeded the threshold!</p>
                    <p><strong>Current Spending:</strong> ₹{data.get('current_cost', 0)}</p>
                    <p><strong>Threshold:</strong> ₹{data.get('threshold', 0)}</p>
                    <p><strong>Action Required:</strong> {data.get('recommendation', 'Review inactive users')}</p>
                    <a href="https://autoops.ai/dashboard" style="background: #ff6b6b; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Take Action</a>
                </div>
            </body>
        </html>
        """
        return "⚠️ Cost Alert from AutoOps AI", html
    
    def _welcome_template(self, data: Dict) -> tuple:
        """Welcome email for new users"""
        html = """
        <html>
            <body style="font-family: Arial; margin: 0; padding: 20px; background: #f0f9ff;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px;">
                    <h1 style="color: #667eea;">Welcome to AutoOps AI 🚀</h1>
                    <p>Thank you for joining us! Here's what you can do:</p>
                    <ul style="line-height: 2; color: #555;">
                        <li>✅ Analyze your inactive users</li>
                        <li>💰 Calculate monthly savings</li>
                        <li>📊 Get AI-powered recommendations</li>
                        <li>📧 Receive automated reports</li>
                        <li>🔗 Integrate with your SaaS platforms</li>
                    </ul>
                    <a href="https://autoops.ai/dashboard" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Get Started</a>
                </div>
            </body>
        </html>
        """
        return "Welcome to AutoOps AI", html
    
    def _digest_template(self, data: Dict) -> tuple:
        """Weekly/Monthly digest"""
        html = f"""
        <html>
            <body style="font-family: Arial; margin: 0; padding: 20px; background: #f5f7fa;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px;">
                    <h2>📈 Your Weekly AutoOps Summary</h2>
                    <table style="width: 100%; margin: 20px 0;">
                        <tr style="background: #f0f0f0;">
                            <td style="padding: 10px;"><strong>Total Users</strong></td>
                            <td style="padding: 10px;">{data.get('total_users', 0)}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;"><strong>Inactive</strong></td>
                            <td style="padding: 10px; color: #ff6b6b;"><strong>{data.get('inactive_count', 0)}</strong></td>
                        </tr>
                        <tr style="background: #f0f0f0;">
                            <td style="padding: 10px;"><strong>Potential Savings</strong></td>
                            <td style="padding: 10px; color: #51cf66;"><strong>₹{data.get('total_savings', 0):,}</strong></td>
                        </tr>
                    </table>
                </div>
            </body>
        </html>
        """
        return "📈 Your Weekly AutoOps Summary", html
    
    def _scheduled_template(self, data: Dict) -> tuple:
        """Scheduled report template"""
        return self._analysis_template(data)
    
    def _generate_user_rows(self, users: List[Dict]) -> str:
        """Generate HTML rows for user table"""
        rows = ""
        for user in users:
            rows += f"""
            <tr>
                <td>{user.get('name', 'N/A')}</td>
                <td>{user.get('email', 'N/A')}</td>
                <td>{user.get('days_inactive', 0)} days</td>
                <td>₹{user.get('cost', 0)}</td>
            </tr>
            """
        return rows
    
    def send_email(self, to_email: str, template_type: str, data: Dict) -> dict:
        """Send email using Resend API"""
        subject, html = self.get_template(template_type, data)
        
        payload = {
            "from": self.from_email,
            "to": to_email,
            "subject": subject,
            "html": html
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(self.api_url, json=payload, headers=headers)
        
        return {
            "success": response.status_code == 200,
            "message": response.json() if response.status_code == 200 else response.text,
            "status_code": response.status_code
        }
    
    def send_bulk_emails(self, emails: List[str], template_type: str, data: Dict) -> list:
        """Send to multiple recipients"""
        results = []
        for email in emails:
            result = self.send_email(email, template_type, data)
            results.append({"email": email, "result": result})
        return results

# Usage example
if __name__ == "__main__":
    service = EmailService(api_key="re_Ki7dzoqm_8tfHV5KBzTDeHh5P8MH5eUUL")
    
    # Send analysis email
    result = service.send_email(
        to_email="harsha17116@gmail.com",
        template_type="analysis",
        data={
            "total_inactive": 3,
            "estimated_savings": 375,
            "inactive_users": [
                {"name": "Ravi", "email": "ravi@gmail.com", "days_inactive": 854, "cost": 125},
                {"name": "Priya", "email": "priya@gmail.com", "days_inactive": 885, "cost": 125},
                {"name": "Arjun", "email": "arjun@gmail.com", "days_inactive": 749, "cost": 125},
            ],
            "ai_insight": "Remove inactive accounts, review usage monthly, enable alerts"
        }
    )
    
    print(f"Email sent: {result['success']}")
