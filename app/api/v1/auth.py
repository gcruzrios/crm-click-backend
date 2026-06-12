from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
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
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        body = await request.json()
        email = body.get("email") or body.get("username")
        password = body.get("password")
        if not email or not password:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="email and password are required")
    else:
        form = await request.form()
        email = form.get("username") or form.get("email")
        password = form.get("password")
        if not email or not password:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username and password are required")

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
