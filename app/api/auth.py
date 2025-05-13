from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils.password import hash_password
from app.database import get_db
from app.models import User
from app.schemas.user import UserSignUp, UserSignUpSuccess


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def create_user(db: Session, user: UserSignUp):
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)


@router.post("/signup", response_model=UserSignUpSuccess)
async def user_signup(user: UserSignUp, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    create_user(db, user)
    return {"message": "SignUp Successfull"}
