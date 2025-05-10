from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends, Body

from users.auth import (authenticate_user, create_token,
                        get_token_payload, get_password_hash)
from users.models import UsersDAO, FollowDAO
from users.schemas import (SUserAuth, SUserRegister, SUserResponse,
                           SFollowResponse, SCreateTokenResponse,
                           SRefreshTokenResponse)


router = APIRouter(
    prefix='/api/v1',
    tags=['Authorization & Users']
)


def user_answer(data):
    answer = SUserResponse(
        id=data.id,
        email=data.email,
        username=data.username,
        date_joined=data.date_joined,
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role
    )
    return answer


@router.get(
    '/follow',
    response_model=list[SFollowResponse],
    summary='Subscriptions',
    description=('Returns all subscriptions of the user who made the request. '
                 'Anonymous requests are not allowed.')
)
async def read_follow(current_user: dict = Depends(get_token_payload)):
    user = await UsersDAO.find_one_or_none(email=current_user['sub'])
    follows = await FollowDAO.find_all('following_user', user_id=user.id)

    return (
        {
            'user': user.username,
            'following': follow.following_user.username
        }
        for follow in follows
    )


@router.post(
    '/follow',
    response_model=SFollowResponse,
    summary='Subscription',
    description=(
        'Subscribes the user on whose behalf the request is made to the user '
        'specified in the request body. Anonymous requests are not allowed.'
    )
)
async def subscription(following: str = Body(..., embed=True),
                       current_user: dict = Depends(get_token_payload)):
    user = await UsersDAO.find_one_or_none(email=current_user['sub'])
    if user.username == following:
        raise HTTPException(status_code=400,
                            detail='You cannot follow yourself.')

    follow = await UsersDAO.find_one_or_none(username=following)
    if not follow:
        raise HTTPException(status_code=404,
                            detail='There is no user with this name.')

    followers = await FollowDAO.find_one_or_none(user_id=user.id,
                                                 following_id=follow.id)
    if followers:
        raise HTTPException(
            status_code=404,
            detail=f"You are already subscribed to '{following}'."
        )

    await FollowDAO.add(user_id=user.id, following_id=follow.id)
    return {'user': user.username, 'following': following}


@router.post(
    '/jwt/create',
    response_model=SCreateTokenResponse,
    summary='Get JWT Token',
    description='Retrieve a JWT token.'
)
async def login_user(user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    await UsersDAO.update(model_id=user.id, last_login=datetime.utcnow())
    access_token = create_token(data={'sub': str(user.email)},
                                token_type='access')
    refresh_token = create_token(data={'sub': str(user.email)},
                                 token_type='refresh')
    return {'access': access_token, 'refresh': refresh_token,
            'token_type': 'Bearer'}


@router.post(
    '/jwt/refresh',
    response_model=SRefreshTokenResponse,
    summary='Refresh JWT Token',
    description='Refresh a JWT token.'
)
async def refresh_token(refresh: str = Body(..., embed=True)):
    token_data = await get_token_payload(token=refresh)

    if token_data['token_type'] != 'refresh':
        raise HTTPException(status_code=401,
                            detail='An invalid token was passed.')

    access_token = create_token(data={'sub': token_data['sub']},
                                token_type='access')
    return {'access': access_token, 'token_type': 'Bearer'}


@router.post(
    '/jwt/verify',
    summary='Validate JWT Token',
    description='Validate a JWT token.'
)
async def verify_token(token: str = Body(..., embed=True)):
    token_data = await get_token_payload(token=token)

    if token_data['token_type'] != 'access':
        raise HTTPException(status_code=401,
                            detail='An invalid token was passed.')
    return {}


@router.post(
    '/register',
    response_model=SUserResponse,
    summary='New User Registration',
    description='Register a new user.')
async def register_user(user_data: SUserRegister):
    existing_email = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail='A user with this email already exists.'
        )

    existing_user = await UsersDAO.find_one_or_none(username=user_data.name)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail='A user with this name already exists.'
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = await UsersDAO.add(
        email=user_data.email,
        password=hashed_password,
        username=user_data.name
    )
    return user_answer(new_user)


@router.get(
    '/me',
    response_model=SUserResponse,
    summary='User Data',
    description='Data of the user who made the request.'
)
async def read_user_me(current_user: dict = Depends(get_token_payload)):
    user = await UsersDAO.find_one_or_none(email=current_user['sub'])
    return user_answer(user)
# 
