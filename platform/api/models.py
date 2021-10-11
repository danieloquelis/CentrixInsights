from django.db import models


# Create your models here.

class SupplierContract(models.Model):
    contractId = models.CharField(max_length=100)
    supplierId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    bill = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=5)

    def __str__(self):
        return self.name
