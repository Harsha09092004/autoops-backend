from datetime import datetime

COST_PER_USER = 125


def analyze_users(users):
    inactive = []

    for user in users:
        last_login = user.get("lastLoginTime")

        if last_login:
            last_login_date = datetime.fromisoformat(last_login.replace("Z", ""))
            days = (datetime.utcnow() - last_login_date).days

            if days > 30:
                inactive.append({
                    "name": user["name"]["fullName"],
                    "email": user["primaryEmail"],
                    "days_inactive": days
                })

    total = len(inactive)
    savings = total * COST_PER_USER

    return {
        "total_inactive": total,
        "estimated_savings": savings,
        "inactive_users": inactive,
        "ai_insight": generate_ai_insight(total, savings)
    }


def generate_ai_insight(total_inactive, savings):
    if total_inactive == 0:
        return "No inactive users. Your SaaS usage is fully optimized."

    percentage = min(30, total_inactive * 2)

    return (
        f"You're losing ₹{savings:,}/month due to {total_inactive} inactive users. "
        f"Potential savings: {percentage}% reduction. "
        f"Action: Remove inactive accounts, review usage monthly, and enable inactivity alerts."
    )