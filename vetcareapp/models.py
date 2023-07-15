from django.db import models
       
class UserDate(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)
    
class ChatForm(models.Model):
    sender = models.CharField(max_length=250)
    message = models.TextField()
    receiver = models.CharField(max_length=250)

    def __str__(self):
        return str(self.owner)