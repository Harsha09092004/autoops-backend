from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://lenofuxujkpowguukvdv.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_secret_OVc-jE_KA8-UchpMKtPAyw_IRbSdZt2")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------AUDIT REPORTS TABLE ----------------
def insert_audit_report(user_email, total_inactive, estimated_savings, ai_insight):
    """Insert analysis report into audit_reports table"""
    try:
        data = {
            "user_email": user_email,
            "total_inactive": total_inactive,
            "estimated_savings": estimated_savings,
            "ai_insight": ai_insight,
            "created_at": None  # Supabase will auto-set to current timestamp
        }
        result = supabase.table("audit_reports").insert(data).execute()
        return result.data
    except Exception as e:
        print(f"Error inserting audit report: {e}")
        return None

def get_audit_reports(limit=50):
    """Get recent audit reports"""
    try:
        result = supabase.table("audit_reports").select("*").order("created_at", desc=True).limit(limit).execute()
        return result.data
    except Exception as e:
        print(f"Error fetching audit reports: {e}")
        return []

def get_user_audit_history(email):
    """Get audit history for a specific user"""
    try:
        result = supabase.table("audit_reports").select("*").eq("user_email", email).order("created_at", desc=True).execute()
        return result.data
    except Exception as e:
        print(f"Error fetching user history: {e}")
        return []

def delete_audit_report(report_id):
    """Delete a specific audit report"""
    try:
        result = supabase.table("audit_reports").delete().eq("id", report_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting report: {e}")
        return False

# ----------------INACTIVE USERS TABLE ----------------
def save_inactive_user(user_email, name, days_inactive, company_email):
    """Save inactive user to tracking table"""
    try:
        data = {
            "user_email": user_email,
            "name": name,
            "days_inactive": days_inactive,
            "company_email": company_email,
            "flagged_at": None,
            "status": "inactive"
        }
        result = supabase.table("inactive_users").insert(data).execute()
        return result.data
    except Exception as e:
        print(f"Error saving inactive user: {e}")
        return None

def get_inactive_users():
    """Get all flagged inactive users"""
    try:
        result = supabase.table("inactive_users").select("*").eq("status", "inactive").execute()
        return result.data
    except Exception as e:
        print(f"Error fetching inactive users: {e}")
        return []

def update_inactive_user_status(user_id, status):
    """Update status of inactive user (e.g., 'removed', 'contacted')"""
    try:
        result = supabase.table("inactive_users").update({"status": status}).eq("id", user_id).execute()
        return True
    except Exception as e:
        print(f"Error updating user status: {e}")
        return False

# ----------------COMPANIES TABLE ----------------
def create_company(company_name, email, admin_email):
    """Register a new company"""
    try:
        data = {
            "company_name": company_name,
            "email": email,
            "admin_email": admin_email,
            "subscription_tier": "free",
            "active": True
        }
        result = supabase.table("companies").insert(data).execute()
        return result.data
    except Exception as e:
        print(f"Error creating company: {e}")
        return None

def get_company(company_id):
    """Get company details"""
    try:
        result = supabase.table("companies").select("*").eq("id", company_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error fetching company: {e}")
        return None

def update_company_subscription(company_id, tier):
    """Update company subscription tier"""
    try:
        result = supabase.table("companies").update({"subscription_tier": tier}).eq("id", company_id).execute()
        return True
    except Exception as e:
        print(f"Error updating company: {e}")
        return False

# ----------------ANALYTICS TABLE ----------------
def log_analytics(company_id, event_type, event_data):
    """Log analytics events"""
    try:
        data = {
            "company_id": company_id,
            "event_type": event_type,
            "event_data": event_data,
            "timestamp": None
        }
        result = supabase.table("analytics").insert(data).execute()
        return result.data
    except Exception as e:
        print(f"Error logging analytics: {e}")
        return None

# ----------------HEALTH CHECK ----------------
def check_supabase_connection():
    """Check if Supabase connection is working"""
    try:
        result = supabase.table("audit_reports").select("*").limit(1).execute()
        return True
    except Exception as e:
        print(f"Supabase connection error: {e}")
        return False
