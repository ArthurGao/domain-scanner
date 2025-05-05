# scripts/generate_system_token.py
import os
import sys

from app.core.security.security import create_access_token

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

token = create_access_token(
    data={
        "type": "system",
        "purpose": "data-sync"
    },
    expires_delta=30 * 60
)

print("Generated system token:\n")
print(token)