import pandas as pd
import numpy as np

path_to_file = r'.\voetbal.xlsx'
data = pd.read_excel(path_to_file)


def random_datetimes_or_dates(start, end, out_format='datetime', n=10):

    '''
    unix timestamp is in ns by default.
    I divide the unix time value by 10**9 to make it seconds (or 24*60*60*10**9 to make it days).
    The corresponding unit variable is passed to the pd.to_datetime function.
    Values for the (divide_by, unit) pair to select is defined by the out_format parameter.
    for 1 -> out_format='datetime'
    for 2 -> out_format=anything else
    '''
    (divide_by, unit) = (10**9, 's') if out_format=='datetime' else (24*60*60*10**9, 'D')

    start_u = start.value//divide_by
    end_u = end.value//divide_by

    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit=unit)


start_date = pd.to_datetime('2011-01-01')
end_date = pd.to_datetime('2011-12-31')

data['geboortedatum'] = random_datetimes_or_dates(start_date, end_date, out_format='not datetime', n=len(data.index))


print(data['geboortedatum'])





