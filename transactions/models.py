from django.db import models

from accounts.models import User
from common.models import BaseModel


class Transaction(BaseModel):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    amount = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "transactions"
