# BloodID

BloodID is a mobile-first prototype for AI-assisted blood group prediction from fingerprint images. The project combines a React Native/Expo mobile app with a FastAPI backend, offering user authentication, fingerprint analysis, prediction history, and personalized settings.

## Project overview

This application is designed as an experimental healthcare demo. It allows users to:

- create an account or sign in
- upload or capture a fingerprint image
- request a blood group prediction through the backend API
- review prediction confidence and probability breakdown
- revisit previous results from a history screen
- configure account preferences and learning content

The current implementation uses a mock inference pipeline rather than a production-trained ML model, which is clearly reflected in the backend logic and API responses.

## Architecture

### Mobile app

The frontend lives in the `mobile/` folder and is built with:

- Expo
- React Native
- Expo Router
- Zustand for state management
- Native UI components and theme tokens

Key screens include:

- splash screen
- login and registration
- dashboard/home
- prediction capture flow
- history screen
- learning tips and educational content
- profile and settings

### Backend API

The backend in `backend/app/` is built with:

- FastAPI
- SQLite for local persistence
- JWT-based authentication
- file upload support for fingerprint analysis

The API exposes endpoints for:

- user registration and login
- current user profile lookup
- prediction analysis
- prediction history retrieval
- saved user settings

## Folder structure

```text
Fingerprint_blood_group_detection/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth_utils.py
│   │   │   ├── prediction.py
│   │   │   ├── settings.py
│   │   │   └── users.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── main.py
│   │   └── ...
│   ├── requirements.txt
│   └── start_backend.bat
├── docs/
├── mobile/
│   ├── app/
│   ├── components/
│   ├── config/
│   ├── services/
│   ├── store/
│   ├── theme/
│   ├── types/
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── shared/
└── README.md
```

## Main features

### Authentication

Users can register and log in via `/api/users/register` and `/api/users/login`. Passwords are hashed with bcrypt, and JWT tokens are created for secure session access.

### Prediction workflow

The backend endpoint `/api/prediction/analyze` accepts an uploaded image and generates a simulated blood-group result based on random probabilities. The response includes:

- predicted blood group
- confidence score
- per-class probability breakdown
- quality score
- model metadata
- creation timestamp

It also stores prediction records in SQLite for the logged-in user.

### History and insights

The frontend fetches `/api/prediction/history` and shows recent predictions in the home dashboard and history screens. The UI also summarizes:

- total number of predictions
- best confidence
- most frequently predicted blood group

### Settings and personalization

Users can manage notification settings, theme, and language through the settings API and related mobile screens.

## Current technical reality

This repository is a functional prototype, not a production-ready medical diagnostic system. The key indicator is that the prediction logic is randomized and the backend explicitly labels the model as a mock implementation.

Important notes:

- the backend is using SQLite rather than MongoDB despite the config default string
- the analysis endpoint is an experimental mock ML inference, not a true trained model
- the app is prepared for local development and demo testing, not clinical deployment

## Tech stack summary

### Frontend

- Expo / React Native
- TypeScript
- Expo Router
- Zustand
- React Native Reanimated
- Lucide icons

### Backend

- Python
- FastAPI
- SQLite
- JWT authentication
- Pydantic settings

## Setup and running the project

### 1) Backend

From the repository root:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

On Windows, a convenience script is also provided:

```bat
backend\start_backend.bat
```

### 2) Mobile app

From the repository root:

```bash
cd mobile
npm install
npx expo start
```

The mobile app expects the backend to be reachable at the API URL defined in `mobile/config/api.ts`. In development, it uses:

- localhost for web
- `10.0.2.2:8001` for Android emulator
- a detected LAN IP for physical devices

If needed, set `EXPO_PUBLIC_API_URL` before starting Expo.

## Environment and configuration

The backend settings are defined in `backend/app/config.py` and include:

- project name
- MongoDB connection string placeholder
- JWT secret
- JWT algorithm
- token expiration period

For local development, these defaults are used, but production deployment should replace the secret and environment values with secure configuration.

## Security and production considerations

This prototype should not be deployed as-is for medical use without:

- a real ML model and validation pipeline
- secure encrypted storage for patient data
- stricter authentication and authorization rules
- production-grade database and file handling
- compliance review for medical device or healthcare workflows

## License

This project appears to include a license file in the mobile app directory, but the repository-level status should be checked before redistribution or commercial use.

## Conclusion

BloodID is a strong demo project for an AI-driven fingerprint blood-group prediction app. It demonstrates a complete full-stack workflow, including a mobile UX, authentication, image upload handling, prediction simulation, history tracking, and settings management. The current codebase is best understood as an educational and prototype platform rather than a clinically validated medical application.
