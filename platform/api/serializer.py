from rest_framework import serializers
from .models import SupplierContract


class SupplierContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierContract
        fields = ['name', 'bill', 'currency']
