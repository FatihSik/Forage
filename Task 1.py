import pandas as pd
import numpy as np

data = pd.read_csv('Nat_Gas.csv')

data['Dates'] = pd.to_datetime(data['Dates'], format='%m/%d/%y')
data.set_index(pd.DatetimeIndex(data['Dates']), inplace=True)
pivot_date = data['Dates'].min()

data['index'] = (data.index.month - pivot_date.month) + (data.index.year - pivot_date.year)*12

x = data['index']
y = data['Prices']

x_mean = np.mean(x)
y_mean = np.mean(y)

diff_x = x - x_mean
diff_y = y - y_mean

reg_gradient = np.sum(diff_x * diff_y)/np.sum((diff_x)**2)

reg_intercept = y_mean - reg_gradient*x_mean

def y_pred(x, gradient, y_intercept):
    return gradient*x + y_intercept

def average_residual(date):
    month = date.month
    month_data = data[data.index.month == month]  # Filter the DataFrame for the selected month
    month_prices = month_data['Prices']
    month_dates_index = (month_data.index.month - pivot_date.month) + (month_data.index.year - pivot_date.year) * 12
    average_residual_month = np.mean(month_prices - y_pred(month_dates_index, reg_gradient, reg_intercept))
    return average_residual_month

user_x = input('Enter in a date in the form MM/DD/YYYY: ')
user_x_date = pd.to_datetime(user_x, format='%m/%d/%Y')
user_x_index = user_x_date.month - pivot_date.month + (user_x_date.year - pivot_date.year)*12

y_pred_value = y_pred(user_x_index, reg_gradient, reg_intercept)

print(y_pred_value + average_residual(user_x_date))
