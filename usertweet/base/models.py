from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class tweets(models.Model):
    tweet = models.CharField(max_length=200, null=True, blank=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.tweet

    class Meta:
        db_table = 'tweets'
