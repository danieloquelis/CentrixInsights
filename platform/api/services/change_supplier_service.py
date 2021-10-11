from datetime import datetime


class ChangeSupplierService:
    start_period = 396 + 24 * 60  # TODO: CHANGE THOSE NUMBERS
    end_period = 396 + 24 * 60 * 2  # TODO: CHANGE THOSE NUMBERS

    def __init__(self, consumption_df, highest_power_consumption, prices_df):
        self.consumption_df = consumption_df
        self.highest_power_consumption = highest_power_consumption
        self.prices_df = prices_df

    @staticmethod
    def dual_tariff(current_date, current_hour, beginning_night_hour, end_night_hour, high_tariff, low_tariff):
        if current_date.weekday() > 4:  # monday is 0 etc sunday is 6
            if current_hour > beginning_night_hour or current_hour < end_night_hour:
                # week end night
                return low_tariff
            else:
                # week end daytime
                return low_tariff
        else:
            if current_hour > beginning_night_hour or current_hour < end_night_hour:
                # week day night
                return low_tariff
            else:
                # week day daytime'
                return high_tariff

    @staticmethod
    def single_tariff(unique_tariff):
        return unique_tariff

    @staticmethod
    def get_dynamic_tariff(df, i):
        return df.loc[i, ['Price (€/kWh)']][0]

    def switch_contracts(self,
                         unique_tariff,
                         current_date,
                         current_hour,
                         beginning_night_hour,
                         end_night_hour,
                         high_tariff,
                         prices_df,
                         low_tariff,
                         contract_type,
                         i):
        switcher = {
            1: self.single_tariff(unique_tariff),
            2: self.dual_tariff(current_date, current_hour, beginning_night_hour, end_night_hour, high_tariff,
                                low_tariff),
            3: self.get_dynamic_tariff(prices_df, i)
        }
        return switcher.get(contract_type)

    """
        contract_type:
            1 : single
            2 : dual
            3 : dynamic
    """
    def compute_bill_3(self, unique_tariff, high_tariff, low_tariff, beginning_night_hour, end_night_hour,
                       contract_type, monthly_fee):
        bill = 0
        capacity_tariff = 0.2  # €/kW

        try:
            for i in range(len(self.consumption_df)):
                year = self.consumption_df.year[i]
                month = self.consumption_df.month[i]
                day = self.consumption_df.day[i]

                current_date = datetime(year, month, day)
                current_hour = self.consumption_df.hour[i]

                tariff = self.switch_contracts(unique_tariff,
                                               current_date,
                                               current_hour,
                                               beginning_night_hour,
                                               end_night_hour,
                                               high_tariff,
                                               self.prices_df,
                                               low_tariff,
                                               contract_type,
                                               i)

                # kWh  # careful : no _ between the word, unlike in dataframe load
                consumption_15_min = float(self.consumption_df.loc[i, ['Global active power']][0]) * 15 / 60

                bill += tariff * consumption_15_min

            print(self.highest_power_consumption)
            for m in range(12):
                bill += capacity_tariff * self.highest_power_consumption.loc[m, ['Highest power consumption (kW)']][
                    0] + monthly_fee

            print(f'Daily household electricity cost: {bill} €')
            return bill
        except TypeError as err:
            print("Something wrong")
            return 0

