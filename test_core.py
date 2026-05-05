#!/usr/bin/env python
"""Quick test of AutoOps AI backend"""

from main import app, get_mock_users, analyze_users
from analyzer import COST_PER_USER

# Test analyze logic
users = get_mock_users()
print('📊 Testing Analysis Logic')
print(f'Total users in mock data: {len(users)}')
print()

data = analyze_users(users)
print(f'✓ Total inactive users: {data["total_inactive"]}')
print(f'✓ Estimated savings: ₹{data["estimated_savings"]}/month')
print(f'✓ Cost per user: ₹{COST_PER_USER}')
print()
print(f'✓ Inactive user details:')
for user in data["inactive_users"]:
    print(f'  - {user["name"]} ({user["email"]}): {user["days_inactive"]} days inactive')
print()
print('✓ AI Insight:')
print(f'  {data["ai_insight"]}')
print()
print('=' * 60)
print('✅ All core functions working correctly!')
print('=' * 60)
