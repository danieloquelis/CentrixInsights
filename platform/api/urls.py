from django.urls import path
from .views import get_supplier_contracts

base_url = 'api/v1'

urlpatterns = [
    path(f'{base_url}/supplier/contracts', get_supplier_contracts),
    path(f'{base_url}/suppliers/contracts/<int:contractId>', get_supplier_contracts),
]