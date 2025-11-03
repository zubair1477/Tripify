from fastapi import APIRouter, HTTPException, status
from models import UserCreate, UserLogin, UserResponse, QuizAnswers, MoodResult, MoodScores
from database import get_database
from passlib.context import CryptContext
from datetime import datetime
from quiz_data import calculate_mood_scores, QUIZ_QUESTIONS
from bson import ObjectId

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
