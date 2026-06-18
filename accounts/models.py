from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('participant', 'Participant')
    )

    role = models.CharField(max_length=20, choices = ROLE_CHOICES,  default= 'participant')

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
        
        elif self.role == 'participant':
            self.is_staff = False

        else:
          raise ValueError('Users must either be admins or participants')

        super().save(*args, **kwargs)
