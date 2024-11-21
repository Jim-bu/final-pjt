from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 닉네임 필드
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="닉네임")
    # 나이 필드
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="나이")
    # 자산 필드
    money = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="자산")
    # 연봉 필드
    salary = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="연봉")
    # 예금 희망 금액
    desire_amount_deposit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="예금 희망 금액")
    # 예금 희망 기간 (월)
    deposit_period = models.PositiveIntegerField(null=True, blank=True, verbose_name="예금 희망 기간 (월)")
    # 월 적금 희망 금액
    desire_amount_saving = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="월 적금 희망 금액")
    # 적금 희망 기간 (월)
    saving_period = models.PositiveIntegerField(null=True, blank=True, verbose_name="적금 희망 기간 (월)")

    def __str__(self):
        return self.username
