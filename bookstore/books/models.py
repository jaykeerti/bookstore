from django.db import models

# Create your models here.
class BookInventory(models.Model):
    bookid = models.CharField(max_length=20,primary_key=True)
    quantity = models.IntegerField()

