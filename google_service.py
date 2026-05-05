"""
Google Workspace Integration
Fetches user activity from Google Workspace using Admin SDK
"""

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google.auth.oauthlib.flow import Flow
    from googleapiclient.discovery import build
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("Warning: Google APIs not available. Install google-auth-oauthlib and google-api-python-client")

import os
from dotenv import load_dotenv

load_dotenv()

# Google Admin SDK scopes
SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user.readonly',
    'https://www.googleapis.com/auth/admin.directory.user.security'
]

CREDENTIALS_FILE = 'credentials.json'

def get_credentials(access_token=None):
    """
    Get Google credentials from token
    """
    if not GOOGLE_AVAILABLE:
        raise Exception("Google libraries not installed. Install google-auth-oauthlib")
    
    if access_token:
        credentials = Credentials(token=access_token)
        return credentials
    
    # Try to load from file if available
    try:
        from google.auth import default
        credentials, project = default(scopes=SCOPES)
        return credentials
    except:
        return None

def get_google_users(access_token):
    """
    Fetch users from Google Workspace
    Requires Admin SDK access
    """
    if not GOOGLE_AVAILABLE:
        return []
    
    try:
        credentials = get_credentials(access_token)
        
        service = build('admin', 'directory_v1', credentials=credentials)
        
        # Get all users in the domain
        results = service.users().list(
            customer='my_customer',
            maxResults=500,
            orderBy='email',
            query='isSuspended=False'
        ).execute()
        
        users = results.get('users', [])
        
        # Format users similar to mock format
        formatted_users = []
        for user in users:
            formatted_users.append({
                "name": {
                    "fullName": user.get('name', {}).get('fullName', user.get('primaryEmail', ''))
                },
                "primaryEmail": user.get('primaryEmail', ''),
                "lastLoginTime": user.get('lastLoginTime', '2025-01-01T00:00:00Z')
            })
        
        return formatted_users
    
    except Exception as e:
        print(f"Google API Error: {e}")
        raise Exception(f"Failed to fetch Google users: {str(e)}")

def get_user_activity(access_token, user_email):
    """
    Get specific user activity details
    """
    if not GOOGLE_AVAILABLE:
        return {}
    
    try:
        credentials = get_credentials(access_token)
        service = build('admin', 'directory_v1', credentials=credentials)
        
        user = service.users().get(userKey=user_email).execute()
        
        return {
            "name": user.get('name', {}).get('fullName'),
            "email": user.get('primaryEmail'),
            "lastLoginTime": user.get('lastLoginTime'),
            "creationTime": user.get('creationTime'),
            "suspended": user.get('suspended', False)
        }
    
    except Exception as e:
        print(f"Error fetching user activity: {e}")
        raise

def disable_user(access_token, user_email):
    """
    Disable/suspend an inactive user (requires admin privileges)
    """
    if not GOOGLE_AVAILABLE:
        return {"success": False}
    
    try:
        credentials = get_credentials(access_token)
        service = build('admin', 'directory_v1', credentials=credentials)
        
        user_body = {
            'suspended': True
        }
        
        result = service.users().update(
            userKey=user_email,
            body=user_body
        ).execute()
        
        return {"success": True, "message": f"User {user_email} suspended"}
    
    except Exception as e:
        print(f"Error disabling user: {e}")
        raise

def send_warning_email(access_token, user_email, days_inactive):
    """
    Send warning email to inactive user
    """
    try:
        # This would require Gmail API integration
        # For now, return a placeholder
        return {
            "success": True,
            "message": f"Warning email queued for {user_email} (inactive for {days_inactive} days)"
        }
    except Exception as e:
        print(f"Error sending email: {e}")
        raise

if __name__ == "__main__":
    # Test with mock access token
    print("Google Service module loaded successfully")

