from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from fastapi.templating import Jinja2Templates
from server.database import User, get_user_db
import smtplib
from email.message import EmailMessage
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP


SECRET = "SECRET"

templates = Jinja2Templates(directory="templates")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('ilja.bazhanov@gmail.com','nvoyazrqlhrclksk')

        smtpObj.sendmail("ilja.bazhanov@gmail.com", user.email, token)
        print(user.email, token)
    async def on_after_reset_password(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has reset their password.")
    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,

    ):
        print('after')

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user
    


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
