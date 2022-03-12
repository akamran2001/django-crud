from turtle import title
from django.db import models


class Message(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
