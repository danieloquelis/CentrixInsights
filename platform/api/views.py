from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.supplier_service import SupplierService


# Create your views here.

@api_view(['GET'])
def get_supplier_contracts(request):
    if request.method == 'GET':
        print('GET Successfully')
        supplier_service = SupplierService()
        return Response(supplier_service.get_suppliers_contracts(), status=status.HTTP_200_OK)
