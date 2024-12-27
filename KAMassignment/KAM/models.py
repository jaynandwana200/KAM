from django.db import models
import datetime


# Create your models here.
class KAMmail(models.Model):
    KAMID = models.CharField(primary_key=True,max_length=10)
    KAMmailid = models.EmailField(default="abc@gmail.com")


class leads(models.Model):
    leadID = models.BigAutoField(primary_key=True)
    restaurantName = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30, default="Kota")
    state = models.CharField(max_length=20, default="Rajasthan")
    country = models.CharField(max_length=20, default="India")
    contactNumber = models.CharField(max_length=10)
    currentStatus = models.CharField(max_length=10)
    KAMID = models.ForeignKey(KAMmail, on_delete=models.CASCADE)
    callFrequency = models.IntegerField(default=10)
    time = models.TimeField(default=datetime.time(00, 00, 00))
    lastCallMade = models.DateField(default=datetime.date)


class tracking(models.Model):
    trackingID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=30)
    emailID = models.EmailField()
    leadID = models.ForeignKey(leads, on_delete=models.CASCADE)


class interactionLogging(models.Model):
    interactionID = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=10)
    notes = models.CharField(max_length=100)
    followUp = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField(default=datetime.time(00, 00, 00))
    leadID = models.ForeignKey(leads, on_delete=models.CASCADE)
