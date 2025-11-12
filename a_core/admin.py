from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from a_core.models import UserProfile, Cats, CatPicture, AdoptionRequest
# Register your models here.

admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(UserProfile)
admin.site.register(Cats)
admin.site.register(CatPicture)
admin.site.register(AdoptionRequest)