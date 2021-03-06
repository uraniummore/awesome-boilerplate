from fastapi import APIRouter, Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm

from app.types import UserAuthForm, UserType, EditUserForm
from app.types.identity import SocialAuthData
from app.controllers.users import UsersController
from app.types.user import RefreshTokenData

router = APIRouter()
controller = UsersController()


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return controller.login_user(form_data)


@router.post("/token/refresh")
def refresh_auth_token(data: RefreshTokenData = Body(...)):
    return controller.validate_refresh_token(data.token)


@router.get("/me")
def get_current_user(current_user: UserType = Depends(controller.get_current_user)):
    return {"user": current_user}


@router.post("/register")
def create_user(data: UserAuthForm):
    return controller.create_new_user(data)


@router.put("/update")
def update_user(form_data: EditUserForm = Body(...), user: UserType = Depends(controller.get_current_user)):
    return controller.update_user(user, form_data)


@router.post("/auth/linkedin")
def authenticate_linkedin(data: SocialAuthData = Body(...)):
    return controller.authenticate_linkedin(data)


@router.post("/auth/google")
def authenticate_google(data: SocialAuthData = Body(...)):
    return controller.authenticate_google(data)


@router.post("/auth/facebook")
def authenticate_facebook(data: SocialAuthData = Body(...)):
    return controller.authenticate_facebook(data)
