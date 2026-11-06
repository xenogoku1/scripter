from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from database import supabase
from schemas import UserRegister, UserLogin, ScriptCreate, AudioNoteCreate

app = FastAPI(title="TalkScript API", version="1.0.0")

# Enable CORS so your Vue 3 frontend can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/auth", tags=["Auth"])
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "TalkScript FastAPI Backend is live! 🚀"}

# --- AUTHENTICATION ENDPOINTS ---

@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    """
    Registers a new user with Supabase Auth using email, password, and username.
    """
    try:
        # Sign up user in Supabase Auth
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "username": user.username
                }
            }
        })
        
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed. User could not be created."
            )
            
        return {
            "message": "User registered successfully. Please check your email for verification if enabled.",
            "user_id": response.user.id
        }
        
    except Exception as e:
        # Catch errors from Supabase or validation and return a clean HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.post("/auth/login")
def login_user(user: UserLogin):
    """
    Authenticates a user via Supabase and returns the session access token.
    """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if not response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )
            
        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user_id": response.user.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/google")
def google_auth():
    try:
        # Ask Supabase to generate the Google OAuth sign-in URL
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": "http://localhost:5173/" # Frontend callback/home URL
            }
        })
        return {"url": response.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))