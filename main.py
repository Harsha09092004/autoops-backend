from fastapi import HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from analyzer import analyze_users
from supabase_client import supabase
from google_service import get_google_users

# PDF imports
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

# Utility imports
import json
from datetime import datetime
import requests

load_dotenv()

app = FastAPI()

# ----------------CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------HOME ----------------
@app.get("/")
def home():
    return {"message": "AutoOps AI running 🚀", "version": "2.0"}

# ----------------MOCK USERS ----------------
def get_mock_users():
    return [
        {
            "name": {"fullName": "Ravi"},
            "primaryEmail": "ravi@gmail.com",
            "lastLoginTime": "2024-01-01T10:00:00Z"
        },
        {
            "name": {"fullName": "Priya"},
            "primaryEmail": "priya@gmail.com",
            "lastLoginTime": "2023-12-01T10:00:00Z"
        },
        {
            "name": {"fullName": "Arjun"},
            "primaryEmail": "arjun@gmail.com",
            "lastLoginTime": "2024-04-15T10:00:00Z"
        }
    ]

# ----------------STORE REPORT (JSON) ----------------
def save_report(data):
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }

    try:
        with open("reports.json", "r") as f:
            reports = json.load(f)
    except:
        reports = []

    reports.append(report)

    with open("reports.json", "w") as f:
        json.dump(reports, f, indent=2)

# ----------------SAVE TO SUPABASE ----------------
def save_to_supabase(email, analysis_data):
    data = {
        "user_email": email,
        "total_inactive": analysis_data['total_inactive'],
        "estimated_savings": analysis_data['estimated_savings'],
        "ai_insight": analysis_data['ai_insight'],
        "created_at": datetime.utcnow().isoformat()
    }

    try:
        supabase.table("audit_reports").insert(data).execute()
        return True
    except Exception as e:
        print(f"Supabase Error: {e}")
        return False

# ----------------ANALYZE ----------------
@app.get("/analyze")
def analyze():
    users = get_mock_users()
    data = analyze_users(users)
    save_report(data)
    return data

# ----------------ANALYZE WITH EMAIL ----------------
@app.get("/analyze-email/{email}")
def analyze_with_email(email: str):
    users = get_mock_users()
    data = analyze_users(users)
    
    save_report(data)
    save_to_supabase(email, data)
    
    try:
        send_email_report(email, data)
        return {"message": "Analysis sent to email", "data": data, "email_sent": True}
    except Exception as e:
        return {"message": "Analysis complete but email failed", "data": data, "email_sent": False, "error": str(e)}

# ----------------GET REPORT HISTORY (JSON) ----------------
@app.get("/reports")
def get_reports():
    try:
        with open("reports.json", "r") as f:
            return json.load(f)
    except:
        return []

# ----------------GET SUPABASE REPORTS ----------------
@app.get("/reports-supabase")
def get_supabase_reports():
    try:
        response = supabase.table("audit_reports").select("*").order("created_at", desc=True).limit(50).execute()
        return response.data
    except Exception as e:
        return {"error": str(e), "data": []}

# ----------------PDF GENERATION ----------------
def generate_pdf(data):
    file_path = "report.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AutoOps AI Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Total Inactive Users: {data['total_inactive']}", styles["Heading2"]))
    content.append(Paragraph(f"Estimated Savings: ₹{data['estimated_savings']:,}/month", styles["Heading2"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("AI Insight:", styles["Heading3"]))
    content.append(Paragraph(data["ai_insight"], styles["Normal"]))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Inactive Users Details:", styles["Heading3"]))
    
    # Create table for users
    user_table_data = [["Name", "Email", "Days Inactive"]]
    for user in data["inactive_users"]:
        user_table_data.append([
            user['name'],
            user['email'],
            str(user['days_inactive'])
        ])

    user_table = Table(user_table_data)
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    content.append(user_table)
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Report Generated: {datetime.utcnow().isoformat()}", styles["Normal"]))

    doc.build(content)

    return file_path

# ----------------EXPORT PDF ----------------
@app.get("/export")
def export_report():
    users = get_mock_users()
    data = analyze_users(users)

    file_path = generate_pdf(data)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="AutoOps_Report.pdf"
    )

# ----------------REQUEST MODELS ----------------
class EmailRequest(BaseModel):
    email: str

class GoogleAuthRequest(BaseModel):
    access_token: str

# ----------------EMAIL FUNCTION ----------------
def send_email_report(to_email, data):
    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": os.getenv("RESEND_API_KEY", "re_Ki7dzoqm_8tfHV5KBzTDeHh5P8MH5eUUL"),
        "Content-Type": "application/json"
    }

    inactive_users_html = "<tr><th>Name</th><th>Email</th><th>Days Inactive</th></tr>"
    for user in data['inactive_users']:
        inactive_users_html += f"<tr><td>{user['name']}</td><td>{user['email']}</td><td>{user['days_inactive']}</td></tr>"

    payload = {
        "from": "noreply@autoops.dev",
        "to": [to_email],
        "subject": "AutoOps AI Analysis Report",
        "html": f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>AutoOps AI Analysis Report</h2>
                <p><strong>Total Inactive Users:</strong> {data['total_inactive']}</p>
                <p><strong>Estimated Savings:</strong> ₹{data['estimated_savings']:,}/month</p>
                <p><strong>AI Insight:</strong> {data['ai_insight']}</p>
                <h3>Inactive Users:</h3>
                <table border="1" cellpadding="10" cellspacing="0">
                    {inactive_users_html}
                </table>
                <p style="margin-top: 20px; color: #999; font-size: 12px;">Generated on {datetime.utcnow().isoformat()}</p>
            </body>
        </html>
        """
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code not in [200, 202]:
        print("Resend Error:", response.text)
        raise Exception("Email failed to send")
    
    return True

# ----------------EMAIL API ----------------
@app.post("/send-email")
def email_report(request: EmailRequest):
    users = get_mock_users()
    data = analyze_users(users)

    try:
        send_email_report(request.email, data)
        save_to_supabase(request.email, data)
        return {"message": "Email sent successfully", "data": data}
    except Exception as e:
        print("EMAIL ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# ----------------GOOGLE USERS ENDPOINT ----------------
@app.post("/google-users")
def fetch_google_users(request: GoogleAuthRequest):
    try:
        users = get_google_users(request.access_token)
        data = analyze_users(users)
        save_report(data)
        return {"message": "Google users analyzed", "data": data, "user_count": len(users)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google API Error: {str(e)}")

# ----------------HEALTH CHECK ----------------
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "running",
            "supabase": "connected",
            "email": "ready"
        }
    }

# ----------------STATS ENDPOINT ----------------
@app.get("/stats")
def get_stats():
    reports = get_reports()
    supabase_reports = []
    try:
        response = supabase.table("audit_reports").select("*").execute()
        supabase_reports = response.data
    except:
        pass

    return {
        "total_json_reports": len(reports),
        "total_supabase_reports": len(supabase_reports),
        "last_analysis": reports[-1]["timestamp"] if reports else None
    }

# ----------------CLEAR REPORTS ----------------
@app.delete("/reports")
def clear_reports():
    try:
        with open("reports.json", "w") as f:
            json.dump([], f)
        return {"message": "Reports cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
