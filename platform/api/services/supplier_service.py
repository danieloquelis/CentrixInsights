import pandas as pd
from .change_supplier_service import ChangeSupplierService
from ..models import SupplierContract
from ..serializer import SupplierContractSerializer


class SupplierService:

    # TODO: add pagination
    @staticmethod
    def get_suppliers_contracts():
        contracts = pd.read_csv('api/data/supplier_contracts.csv', sep=';')
        dynamic_tariff_2008 = pd.read_csv('api/data/prices_year_15min_random_2008.csv', sep=',')
        load_year_15min = pd.read_csv('api/data/load_year_15min.csv', sep=',')
        highest_power_consumption = pd.read_csv('api/data/highest_power_consumption.csv', sep=',')

        # Preparing consumption data before to process it
        load_year_15min['Date2'] = pd.to_datetime(load_year_15min['Date'], format='%d/%m/%Y')
        load_year_15min['Time2'] = pd.to_datetime(load_year_15min['Time'], format='%X')

        load_year_15min['day'] = load_year_15min.Date2.dt.day
        load_year_15min['month'] = load_year_15min.Date2.dt.month
        load_year_15min['year'] = load_year_15min.Date2.dt.year
        load_year_15min['hour'] = load_year_15min.Time2.dt.hour
        load_year_15min['minute'] = load_year_15min.Time2.dt.minute

        # Preparing supplier data
        contracts['beginning_day2'] = pd.to_datetime(contracts['beginning_day'], format='%X')
        contracts['end_day2'] = pd.to_datetime(contracts['end_day'], format='%X')
        contracts['beginning_day_hour'] = contracts.beginning_day2.dt.hour
        contracts['end_day_hour'] = contracts.end_day2.dt.hour

        # Adding price column
        dynamic_tariff_2008['Price (€/kWh)'] = dynamic_tariff_2008['Price'] / 1000

        # Compute suppliers list
        change_supplier_service = ChangeSupplierService(load_year_15min, highest_power_consumption, dynamic_tariff_2008)

        data = []
        for i in range(len(contracts)):
            bill = change_supplier_service.compute_bill_3(
                contracts.unique_tariff[i],
                contracts.high_tariff[i],
                contracts.low_tariff[i],
                contracts.beginning_day_hour[i],
                contracts.end_day_hour[i],
                contracts.contract_type[i],
                contracts.fixed_cost_month[i]
            )
            supplier = SupplierContract()
            supplier.name = contracts.supplier_name[i]
            supplier.bill = bill
            supplier.currency = '€'
            data.append(supplier)

        serializer = SupplierContractSerializer(data, many=True)
        print(serializer.data)
        return serializer.data
