# HANTRIX Inventory Management System

## Backend

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

The API listens on port `8000`. For a shared deployment, host this FastAPI service on a server with a stable HTTPS URL. Supabase can provide the shared PostgreSQL database, but it does not host this FastAPI service.

Copy `.env.example` to `.env` and set `DATABASE_URL` to the Supabase PostgreSQL connection string. Never commit `.env`.

## Frontend

```powershell
cd frontend
flutter pub get
flutter run --dart-define=API_BASE_URL=http://127.0.0.1:8000
```

For a phone, Pi, or contributor on another computer, pass the stable backend URL instead:

```powershell
flutter run --dart-define=API_BASE_URL=https://api.example.com
```

The Raspberry Pi should send data to that same stable backend URL. Its local IP can change without requiring a Flutter source-code edit. For temporary local testing, use the backend computer's current LAN address as `API_BASE_URL`; both devices must be on the same network and port `8000` must be allowed through the firewall.
