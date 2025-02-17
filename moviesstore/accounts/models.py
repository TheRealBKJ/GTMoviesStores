from django.db import models
from django.contrib.auth.models import User

class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def generate_token(self):
        self.token = str(uuid.uuid4())
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.token}"
