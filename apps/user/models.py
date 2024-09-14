from tortoise import fields

from core.base.base_models import BaseDBModel


class UserInfo(BaseDBModel):
    address = fields.CharField(max_length=50, unique=True, description="user's evm address")
    last_login = fields.DatetimeField(null=True)
    avatar = fields.CharField(max_length=200, null=True)
    username = fields.CharField(max_length=50, null=True)
    source = fields.CharField(max_length=30, null=True)
    invite_code = fields.CharField(max_length=10, null=True)
    wallet = fields.CharField(max_length=20, null=True)

    def __str__(self):
        return self.address

    class Meta:
        table = 'user_info'
