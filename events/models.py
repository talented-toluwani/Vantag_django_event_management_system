from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(blank= True )

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    location = models.CharField(max_length = 200)
    date = models.DateTimeField()
    capacity = models.IntegerField()
    is_cancelled = models.BooleanField(default = False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete =models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.title

class Registration(models.Model):
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('cancelled', 'Cancelled')
] 

    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=20, choices= STATUS_CHOICES, default="active")

    class Meta:
        unique_together = ("event", "participant")

    def __str__(self):
        return f"{self.participant} - {self.event}"