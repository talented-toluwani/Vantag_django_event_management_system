from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    created_by = models.ForeignKey(User, on_delete =models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.title
  
class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    participant = models.ForeignKey(User, on_delete = models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=20, choices= models.STATUS_CHOICES, default="active")

class Meta:
    unique_together = ("event", "participant")

    def __str__(self):
        return "f{self.particpant} - {self.event}"