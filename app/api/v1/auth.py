import json as _json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import get_current_user
from app.core.security import hash_password, verify_password
from app.db.session import get_db
from app.schemas.user import ChangePasswordRequest, UserResponse
from app.services.auth_service import authenticate_user, issue_tokens, refresh_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/login")
async def login(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    body_bytes = await request.body()
    email: str | None = None
    password: str | None = None

    # Try JSON first — works with or without Content-Type: application/json
    try:
        parsed = _json.loads(body_bytes)
        email = parsed.get("email") or parsed.get("username")
        password = parsed.get("password")
    except Exception:
        pass

    # Fall back to URL-encoded form data (OAuth2PasswordRequestForm, HTML forms)
    if not email or not password:
        try:
            form = await request.form()
            email = form.get("username") or form.get("email")
            password = form.get("password")
        except Exception:
            pass

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="email and password are required",
        )

    user = await authenticate_user(db, email, password)
    tokens = issue_tokens(user.id)
    tokens["user"] = UserResponse.model_validate(user)
    return tokens


@router.post("/refresh")
async def refresh(payload: RefreshRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    return await refresh_access_token(db, payload.refresh_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    return None


@router.post("/change-password")
async def change_password(
    payload: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: Annotated[AsyncSession, Depends(get_db)] = None,
):
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    current_user.password_hash = hash_password(payload.new_password)
    db.add(current_user)
    await db.commit()
    return {"message": "Password updated successfully"}
