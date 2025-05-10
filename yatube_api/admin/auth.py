from datetime import datetime
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from config import settings
from users.auth import authenticate_user, create_token, get_token_payload
from users.models import UsersDAO


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form['username'], form['password']

        user = await authenticate_user(email, password)
        if user and user.role in ('moderator', 'admin', 'root'):
            await UsersDAO.update(model_id=user.id,
                                  last_login=datetime.utcnow())
            access_token = create_token(data={'sub': str(user.email)},
                                        token_type='access')
            request.session.update({'token': access_token, 'role': user.role})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get('token')
        role = request.session.get('role')

        if not token or not role:
            return False

        token_data = await get_token_payload(token=token)
        if token_data and token_data['sub']:
            user = await UsersDAO.find_one_or_none(email=token_data['sub'])
            if user and user.role == role:
                return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
# 
