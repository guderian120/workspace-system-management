from django.db import models

class CsvData(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    computed_value = models.FloatField()  # Store computed result

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
