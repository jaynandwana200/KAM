from django.db import models

# Create your models here.
class leads(models.Model):
    leadID = models.BigAutoField(primary_key=True)
    restaurantName = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=10)
    currentStatus = models.CharField(max_length=10)
    KAMID = models.CharField(max_length=10)

class tracking(models.Model):
    trackingID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=30)
    emailID = models.EmailField()
    leadID = models.ForeignKey(leads,on_delete=models.CASCADE)

class interactionLogging(models.Model):
    interactionID = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=10)
    notes = models.CharField(max_length=100)
    followUp = models.CharField(max_length=10)
    date = models.DateField()
    leadID = models.ForeignKey(leads,on_delete=models.CASCADE)