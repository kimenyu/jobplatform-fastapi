from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import secret_key, ALGORITHM

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
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
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


def get_current_employer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get current user and verify they have employer role
    """
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
    access_denied_exception = HTTPException(status_code=403, detail="Access denied. Employer role required.")

    try:
        print("EMPLOYER TOKEN:", token)
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        print("EMPLOYER PAYLOAD:", payload)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError) as e:
        print("EMPLOYER JWT ERROR:", e)
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        print("EMPLOYER USER NOT FOUND")
        raise credentials_exception

    # Check if user has employer role
    if user.role != "employer":
        print(f"ACCESS DENIED - User role: {user.role}, Required: employer")
        raise access_denied_exception

    print("AUTHENTICATED EMPLOYER:", user.email)
    return user


def get_current_job_seeker(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get current user and verify they have job_seeker role
    """
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
    access_denied_exception = HTTPException(status_code=403, detail="Access denied. Job seeker role required.")

    try:
        print("JOB SEEKER TOKEN:", token)
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        print("JOB SEEKER PAYLOAD:", payload)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError) as e:
        print("JOB SEEKER JWT ERROR:", e)
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        print("JOB SEEKER USER NOT FOUND")
        raise credentials_exception

    # Check if user has job_seeker role
    if user.role != "job_seeker":
        print(f"ACCESS DENIED - User role: {user.role}, Required: job_seeker")
        raise access_denied_exception

    print("AUTHENTICATED JOB SEEKER:", user.email)
    return user


def require_role(role: str):
    """
    Generic role checker - existing function
    """

    def checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user

    return checker


def require_any_role(*roles: str):
    """
    Check if user has any of the specified roles
    """

    def checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required roles: {', '.join(roles)}"
            )
        return user

    return checker


def get_current_user_optional(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User | None:
    """
    Get current user but don't raise exception if not authenticated
    Useful for endpoints that work for both authenticated and anonymous users
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except (JWTError, ValueError, TypeError):
        return None


def verify_user_owns_resource(resource_user_id: int):
    """
    Verify that the current user owns a specific resource
    """

    def checker(current_user: User = Depends(get_current_user)):
        if current_user.id != resource_user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied. You can only access your own resources."
            )
        return current_user

    return checker