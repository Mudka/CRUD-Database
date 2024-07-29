from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    workflow = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name