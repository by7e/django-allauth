from django.db import models
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
class Cats(models.Model):
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    adopter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='adopted_cats', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    is_adopted = models.BooleanField(default=False)
    is_ill = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.id}: {self.name}"
    

class CatPicture(models.Model):
    # This is the ForeignKey creating the Many-to-One link: Many Pictures to One Cat
    cat = models.ForeignKey(Cats, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cat_gallery/')
    
    def __str__(self):
        return f"Picture for {self.cat.name}"

class AdoptionRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'pending'
        APPROVED = 'Approved', 'approved'
        REJECTED = 'Rejected', 'rejected'

    cat = models.ForeignKey(Cats, on_delete=models.CASCADE)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"Adoption request for {self.cat.name} by {self.requester.username}"