import pandas as pd

def calculate_contract_value(injection_date, withdrawal_date, buy_price, sell_price, injection_rate, withdrawal_rate, max_volume, monthly_storage_cost, transport_cost):
    storage_time_delta = withdrawal_date - injection_date
    storage_time_months = storage_time_delta / pd.Timedelta(days=30)  # assuming 30 days per month
    storage_cost = monthly_storage_cost * storage_time_months
    injection_and_withdrawal_cost = (max_volume / 1000000) * (injection_rate + withdrawal_rate)
    total_transport_cost = 2 * transport_cost
    contract_value = sell_price - buy_price - storage_cost - total_transport_cost - injection_and_withdrawal_cost

    return contract_value

# Rates are per million MMBtu
monthly_storage_cost = 100000
injection_rate = 10000
withdrawal_rate = 10000
transport_cost = 50000
max_volume = 10000000

df = pd.read_csv('Nat_Gas.csv')
df['Dates'] = pd.to_datetime(df['Dates'], format='%m/%d/%y')
df.set_index('Dates', inplace=True)
#Picking any injection and withdrawal date
injection_date = df['Prices'].idxmin()
withdrawal_date = df['Prices'].idxmax()
buy_price = df.loc[injection_date, 'Prices']
sell_price = df.loc[withdrawal_date, 'Prices']

result = calculate_contract_value(injection_date, withdrawal_date, buy_price, sell_price, injection_rate, withdrawal_rate, max_volume, monthly_storage_cost, transport_cost)

print("Contract Value:", result)
