from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Organization Officer (Admin)'
        COORDINATOR = 'COORDINATOR', 'Event Coordinator'
        ADVISER = 'ADVISER', 'Faculty Adviser'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.COORDINATOR)
    contact_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"