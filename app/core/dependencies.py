from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
    try:
        print("TOKEN:", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("PAYLOAD:", payload)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError) as e:
        print("JWT ERROR:", e)
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        print("USER NOT FOUND")
        raise credentials_exception
    print("AUTHENTICATED USER:", user.email)
    return user



def require_role(role: str):
    def checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return checker
