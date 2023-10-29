from django.db import models

# Create your models here.

class TodoItem(models.Model):
    url_path = models.CharField(max_length=200)
    table_num = models.CharField(max_length=200)