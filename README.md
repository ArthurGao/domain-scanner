```bash
pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
docker-compose up -d
```

```bash
 uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
PYTHONPATH=. python scripts/create_admin_user.py
```