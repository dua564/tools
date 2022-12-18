import pandas as pd
import pprint
import datetime

df = pd.read_csv(r'/Users/nikhildua/Documents/scripts/red-hot-chilli/Financial Shifts Summary.csv')


def set_pandas_display_options() -> None:
    """Set pandas display options."""
    # Ref: https://stackoverflow.com/a/52432757/
    display = pd.options.display
    display.max_columns = 1000
    display.max_rows = 1000
    display.max_colwidth = 199
    display.width = 1000
    # display.precision = 2  # set as needed
set_pandas_display_options()



df_new = df[['Employee/Drawer', 'Started', 'Closed', 'Non-Cash Tips', 'Gratuity']].copy()


df_new['70%_Gratuity'] = df_new["Gratuity"] * 0.7
df_new['Total_Tips'] = df_new['70%_Gratuity'] + df_new['Non-Cash Tips']

df_new['timestamp'] = pd.to_datetime(df_new['Closed'])
df_new['date'] = df_new['timestamp'].dt.date
#df_new['time'] = df_new['timestamp'].dt.time
df_new['hour'] = df_new['timestamp'].dt.hour




#pprint.pprint((df_new))

def categorise(row):
    pass
    if float(row['hour']) <= 16:
        return 'Morning'
    elif float(row['hour']) > 16:
        return 'Night'
    else:
        return 'Night'


df_new['TOD'] = df_new.apply(lambda row: categorise(row), axis=1)
#pprint.pprint((df_new))

df_categorized = df_new[['Employee/Drawer', 'date', 'hour', 'TOD', 'Gratuity', '70%_Gratuity', 'Non-Cash Tips',  'Total_Tips']].copy()
pprint.pprint(df_categorized)

df_categorized_date = df_categorized.groupby(['date', 'TOD']).sum()
pprint.pprint(df_categorized_date)

df_categorized_date.to_csv('red-hot-chilli.csv')








#df new = old[['A', 'C', 'D']].copy()
