from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from .models import (
    UserCreate, UserLogin, UserResponse, QuizAnswers, MoodResult, MoodScores,
    SpotifyAuthRequest, SpotifyCallbackRequest, CreatePlaylistRequest
)
from .database import get_database
from passlib.context import CryptContext
from datetime import datetime
from .quiz_data import calculate_mood_scores, QUIZ_QUESTIONS
from bson import ObjectId
from .spotify_service import (
    get_spotify_auth_url, get_spotify_client, exchange_code_for_token,
    get_recommendations, create_playlist
)

router = APIRouter()

# Password hashing (even though you said no security, we'll do basic hashing)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/auth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    """Create a new user account"""
    db = get_database()
    users_collection = db["users"]

    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user_dict = {
        "fullName": user.fullName,
        "email": user.email,
        "password": hash_password(user.password),
        "createdAt": datetime.utcnow()
    }

    result = await users_collection.insert_one(user_dict)

    # Return user data (without password)
    return UserResponse(
        id=str(result.inserted_id),
        fullName=user.fullName,
        email=user.email,
        createdAt=user_dict["createdAt"]
    )


@router.post("/auth/login", response_model=UserResponse)
async def login(user_login: UserLogin):
    """Login with email and password"""
    db = get_database()
    users_collection = db["users"]

    # Find user by email
    user = await users_collection.find_one({"email": user_login.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(user_login.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Return user data (without password)
    return UserResponse(
        id=str(user["_id"]),
        fullName=user["fullName"],
        email=user["email"],
        createdAt=user["createdAt"]
    )


@router.get("/auth/users/{email}")
async def get_user(email: str):
    """Check if a user exists by email"""
    db = get_database()
    users_collection = db["users"]

    user = await users_collection.find_one({"email": email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": str(user["_id"]),
        "fullName": user["fullName"],
        "email": user["email"],
        "exists": True
    }


# Quiz Routes
@router.get("/quiz/questions")
async def get_quiz_questions():
    """Get all quiz questions"""
    return {
        "questions": QUIZ_QUESTIONS
    }


@router.post("/quiz/calculate-mood", response_model=MoodResult)
async def calculate_mood(quiz_answers: QuizAnswers):
    """Calculate mood scores based on quiz answers"""
    db = get_database()
    users_collection = db["users"]
    mood_results_collection = db["mood_results"]

    # Verify user exists (convert string ID to ObjectId)
    try:
        user_object_id = ObjectId(quiz_answers.userId)
        user = await users_collection.find_one({"_id": user_object_id})
    except Exception as e:
        # If ObjectId conversion fails or user not found, continue anyway for guest users
        user = None
        print(f"User lookup failed: {e}. Continuing with guest mode.")

    # Calculate mood scores
    mood_data = calculate_mood_scores(quiz_answers.answers)

    # Create mood result
    mood_result = {
        "userId": quiz_answers.userId,
        "moodScores": mood_data["moodScores"],
        "dominantMood": mood_data["dominantMood"],
        "createdAt": datetime.utcnow()
    }

    # Save to database
    result = await mood_results_collection.insert_one(mood_result)

    # Return result
    return MoodResult(
        userId=quiz_answers.userId,
        moodScores=MoodScores(**mood_data["moodScores"]),
        dominantMood=mood_data["dominantMood"],
        createdAt=mood_result["createdAt"]
    )


@router.get("/quiz/mood-history/{user_id}")
async def get_mood_history(user_id: str):
    """Get user's mood calculation history"""
    db = get_database()
    mood_results_collection = db["mood_results"]

    # Get all mood results for user
    cursor = mood_results_collection.find({"userId": user_id}).sort("createdAt", -1)
    results = await cursor.to_list(length=100)

    if not results:
        return {"moodHistory": []}

    # Format results
    mood_history = []
    for result in results:
        mood_history.append({
            "id": str(result["_id"]),
            "moodScores": result["moodScores"],
            "dominantMood": result["dominantMood"],
            "createdAt": result["createdAt"]
        })

    return {"moodHistory": mood_history}


# Spotify Routes
@router.get("/spotify/auth")
async def spotify_auth(userId: str):
    """Get Spotify authorization URL"""
    try:
        auth_url = get_spotify_auth_url()
        # Store userId in database to retrieve after callback
        db = get_database()
        spotify_auth_collection = db["spotify_auth_sessions"]

        # Store temporary session
        await spotify_auth_collection.insert_one({
            "userId": userId,
            "createdAt": datetime.utcnow()
        })

        return {"authUrl": auth_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate Spotify auth URL: {str(e)}"
        )


@router.get("/spotify/callback")
async def spotify_callback(code: str, state: str = None):
    """Handle Spotify OAuth callback"""
    try:
        # Exchange code for access token
        token_info = exchange_code_for_token(code)

        # For simplicity, redirect to frontend with token
        # In production, you'd want to store this more securely
        frontend_url = (
            f"http://localhost:8081/SpotifySuccess?"
            f"access_token={token_info['access_token']}&"
            f"refresh_token={token_info.get('refresh_token', '')}"
        )



        return RedirectResponse(url=frontend_url)
    except Exception as e:
        error_url = f"http://localhost:19006/spotify-error?error={str(e)}"
        return RedirectResponse(url=error_url)


@router.post("/spotify/generate-playlist")
async def generate_playlist(request: CreatePlaylistRequest):
    """Generate playlist recommendations based on mood"""
    try:
        # Get Spotify client with access token
        sp = get_spotify_client(request.accessToken)

        # Get recommendations based on mood
        tracks = get_recommendations(sp, request.mood)

        return {
            "tracks": tracks,
            "mood": request.mood
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate playlist: {str(e)}"
        )


@router.post("/spotify/create-playlist")
async def create_spotify_playlist(request: CreatePlaylistRequest):
    """Create playlist on user's Spotify account"""
    db = get_database()
    playlists_collection = db["playlists"]

    try:
        # Get Spotify client
        sp = get_spotify_client(request.accessToken)

        # Get recommendations
        tracks = get_recommendations(sp, request.mood)

        # Create playlist on Spotify
        playlist_info = create_playlist(sp, request.userId, request.mood, tracks)

        # Save playlist to database
        playlist_doc = {
            "userId": request.userId,
            "mood": request.mood,
            "spotifyPlaylistId": playlist_info["playlist_id"],
            "playlistName": playlist_info["playlist_name"],
            "playlistUrl": playlist_info["playlist_url"],
            "tracksCount": playlist_info["tracks_added"],
            "tracks": tracks,
            "createdAt": datetime.utcnow()
        }

        result = await playlists_collection.insert_one(playlist_doc)

        return {
            "success": True,
            "playlistId": str(result.inserted_id),
            "spotifyPlaylistId": playlist_info["playlist_id"],
            "playlistUrl": playlist_info["playlist_url"],
            "playlistName": playlist_info["playlist_name"],
            "tracksAdded": playlist_info["tracks_added"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create Spotify playlist: {str(e)}"
        )


@router.get("/spotify/playlists/{user_id}")
async def get_user_playlists(user_id: str):
    """Get user's saved playlists"""
    db = get_database()
    playlists_collection = db["playlists"]

    try:
        cursor = playlists_collection.find({"userId": user_id}).sort("createdAt", -1)
        playlists = await cursor.to_list(length=100)

        result = []
        for playlist in playlists:
            result.append({
                "id": str(playlist["_id"]),
                "mood": playlist["mood"],
                "playlistName": playlist["playlistName"],
                "playlistUrl": playlist["playlistUrl"],
                "tracksCount": playlist["tracksCount"],
                "createdAt": playlist["createdAt"]
            })

        return {"playlists": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch playlists: {str(e)}"
        )
