from typing import Optional

from pydantic import BaseModel


class CredentialsSchema(BaseModel):
    address: Optional[str]


class CredentialsRefreshSchema(BaseModel):
    refresh_token: Optional[str]


class JWTToken(BaseModel):
    access_token: str
    refresh_access_token: str
    token_type: str


class JWTRefreshToken(BaseModel):
    access_token: str
    token_type: str

# class JWTTokenData(BaseModel):
#     username: str = None


class JWTTokenPayload(BaseModel):
    user_id: int = None


class Msg(BaseModel):
    msg: str