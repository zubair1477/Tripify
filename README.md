# Tripify

Tripify is an innovative mobile application that revolutionizes the road trip experience by creating personalized music playlists based on the user's current emotional state and their destination.

## Tech Stack

**Frontend:** React Native with Expo
**Backend:** FastAPI (Python)
**Database:** MongoDB Atlas

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.11 or higher
- Node.js and npm
- MongoDB Atlas account (free tier)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Tripify
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0
DATABASE_NAME=tripify
PORT=8000
```

Replace `username`, `password`, and the cluster URL with your MongoDB Atlas credentials.

#### Set Up MongoDB Atlas

1. Go to https://www.mongodb.com/cloud/atlas/register and create a free account
2. Create a new cluster (M0 Free tier)
3. Under "Database Access", create a database user with username and password
4. Under "Network Access", add `0.0.0.0/0` to allow access from anywhere (for development)
5. Get your connection string by clicking "Connect" on your cluster and choosing "Drivers"
6. Update the `.env` file with your connection string

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd TripifyApp
npm install
```

## Running the Application

You need to run both the backend and frontend simultaneously in separate terminal windows.

### Terminal 1: Start the Backend

```bash
cd backend/src
uvicorn main:app --reload --port 8000
```

You should see:
```
Successfully connected to MongoDB!
Application startup complete.
```

The backend API will be running at http://127.0.0.1:8000

### Terminal 2: Start the Frontend

```bash
cd TripifyApp
npm start
```

After the Expo development server starts, press `w` to open the app in your web browser.

Alternatively:
- Press `i` to open in iOS Simulator (macOS only)
- Press `a` to open in Android Emulator
- Scan the QR code with the Expo Go app on your phone

## Project Structure

```
Tripify/
├── backend/
│   ├── src/
│   │   ├── main.py           # FastAPI application entry point
│   │   ├── routes.py         # API routes for authentication
│   │   ├── models.py         # Pydantic models
│   │   └── database.py       # MongoDB connection
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment variables (not in git)
└── TripifyApp/
    ├── app/                  # React Native app screens
    ├── assets/               # Images and static files
    ├── package.json          # Node dependencies
    └── index.ts              # App entry point
```

## API Endpoints

- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/login` - Login with email and password
- `GET /api/auth/users/{email}` - Get user information by email



