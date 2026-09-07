# HANTRIX Inventory Management System

## Backend

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

The API runs on `http://0.0.0.0:8000`. From another device, use the Windows host LAN address, not `0.0.0.0`.

## Frontend

The Flutter app currently expects the backend at `http://192.168.76.43:8000`. Update the address in `frontend/lib/core/api/api_client.dart` and the IoT services if the backend computer receives a different LAN IP.

```powershell
cd frontend
flutter pub get
flutter run
```

The Raspberry Pi address is `192.168.76.232`; it should send data to the backend computer's LAN address. Both devices must be connected to the same network, and the backend computer's firewall must allow TCP port `8000`.
