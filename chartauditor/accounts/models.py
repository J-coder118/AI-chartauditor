from django.contrib.auth.models import AbstractUser
from chartauditor.accounts.managers import CustomUserManager
from django.db import models
import uuid


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_profile = models.BooleanField(default=False)
    character_limit = models.IntegerField(default=0)
    stripe_customer_id = models.CharField(max_length=200, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class FacultyOption(models.Model):
    option_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.option_name


class CompanyInformation(models.Model):
    FLORIDA = 'Florida'
    CALIFORNIA = 'California'

    STATE_COMPLIANCE = (
        (FLORIDA, 'Florida'),
        (CALIFORNIA, 'California'),
    )

    JOINT_COMMISSION = 'Joint Commission'
    CARF = 'CARF'

    ACCREDITATION_OPTIONS = (
        (JOINT_COMMISSION, 'Joint Commission'),
        (CARF, 'CARF'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=200, blank=True)
    state_licence = models.CharField(max_length=200, choices=STATE_COMPLIANCE, null=True, blank=True)
    accreditation = models.CharField(max_length=200, choices=ACCREDITATION_OPTIONS, null=True, blank=True)
    accept_insurance = models.CharField(max_length=200, blank=True)
    facility_type = models.ManyToManyField(FacultyOption, blank=True)