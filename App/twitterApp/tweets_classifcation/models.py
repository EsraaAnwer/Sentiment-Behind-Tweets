from django.db import models

# Create your models here.


class Contact_us(models.Model):
    first_name = models.CharField(max_length=50)
    mail = models.EmailField()
    phonenumber = models.CharField(max_length=50)
    message = models.CharField(max_length=2000)

    class Meta:
    	verbose_name_plural = "contact_us"
    	db_table = "contact_us"
