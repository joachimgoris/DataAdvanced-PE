import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1 - inladen van het excel bestand
path_to_file = r'.\voetbal.xlsx'
data = pd.read_excel(path_to_file)


def random_datetimes_or_dates(start, end, out_format='datetime', n=10):
    """
    :param start: first possible date
    :param end: last possible date
    :param out_format: format
    :param n: amount of dates
    :return: pandas object with specified amount of dates
    """
    (divide_by, unit) = (10**9, 's') if out_format=='datetime' else (24*60*60*10**9, 'D')

    start_u = start.value//divide_by
    end_u = end.value//divide_by

    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit=unit)


def get_category(month):
    """
    Get category based on month of year

    1 - January, Fabruary, March
    2 - April, May, June
    3 - July, August, September
    4 - October, November, December

    :param month: month to get the category of
    :return: the category (1-4)
    """
    if month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    else:
        return 4


def get_inzet_by_category(cat):
    """
    Get inzet van category

    :param cat: cateogry of the month of birth
    :return: inzet (matig, goed, zeer goed)
    """
    if cat == 1:
        return 'zeer goed'
    elif cat == 2 or cat == 3:
        return 'goed'
    else:
        return 'matig'


# 2 - genereren van de geboorte datum en indeling in de 4 categorieën
start_date = pd.to_datetime('2011-01-01')
end_date = pd.to_datetime('2011-12-31')
data['geboortedatum'] = random_datetimes_or_dates(start_date, end_date, out_format='not datetime', n=len(data.index))
data['categorie'] = data['geboortedatum'].apply(lambda x: get_category(x.to_pydatetime().month))

# 3 - genereren van de colom inzet
data['inzet'] = data['categorie'].apply(lambda x: get_inzet_by_category(x))

# 4 - maken spreidingsdiagram (x-as: gewitch, y-as: lengte)
plot = data.plot.scatter(x='gewicht', y='lengte', c='DarkBlue')
plot.set_xlim(19, 31)  # min en max waarde van de x-as
plot.set_ylim(110, 140)  # min en max waarde van de y-as
fig = plot.get_figure()
fig.savefig('scatter.png')

# 5 - staafdiagram van het aantal gemaakte goalen per positie
bar_data = data.groupby(['positie', 'inzet'])['aantal gemaakte goalen'].sum().unstack()
plot = bar_data.plot.bar(title='Aantal Goalen Per Positie en Inzet')
plot.set_xlabel('Posities per Inzet')  # titel van de x-as
plot.set_ylabel('Aantal Gemaakte Goalen')  # titel van de y-as
fig = plot.get_figure()
fig.tight_layout()  # groote van diagram aanpassen aan groote van export foto
fig.savefig('staaf_diagram.png')

# 6 - Gemiddelde en modus van de kolom 'aantal gemaakte goalen' per positie    TODO ------------------------------
gemiddelde = data['aantal gemaakte goalen'].mean()
modus = data['aantal gemaakte goalen'].mode()
print("gemiddelde: ", round(float(gemiddelde), 2))
print("modus: ", round(float(modus[0]), 20))
print("\n")

# 7 - Kwartiel 1 en standaardafwijking van kolom 'gewicht'
standaardafwijking = data['gewicht'].std()
kwartiel1 = data['gewicht'].quantile(0.25)
print("standaardafwijking: ", round(float(standaardafwijking), 2))
print("kwartiel 1:", round(float(kwartiel1), 2))
print("\n")

# 8 - verband tussen positie op het veld en het aantal goals gescoord
# groeperen op positie en som van de aantal gemaakte goalen
bar_data2 = data.groupby('positie')['aantal gemaakte goalen'].sum().to_frame()
# sorteren van meest naar minst gescoorde goals per positie
bar_data2 = bar_data2.sort_values(by='aantal gemaakte goalen', ascending=False)
plot = bar_data2.plot.bar(title='Aantal gemaakte goalen per Positie')

# waardes tonen op het diagram
for i in plot.patches:
    plot.text(i.get_x()+.08, i.get_height()+.5, str(round(i.get_height())), fontsize=12, color='black')

fig = plot.get_figure()
fig.tight_layout()  # groote van diagram aanpassen aan groote van export foto
fig.savefig('bar_aantal_gemaakte_goalen_per_positie.png')

# 9 - cirkeldiagram inzet
# groeperen per inzet en count van aantal inzet
pie_data = data.groupby(['inzet'])['inzet'].count().to_frame().rename(columns={'inzet':'counts'}).reset_index()
plot = pie_data.plot.pie(y='counts', labels=pie_data['inzet'], legend=False)
fig = plot.get_figure()
fig.tight_layout()  # groote van diagram aanpassen aan groote van export foto
fig.savefig('circle.png')

# 10 - boxplot vergelijking posities (linkervleugel, rechtervleugel, piloot)
# selecteer specifieke posities
box_data = data.loc[data['positie'].isin(['linkervleugel', 'rechtervleugel', 'piloot'])]
plot = box_data.boxplot(by='positie', column=['aantal gemaakte goalen'], figsize=(8, 6))
plot.set_title("Aantal Gemaakte Goals per Positie", fontsize=16)  # titel van diagram
plot.set_xlabel("Positie", fontsize=14)  # titel van de x-as
plot.set_ylabel("Aantal gemaakte goals", fontsize=14)   # titel van de y-as
plt.suptitle("")  # suptitle leegmaken
fig = plot.get_figure()
fig.tight_layout()  # groote van diagram aanpassen aan groote van export foto
fig.savefig('boxplot.png')

# toon alle gemaakte diagrammen in pycharm editor
plt.show()



