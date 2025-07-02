from django.db import models

# Create your models here.
class longtoshort(models.Model):
    long_url=models.URLField()
    custom_name=models.CharField(max_length=50, unique=True)
    create_date=models.DateField(auto_now_add=True)
    vist_count=models.IntegerField(default=0)

