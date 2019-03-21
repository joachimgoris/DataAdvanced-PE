import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


def get_category(date):
    if date <= 3:
        return 1
    elif date <= 6:
        return 2
    elif date <= 9:
        return 3
    else:
        return 4


def get_inzet_by_category(cat):
    if cat == 1:
        return 'zeer goed'
    elif cat == 2 or cat == 3:
        return 'goed'
    else:
        return 'matig'


start_date = pd.to_datetime('2011-01-01')
end_date = pd.to_datetime('2011-12-31')
data['geboortedatum'] = random_datetimes_or_dates(start_date, end_date, out_format='not datetime', n=len(data.index))
data['categorie'] = data['geboortedatum'].apply(lambda x: get_category(x.to_pydatetime().month))
data['inzet'] = data['categorie'].apply(lambda x: get_inzet_by_category(x))

# print(data['categorie'])

plot = data.plot.scatter(x='gewicht', y='lengte', c='DarkBlue')
plot.set_xlim(19, 31)
plot.set_ylim(110, 140)
fig = plot.get_figure()
fig.savefig('scatter.png')

bar_data = data.groupby(['positie', 'inzet'])['aantal gemaakte goalen'].sum().unstack()
plot = bar_data.plot.bar(title='Aantal Goalen Per Positie en Inzet')
plot.set_xlabel('Posities per Inzet')
plot.set_ylabel('Aantal Gemaakte Goalen')
fig = plot.get_figure()
fig.tight_layout()
fig.savefig('staaf_diagram.png')

gemiddelde = data['aantal gemaakte goalen'].mean()
modus = data['aantal gemaakte goalen'].mode()
print(gemiddelde)
print(modus)

standaardafwijking = data['gewicht'].std()
kwartiel1 = data['gewicht'].quantile(0.25)
print(standaardafwijking)
print(kwartiel1)

# pie_data = data.groupby(['inzet'])['inzet'].count().to_frame().rename(columns={'inzet':'counts'}).reset_index()

# pie_df = pd.DataFrame(dict(inzet=pie_data.index, count=pie_data.values))
# pie_data = data.groupby(data.inzet)['inzet'].sum().unstack()
# pie_data.plot(kind='pie', subplots=True, y='inzet')
# plt.pie(pie_data, labels=pie_data.index)

# plot = pie_data.plot.pie(subplots=True)
# fig = plot.get_figure()
# fig.savefig('circle.png')
# print(pie_data)

# plt.show()

