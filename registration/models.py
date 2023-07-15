from django.db import models


class Patient(models.Model):
    username = models.CharField(max_length=250)
    phonenumber = models.CharField(max_length=10)
    email = models.CharField(max_length=250)
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.username


class Doctor(models.Model):
    # QUALIFICATIONS = [
    #     ("Bachelor of Veterinary Science", "Bachelor of Veterinary Science"),
    #     ("Master Programme (MVSc)", "Master Programme (MVSc)"),
    #     ("Doctoral Programme (PhD)", "Doctoral Programme (PhD)"),
    #     ("National Diploma", "National Diploma"),
    # ]

    username = models.CharField(max_length=250)
    phonenumber = models.CharField(max_length=10)
    email = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    lat = models.FloatField()
    # qualifications = models.CharField(max_length=30, choices=QUALIFICATIONS)
    lng = models.FloatField()
    time1 = models.TimeField(blank=True)
    time2 = models.TimeField(blank=True)
    days = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.username

class Consult(models.Model):
    ownername = models.CharField(max_length=250)
    phone = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
    pet_name = models.CharField(max_length=250)
    pet_age = models.IntegerField()
    pet_type = models.CharField(max_length=250)
    symptoms = models.TextField()
    doctor = models.CharField(max_length=250)
    
    def __str__(self):
        return self.ownername
    
    class Meta:
        db_table = 'consult'