from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    CATEGORY_CHOICES = [
        ('engineer', 'Engineer'),
        ('contractor', 'Contractor'),
        ('worker', 'worker'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    license_number = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    license_no = models.CharField(max_length=100, blank=True, null=True)  # ✅ Add this
    license_file = models.FileField(upload_to='licenses/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.category})"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

