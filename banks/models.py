from django.db import models
from django.contrib.auth.models import User

class Bank(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    inst_num = models.CharField(max_length=20)  # Adjust the max length as required
    swift_code = models.CharField(max_length=20)  # Adjust the max length as required
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banks')

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=255)
    transit_num = models.CharField(max_length=20)  # Adjust the max length as required
    address = models.TextField()
    email = models.EmailField()
    capacity = models.PositiveIntegerField()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='branches')
    last_modified = models.DateTimeField(auto_now=True)  # auto-updated to now every time the object is saved

    def __str__(self):
        return self.name
