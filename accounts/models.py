from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username.username

