from fastapi import APIRouter, HTTPException, status
from models import UserCreate, UserLogin, UserResponse
from database import get_database
from passlib.context import CryptContext
from datetime import datetime

router = APIRouter()

# Password hashing (even though you said no security, we'll do basic hashing)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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


@router.post("/login", response_model=UserResponse)
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


@router.get("/users/{email}")
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
