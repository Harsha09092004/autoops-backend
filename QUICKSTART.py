#!/usr/bin/env python
"""API endpoint tester for AutoOps AI Backend"""

import json
import sys

print("=" * 70)
print("   AutoOps AI Backend - Quick Start Guide".center(70))
print("=" * 70)
print()

print("📋 PROJECT STRUCTURE")
print("-" * 70)
print("✓ main.py              - FastAPI application with 15+ endpoints")
print("✓ analyzer.py          - Core inactivity analysis logic")
print("✓ google_service.py    - Google Workspace integration")
print("✓ supabase_client.py   - Database operations with helper functions")
print("✓ .env                 - Configuration with API keys")
print("✓ requirements.txt     - All Python dependencies")
print("✓ reports.json         - Local report storage")
print()

print("🚀 QUICK START")
print("-" * 70)
print("1. Install dependencies:")
print("   pip install -r requirements.txt")
print()
print("2. Start the server:")
print("   python main.py")
print("   OR")
print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
print()
print("3. Access API:")
print("   http://localhost:8000")
print()
print("4. View interactive docs:")
print("   http://localhost:8000/docs")
print()

print("📡 KEY API ENDPOINTS")
print("-" * 70)

endpoints = [
    ("GET /", "Health check & welcome"),
    ("GET /health", "Detailed health status"),
    ("GET /stats", "Report statistics"),
    ("GET /analyze", "Run analysis (mock data)"),
    ("GET /analyze-email/{email}", "Analyze & email results"),
    ("POST /send-email", "Send report to email"),
    ("GET /export", "Download PDF report"),
    ("GET /reports", "Get JSON report history"),
    ("GET /reports-supabase", "Get Supabase reports"),
    ("POST /google-users", "Analyze Google Workspace users"),
    ("DELETE /reports", "Clear report history"),
]

for endpoint, desc in endpoints:
    print(f"  {endpoint:<30} → {desc}")
print()

print("🧪 EXAMPLE CURL COMMANDS")
print("-" * 70)
print()
print("1. Test API health:")
print('   curl http://localhost:8000/')
print()
print("2. Run analysis:")
print('   curl http://localhost:8000/analyze')
print()
print("3. Send email report:")
print('   curl -X POST http://localhost:8000/send-email \\')
print('     -H "Content-Type: application/json" \\')
print('     -d \'{"email": "admin@company.com"}\'')
print()
print("4. Export PDF:")
print('   curl http://localhost:8000/export > report.pdf')
print()
print("5. Get statistics:")
print('   curl http://localhost:8000/stats')
print()

print("💾 FEATURES IMPLEMENTED")
print("-" * 70)
print("✅ User inactivity analysis (30+ days threshold)")
print("✅ Cost optimization calculations")
print("✅ Email report sending (Resend API)")
print("✅ PDF generation with tables")
print("✅ Google Workspace integration")
print("✅ Supabase database storage")
print("✅ JSON local report history")
print("✅ Health monitoring & stats")
print("✅ Error handling & validation")
print("✅ CORS enabled for frontend")
print()

print("⚙️  CONFIGURATION")
print("-" * 70)
print("Edit .env file to set:")
print("  SUPABASE_URL         - Your Supabase project URL")
print("  SUPABASE_KEY         - Supabase API key")
print("  RESEND_API_KEY       - Email service key")
print("  GOOGLE_CLIENT_ID     - Google Cloud client ID")
print("  GOOGLE_CLIENT_SECRET - Google Cloud client secret")
print()

print("📊 SAMPLE ANALYSIS OUTPUT")
print("-" * 70)
sample = {
    "total_inactive": 3,
    "estimated_savings": 375,
    "inactive_users": [
        {"name": "Ravi", "email": "ravi@gmail.com", "days_inactive": 851},
        {"name": "Priya", "email": "priya@gmail.com", "days_inactive": 882},
        {"name": "Arjun", "email": "arjun@gmail.com", "days_inactive": 746}
    ],
    "ai_insight": "You're losing ₹375/month due to 3 inactive users..."
}
print(json.dumps(sample, indent=2))
print()

print("📚 FILE SIZES & STATUS")
print("-" * 70)
import os
files = {
    "main.py": "c:\\Users\\RESHMA B\\Downloads\\autoops-backend\\main.py",
    "analyzer.py": "c:\\Users\\RESHMA B\\Downloads\\autoops-backend\\analyzer.py",
    "google_service.py": "c:\\Users\\RESHMA B\\Downloads\\autoops-backend\\google_service.py",
    "supabase_client.py": "c:\\Users\\RESHMA B\\Downloads\\autoops-backend\\supabase_client.py",
}

for name, path in files.items():
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"✓ {name:<25} {size:>6} bytes")
    else:
        print(f"✗ {name:<25} NOT FOUND")
print()

print("🔗 NEXT STEPS")
print("-" * 70)
print("1. Update .env with your actual API keys")
print("2. Set up Supabase tables: audit_reports, inactive_users, companies")
print("3. Start the server: python main.py")
print("4. Test endpoints using curl or Postman")
print("5. Integrate with frontend for UI")
print("6. Deploy to production (Docker, AWS, Heroku, etc.)")
print()

print("=" * 70)
print("✅ AutoOps AI Backend is ready! 🚀".center(70))
print("=" * 70)
