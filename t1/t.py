import requests

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzcwMTQ0Nzk4fQ.Ml_PY5canoW6XTwkzRlqaDdW5kf12hRcrl7Imhvynsc"}

req = requests.get("http://127.0.0.1:8001/auth/refresh", headers=headers)
print(req)
print(req.json())