#!/usr/bin/env python3
"""
Multi-Core Processing & Scaling Architecture
Background job processing with Celery + Redis
"""

from celery import Celery, group, chord
from celery.utils.log import get_task_logger
from typing import List, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time

# Initialize Celery
app = Celery(
    'autoops',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['autoops_tasks']
)

# Configure Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

logger = get_task_logger(__name__)

# ============= BACKGROUND TASKS =============

@app.task(bind=True, max_retries=3)
def analyze_company_task(self, company_id: int):
    """Analyze single company - runs in background"""
    try:
        logger.info(f"Analyzing company {company_id}")
        
        # Import here to avoid circular imports
        from analyzer import analyze_users
        from supabase_client import get_company_users, insert_audit_report, save_inactive_users
        
        # Get users
        users = get_company_users(company_id)
        
        # Analyze
        result = analyze_users(users)
        
        # Save results
        insert_audit_report(
            user_email=f"company_{company_id}",
            total_inactive=result['total_inactive'],
            estimated_savings=result['estimated_savings'],
            ai_insight=result['ai_insight']
        )
        
        # Save inactive users
        for user in result['inactive_users']:
            save_inactive_users(
                user_email=user['email'],
                name=user['name'],
                days_inactive=user['days_inactive'],
                company_email=f"company_{company_id}"
            )
        
        return {
            "company_id": company_id,
            "status": "success",
            "result": result
        }
    
    except Exception as exc:
        logger.error(f"Error analyzing company {company_id}: {exc}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * 2 ** self.request.retries)

@app.task(bind=True)
def send_email_task(self, to_email: str, template_type: str, data: dict):
    """Send email - async task"""
    try:
        logger.info(f"Sending email to {to_email}")
        from email_handler import EmailService
        from dotenv import dotenv_values
        
        config = dotenv_values(".env")
        service = EmailService(api_key=config.get("RESEND_API_KEY"))
        
        result = service.send_email(to_email, template_type, data)
        
        return {
            "email": to_email,
            "status": "success" if result['success'] else "failed",
            "message": result.get('message')
        }
    
    except Exception as exc:
        logger.error(f"Error sending email: {exc}")
        raise self.retry(exc=exc, countdown=300)

@app.task(bind=True)
def export_pdf_task(self, company_id: int, data: dict):
    """Generate PDF - async task"""
    try:
        logger.info(f"Generating PDF for company {company_id}")
        from main import generate_pdf
        import uuid
        
        filename = f"report_{company_id}_{uuid.uuid4()}.pdf"
        pdf_path = f"/reports/{filename}"
        
        generate_pdf(data)
        
        return {
            "company_id": company_id,
            "pdf_path": pdf_path,
            "status": "success"
        }
    
    except Exception as exc:
        logger.error(f"Error generating PDF: {exc}")
        raise self.retry(exc=exc, countdown=300)

# ============= BATCH PROCESSING =============

class BatchProcessor:
    """Process multiple analyses in parallel"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    def analyze_batch_async(self, company_ids: List[int]) -> dict:
        """Process multiple companies asynchronously with Celery"""
        # Create group of tasks
        job = group(
            analyze_company_task.s(company_id) 
            for company_id in company_ids
        )
        
        # Execute group
        result = job.apply_async()
        
        return {
            "job_id": result.id,
            "status": "processing",
            "companies": company_ids,
            "total": len(company_ids)
        }
    
    def analyze_batch_concurrent(self, company_ids: List[int]) -> list:
        """Process using ThreadPoolExecutor (CPU-bound)"""
        from analyzer import analyze_users
        from supabase_client import get_company_users
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._analyze_single, company_id): company_id
                for company_id in company_ids
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    company_id = futures[future]
                    results.append({
                        "company_id": company_id,
                        "error": str(exc),
                        "status": "failed"
                    })
        
        return results
    
    def _analyze_single(self, company_id: int) -> dict:
        """Analyze single company"""
        from analyzer import analyze_users
        from supabase_client import get_company_users, insert_audit_report
        
        try:
            users = get_company_users(company_id)
            result = analyze_users(users)
            
            insert_audit_report(
                user_email=f"company_{company_id}",
                total_inactive=result['total_inactive'],
                estimated_savings=result['estimated_savings'],
                ai_insight=result['ai_insight']
            )
            
            return {
                "company_id": company_id,
                "status": "success",
                "total_inactive": result['total_inactive'],
                "savings": result['estimated_savings']
            }
        except Exception as e:
            return {
                "company_id": company_id,
                "status": "error",
                "error": str(e)
            }

# ============= SCHEDULED TASKS =============

from celery.schedules import crontab

app.conf.beat_schedule = {
    # Run analysis every Monday at 9 AM
    'analyze-weekly': {
        'task': 'analyze_scheduled_task',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),
        'args': ()
    },
    # Send digest reports every Friday
    'digest-weekly': {
        'task': 'send_digest_task',
        'schedule': crontab(hour=10, minute=0, day_of_week=5),
        'args': ()
    },
    # Check for alerts every 6 hours
    'check-alerts': {
        'task': 'check_cost_alerts_task',
        'schedule': 21600.0,  # 6 hours in seconds
        'args': ()
    },
}

@app.task
def analyze_scheduled_task():
    """Run weekly analysis for all companies"""
    logger.info("Starting scheduled analysis")
    from supabase_client import get_all_companies
    
    companies = get_all_companies()
    batch = BatchProcessor()
    
    result = batch.analyze_batch_async([c['id'] for c in companies])
    logger.info(f"Scheduled analysis started: {result}")
    
    return result

@app.task
def send_digest_task():
    """Send weekly digest to all users"""
    logger.info("Sending weekly digests")
    from supabase_client import get_all_subscriptions
    
    subscriptions = get_all_subscriptions()
    
    for sub in subscriptions:
        if sub['frequency'] == 'weekly':
            send_email_task.delay(
                to_email=sub['email'],
                template_type='digest',
                data=sub['data']
            )
    
    return {"status": "digests_sent", "count": len(subscriptions)}

@app.task
def check_cost_alerts_task():
    """Check if any costs exceeded thresholds"""
    logger.info("Checking cost alerts")
    from supabase_client import get_all_companies
    
    companies = get_all_companies()
    alerts_sent = 0
    
    for company in companies:
        if company['current_cost'] > company['cost_threshold']:
            send_email_task.delay(
                to_email=company['admin_email'],
                template_type='alert',
                data={
                    'current_cost': company['current_cost'],
                    'threshold': company['cost_threshold'],
                    'recommendation': 'Review and archive inactive users'
                }
            )
            alerts_sent += 1
    
    return {"status": "alerts_checked", "sent": alerts_sent}

# ============= CHAIN & WORKFLOW =============

def create_analysis_workflow(company_id: int, send_email_to: str = None):
    """
    Create a workflow:
    1. Analyze company
    2. Generate PDF
    3. Send email
    """
    from celery import chain, chord
    
    # Define tasks
    workflow = chord(
        [analyze_company_task.s(company_id)],
        export_pdf_task.s(company_id) | send_email_task.s(send_email_to, 'analysis')
    )
    
    return workflow.apply_async()

# ============= MONITORING =============

@app.task
def get_task_status(task_id: str):
    """Get status of a task"""
    from celery.result import AsyncResult
    
    result = AsyncResult(task_id, app=app)
    
    return {
        "task_id": task_id,
        "state": result.state,
        "result": result.result if result.ready() else "pending",
        "progress": result.info.get('progress', 0) if result.info else 0
    }

# ============= USAGE IN MAIN API =============

"""
# Add to main.py:

from celery_config import app, analyze_company_task, send_email_task, BatchProcessor

@app.post("/analyze-async")
async def analyze_async(company_id: int):
    '''Non-blocking analysis'''
    task = analyze_company_task.delay(company_id)
    return {
        "task_id": task.id,
        "status": "processing",
        "check_url": f"/tasks/{task.id}"
    }

@app.post("/batch-analyze")
async def batch_analyze(company_ids: List[int]):
    '''Analyze multiple companies'''
    batch = BatchProcessor()
    result = batch.analyze_batch_async(company_ids)
    return result

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    '''Get task status'''
    from celery_config import get_task_status
    return get_task_status(task_id)
"""

if __name__ == "__main__":
    print("Celery worker started")
    print("Run with: celery -A celery_config worker --loglevel=info")
