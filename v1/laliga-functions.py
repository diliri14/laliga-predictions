import pandas as pd
from datetime import datetime
from scipy.stats import poisson
import numpy as np

'''
Lee las páginas de Wikipedia que contienen los resultados de los juegos de La Liga en cada año según se especifique
Genera un archivo llamado historical_results.csv con columnas 'Local', 'Visitante', 'Temporada', 'GolesLocal', 'GolesVisitante'
'''

# Extraer la data de la web
# Leer las páginas de Wikipedia que contienen los resultados de los juegos de La Liga en cada año


def get_historical_data(years):
    wiki = 'https://en.wikipedia.org/wiki/'
    # Crear un diccionario con la temporada y la tabla de resultados
    historical_data = {"season": [], "data": []}

    # Limpiar la data
    # Agregar columna de temporada en historical_data y unificar el nombre de los equipos en los df
    for year in years:
        historical_data['season'].append(year)
        historical_data['data'].append(
            pd.read_html(f'{wiki}{year}_La_Liga')[5])

    # Agregar una columna con la temporada en cada juego
    for i in range(len(historical_data['data'])):
        season = historical_data['season'][i]
        data = historical_data['data'][i]
        data.insert(0, 'season', season)

    # Cambiar los nombres de las columnas
    for i in range(len(historical_data['data'])):
        short_names = historical_data['data'][i].columns[2:]
        long_names = historical_data['data'][i].iloc[:, 1]
        dict_team_names = dict(zip(short_names, long_names))

        # Renombrar las filas utilizando el diccionario generado long,shorts
        # historical_data['data'][i].replace(dict_team_names, inplace=True)
        # Renombrar las columnas utilizando el diccionario generado shorts,longs
        historical_data['data'][i].rename(
            columns=dict_team_names, inplace=True)

        # Establecer la primera fila como índice y cambiar el nombre de la columna "Unnamed: 0" por "Equipo"
        historical_data['data'][i] = historical_data['data'][i].set_index(
            historical_data['data'][i].columns[1]).rename_axis("Equipo")

    # Crear un nuevo dataframe que muestre los resultados en el formato deseado 'Local', 'Resultado', 'Visitante', 'Temporada
    historical_results = pd.DataFrame(columns=[
        'Local', 'Resultado', 'Visitante', 'Temporada', 'GolesLocal', 'GolesVisitante'])

    for i in range(len(historical_data['data'])):
        historical_data_filtered = historical_data['data'][i].iloc[:, 0:]
        for index, row in historical_data_filtered.iterrows():
            for col_name, value in row.iloc[1:].items():
                # Obtener el resultado del partido en formato "goles_local - goles_visitante"
                score = value.strip()
                # Obtener el nombre del equipo visitante
                away_team = col_name
                # Obtener el nombre del equipo local
                local_team = index
                # Obtener la temporada
                season = historical_data['data'][i].iloc[0, 0]
                # Crear un nuevo dataframe con la fila actual
                new_row = pd.DataFrame({'Local': [local_team], 'Resultado': [
                    score], 'Visitante': [away_team], 'Temporada': [season]})
                # Concatenar el nuevo dataframe con el dataframe de resultados existente
                historical_results = pd.concat(
                    [historical_results, new_row], ignore_index=True)

    # Remover resultados entre los mismos equipos
    historical_results = historical_results[historical_results['Local']
                                            != historical_results['Visitante']]
    # Separar la columna de resultado en goles local / goles visitante
    historical_results[['GolesLocal', 'GolesVisitante']
                       ] = historical_results['Resultado'].str.split('–', expand=True)

    # Eliminar la columna resultado
    historical_results.drop('Resultado', axis=1, inplace=True)

    # Convertir las columnas de GolesLocal y GolesVisitante a tipo número
    historical_results = historical_results.astype(
        {'GolesLocal': int, 'GolesVisitante': int})
    # Exportar a un archivo .csv
    historical_results.to_csv('historical_results.csv', index=False)

    return historical_results


'''
Se ejecuta:
historical_results = get_historical_data(
    ['2017-18', '2018-19', '2019-20', '2020-21', '2021-22'])
'''


'''
Lee las páginas de Wikipedia que contienen los resultados de los juegos de La Liga de esta temporada 2022-23
Genera un archivo llamado current_results.csv con columnas 'Local', 'Visitante', 'Fecha', 'GolesLocal', 'GolesVisitante'
'''


def get_current_results():
    # Leer las tablas desde la URL
    url = 'https://es.m.wikipedia.org/wiki/Primera_Divisi%C3%B3n_de_Espa%C3%B1a_2022-23'
    all_tables = pd.read_html(url)

    # Seleccionar solo las tablas que van del índice 14 al 52 menos la 19 que son las jornadas de la temporada 22-23
    selected_tables = all_tables[14:53]
    # Elimina la tabla de la posición 19
    selected_tables.pop(19)

    # Organizar la data
    current_results = pd.DataFrame()
    for table in selected_tables:
        # Eliminar el primer nivel del MultiIndex de las columnas
        table.columns = table.columns.droplevel(0)
        # Escoger solo las columnas que nos interesan
        table = table[['Local', 'Resultado', 'Visitante', 'Fecha']]
        current_results = pd.concat(
            [current_results, table], ignore_index=True)

    # Separar la columna de resultado en goles local / goles visitante
    current_results[['GolesLocal', 'GolesVisitante']
                    ] = current_results['Resultado'].str.split('–', expand=True)
    current_results.drop('Resultado', axis=1, inplace=True)

    # Borrar las filas que tienen valores NaN
    current_results = current_results.dropna()

    # Convertir las columnas de GolesLocal y GolesVisitante a tipo número
    current_results = current_results.astype(
        {'GolesLocal': int, 'GolesVisitante': int})

    # Crear función para convertir la fecha
    def date_conversion(date_str):
        month_dict = {
            'enero': 1,
            'febrero': 2,
            'marzo': 3,
            'abril': 4,
            'mayo': 5,
            'junio': 6,
            'julio': 7,
            'agosto': 8,
            'septiembre': 9,
            'octubre': 10,
            'noviembre': 11,
            'diciembre': 12
        }
        date_list = date_str.split()
        day = date_list[0]
        month_str = date_list[2]
        month = month_dict[month_str]
        if month <= 7:
            year = 2023
        else:
            year = 2022
        fecha = datetime(year, month, int(day))
        return fecha.strftime('%d/%m/%Y')

    # Aplicar la función a la columna Fecha
    current_results['Fecha'] = current_results['Fecha'].apply(date_conversion)

    current_results['Fecha'] = pd.to_datetime(
        current_results['Fecha'], format='%d/%m/%Y')
    current_results

    # Extraer el nombre limpio de los equipos que juegan la temporada 2022-23
    wiki = 'https://en.wikipedia.org/wiki/'
    years = '2022-23'
    url = f'{wiki}{years}_La_Liga'

    season_2223 = pd.read_html(url)[2]
    teams_2223 = list(season_2223['Team'])

    # Extraer el nombre a sustituir de los equipos del dataframe
    teams_2223_to_change = current_results[[
        'Local', 'Visitante']].values.flatten()
    teams_2223_to_change = list(pd.unique(teams_2223_to_change))

    # Arreglo con los nuevos nombres de los equipos
    renaming_dict = {'C. A. Osasuna': 'Osasuna',
                     'Sevilla F. C.': 'Sevilla',
                     'R. C. Celta de Vigo': 'Celta Vigo',
                     'R. C. D. Espanyol': 'Espanyol',
                     'Real Valladolid C. F.': 'Valladolid',
                     'Villarreal C. F.': 'Villarreal',
                     'F. C. Barcelona': 'Barcelona',
                     'Rayo Vallecano': 'Rayo Vallecano',
                     'Cádiz C. F.': 'Cádiz',
                     'Real Sociedad': 'Real Sociedad',
                     'Valencia C. F.': 'Valencia',
                     'Girona F. C.': 'Girona',
                     'U. D. Almería': 'Almería',
                     'Real Madrid C. F.': 'Real Madrid',
                     'Athletic Club': 'Athletic Bilbao',
                     'R. C. D. Mallorca': 'Mallorca',
                     'Getafe C. F.': 'Getafe',
                     'Atlético de Madrid': 'Atlético Madrid',
                     'Real Betis': 'Real Betis',
                     'Elche C. F.': 'Elche',
                     'Valencia F. C.': 'Valencia'}

    # Sustituir los nombres en el dataframe
    current_results.replace(renaming_dict, inplace=True)

    # Exportar a un archivo .csv
    current_results.to_csv('current_results.csv', index=False)
    return current_results


'''
Calcula la fuerza goleadora de los equipos como locales o visitantes a partir de una tabla con columnas 'Local', 'Visitante', 'Temporada', 'GolesLocal', 'GolesVisitante'.
Devuelve los df de local y visitante y los promedios totales de goles anotados por locales y visitantes
'''


def team_strength(df_historical_results):

    # # Creando nuevos df de local y visitante
    # df_home = df_historical_results[[
    #     'Local', 'GolesLocal', 'GolesVisitante', 'Temporada']]
    # df_away = df_historical_results[[
    #     'Visitante', 'GolesVisitante', 'GolesLocal', 'Temporada']]

    # Creando nuevos df de local y visitante
    df_home = df_historical_results[[
        'Local', 'GolesLocal', 'GolesVisitante']]
    df_away = df_historical_results[[
        'Visitante', 'GolesVisitante', 'GolesLocal']]

    # Dividiendo df en local y visitante
    df_home = df_home.rename(columns={
                             'Local': 'Equipo', 'GolesLocal': 'GolesAnotados', 'GolesVisitante': 'GolesRecibidos'})
    df_away = df_away.rename(columns={
                             'Visitante': 'Equipo', 'GolesVisitante': 'GolesAnotados', 'GolesLocal': 'GolesRecibidos'})

    # Calculando promedios totales de goles anotados por locales y visitantes
    # goles anotados local = gples encajados visitante
    home_scored = df_home['GolesAnotados'].mean()
    # goles anotados visitante = gples encajados local
    away_scored = df_away['GolesAnotados'].mean()

    # Calculando promedios de goles anotados y encajados por equipo local, en función del promedio total de goles anotados y encajados de local por todos los equipos
    df_homestrength = df_home.groupby(['Equipo']).mean()
    df_homestrength['PromedioGolesAnotados'] = df_homestrength['GolesAnotados'] / home_scored
    df_homestrength['PromedioGolesRecibidos'] = df_homestrength['GolesRecibidos'] / away_scored
    # Eliminar las filas que no necesitamos
    df_homestrength.drop(
        ['GolesAnotados', 'GolesRecibidos'], axis=1, inplace=True)

    # Calculando promedios de goles anotados y encajados por equipo visitante en función del promedio total de goles anotados y encajados de visitante
    df_awaystrength = df_away.groupby(['Equipo']).mean()
    df_awaystrength['PromedioGolesAnotados'] = df_awaystrength['GolesAnotados'] / away_scored
    df_awaystrength['PromedioGolesRecibidos'] = df_awaystrength['GolesRecibidos'] / home_scored
    # Eliminar las filas que no necesitamos
    df_awaystrength.drop(
        ['GolesAnotados', 'GolesRecibidos'], axis=1, inplace=True)

    # Imprimiendo dataframes
    return (df_homestrength, df_awaystrength, home_scored, away_scored)


'''
Calcula la probabilidad de Poisson.
Devuelve el % ganar del local, el % de empate y el % de ganar del visitante
'''


def prob_poisson(local, visitante, df_homestrength, df_awaystrength, home_scored, away_scored):

    # Definiendo la función
    if local in df_homestrength.index and visitante in df_awaystrength.index:
        # goals_scored * goals_conceded
        home_xgoals = df_homestrength.at[local, 'PromedioGolesAnotados'] * \
            df_awaystrength.at[visitante,
                               'PromedioGolesRecibidos'] * home_scored
        away_xgoals = df_awaystrength.at[visitante, 'PromedioGolesAnotados'] * \
            df_homestrength.at[local, 'PromedioGolesRecibidos'] * away_scored
        # return (goles_local, goles_visitante)
        prob_draw = 0
        prob_home = 0
        prob_away = 0

        for x in range(0, 10):  # Goles equipo local
            for y in range(0, 10):  # Goles equipo visitante
                p = poisson.pmf(x, home_xgoals) * poisson.pmf(y, away_xgoals)
                if x == y:
                    prob_draw += p * 100
                elif x > y:
                    prob_home += p * 100
                else:
                    prob_away += p * 100

    # Imprimiendo probabilidades
    return (f"{prob_home:.2f}%", f"{prob_draw:.2f}%", f"{prob_away:.2f}%")


'''
Se ejecuta:
prob_poisson('Barcelona', 'Real Madrid', df_homestrength,
             df_awaystrength, home_scored, away_scored)
'''

'''
Calcula la probabilidad según el enfrentamiento directo de los equipos.
Devuelve el % ganar del local, el % de empate y el % de ganar del visitante
'''


def prob_headtohead(local, visitante, df_results):
    if ((df_results['Local'] == local).any() and (df_results['Local'] == visitante).any()):
        # sacar todos los partidos previos entre equipos
        matches1 = df_results.loc[(df_results['Local'] == local) & (
            df_results['Visitante'] == visitante)]
        matches2 = df_results.loc[(df_results['Local'] == visitante) & (
            df_results['Visitante'] == local)]
        total_matches = df_results.loc[((df_results['Local'] == local) & (df_results['Visitante'] == visitante)) |
                                       ((df_results['Local'] == visitante) & (df_results['Visitante'] == local)), :]

        # Creamos una copia del DataFrame
        home_results = matches1.copy()
        away_results = matches2.copy()

        prob_home = 0
        prob_away = 0
        prob_draw = 0

        # Cuando el equipo local juega de local:
        home_results.loc[home_results["GolesLocal"] >
                         home_results["GolesVisitante"], "ResultadoLocal"] = "Local"
        home_results.loc[home_results["GolesLocal"] ==
                         home_results["GolesVisitante"], "ResultadoLocal"] = "Empate"
        home_results.loc[home_results["GolesLocal"] <
                         home_results["GolesVisitante"], "ResultadoLocal"] = "Visitante"
        # Cuando el equipo visitante juega de visitante:
        away_results.loc[away_results["GolesVisitante"] >
                         away_results["GolesLocal"], "ResultadoVisitante"] = "Visitante"
        away_results.loc[away_results["GolesVisitante"] ==
                         away_results["GolesLocal"], "ResultadoVisitante"] = "Empate"
        away_results.loc[away_results["GolesVisitante"] <
                         away_results["GolesLocal"], "ResultadoVisitante"] = "Local"

        # contar el número de partidos por resultado
        home_results1 = home_results.groupby(
            ["Local", "ResultadoLocal"]).size() * 2
        away_results1 = away_results.groupby(
            ["Visitante", "ResultadoVisitante"]).size()

        prob_home = ((home_results1.get((local, "Local"), 0) + away_results1.get(
            (local, "Visitante"), 0)) / (len(home_results) * 2 + len(away_results))) * 100
        prob_draw = ((home_results1.get((local, "Empate"), 0) + away_results1.get(
            (local, "Empate"), 0)) / (len(home_results) * 2 + len(away_results))) * 100
        prob_away = ((home_results1.get((local, "Visitante"), 0) + away_results1.get(
            (local, "Local"), 0)) / (len(home_results) * 2 + len(away_results))) * 100

        return (f"{prob_home:.2f}%", f"{prob_draw:.2f}%", f"{prob_away:.2f}%")


def get_teams():

    teams = ['Real Madrid',
             'Barcelona',
             'Atlético Madrid',
             'Sevilla',
             'Real Betis',
             'Real Sociedad',
             'Villarreal',
             'Athletic Bilbao',
             'Valencia',
             'Osasuna',
             'Celta Vigo',
             'Rayo Vallecano',
             'Elche',
             'Espanyol',
             'Getafe',
             'Mallorca',
             'Cádiz',
             'Almería',
             'Valladolid',
             'Girona']
    return teams


'''
Se ejecuta:
current_results = get_current_results()
'''

'''
Devuelve los últimos N partidos de un equipo en particular
'''


def last_matches_team(team, matches_num, df_current_results):

    # Filtrar los partidos del equipo especificado
    last_matches = df_current_results[(df_current_results['Local'] == team) | (
        df_current_results['Visitante'] == team)]

    # Ordenar los partidos por fecha descendente
    last_matches = last_matches.sort_values(by='Fecha', ascending=False)

    # Seleccionar los últimos (matches_num) partidos
    last_matches = last_matches.head(matches_num).reset_index(drop=True)

    # Asignar un peso a cada partido
    weights = np.exp(np.linspace(0, -1, matches_num))

    # Crear un nuevo DataFrame solo con los pesos
    weights_df = pd.DataFrame(weights, columns=['Pesos'])

    # Unir el nuevo DataFrame de los pesos con el DataFrame de los partidos locales y visitantes
    last_matches = pd.concat([last_matches, weights_df], axis=1)

    # Devolver el DataFrame con los últimos partidos del equipo
    return (last_matches)


'''
Calcula la probabilidad según la forma y resultados actuales de cada equipo.
Devuelve el % ganar del local, el % de empate y el % de ganar del visitante
'''


def prob_recentform(home, away, matches_num, df_current_results):
    if ((df_current_results['Local'] == home).any() and (df_current_results['Local'] == away).any()):

        # Obtener los últimos partidos de cada equipo
        home_matches = last_matches_team(home, matches_num, df_current_results)
        away_matches = last_matches_team(away, matches_num, df_current_results)

        # Cuando el equipo local juega de local:
        home1 = home_matches.loc[home_matches['Local'] == home]
        home_matches1 = home1.copy()
        home_matches1.loc[home_matches1["GolesLocal"] >
                          home_matches1["GolesVisitante"], "Resultado"] = "Local"
        home_matches1.loc[home_matches1["GolesLocal"] ==
                          home_matches1["GolesVisitante"], "Resultado"] = "Empate"
        home_matches1.loc[home_matches1["GolesLocal"] <
                          home_matches1["GolesVisitante"], "Resultado"] = "Visitante"
        home_matches1['Pesos'] = home_matches1['Pesos'] * 2
        home_results1 = home_matches1.groupby('Resultado')['Pesos'].sum()

        # Cuando el equipo local juega de visitante:
        home2 = home_matches.loc[home_matches['Visitante'] == home]
        home_matches2 = home2.copy()
        home_matches2.loc[home_matches2["GolesLocal"] >
                          home_matches2["GolesVisitante"], "Resultado"] = "Local"
        home_matches2.loc[home_matches2["GolesLocal"] ==
                          home_matches2["GolesVisitante"], "Resultado"] = "Empate"
        home_matches2.loc[home_matches2["GolesLocal"] <
                          home_matches2["GolesVisitante"], "Resultado"] = "Visitante"
        home_matches2['Pesos'] = home_matches2['Pesos']
        home_results2 = home_matches2.groupby('Resultado')['Pesos'].sum()

        # Cuando el equipo visitante juega de visitante:
        away1 = away_matches.loc[away_matches['Visitante'] == away]
        away_matches1 = away1.copy()
        away_matches1.loc[away_matches1["GolesLocal"] >
                          away_matches1["GolesVisitante"], "Resultado"] = "Local"
        away_matches1.loc[away_matches1["GolesLocal"] ==
                          away_matches1["GolesVisitante"], "Resultado"] = "Empate"
        away_matches1.loc[away_matches1["GolesLocal"] <
                          away_matches1["GolesVisitante"], "Resultado"] = "Visitante"
        away_matches1['Pesos'] = away_matches1['Pesos'] * 2
        away_results1 = away_matches1.groupby('Resultado')['Pesos'].sum()

        # Cuando el equipo visitante juega de local:
        away2 = away_matches.loc[away_matches['Local'] == away]
        away_matches2 = away2.copy()
        away_matches2.loc[away_matches2["GolesLocal"] >
                          away_matches2["GolesVisitante"], "Resultado"] = "Local"
        away_matches2.loc[away_matches2["GolesLocal"] ==
                          away_matches2["GolesVisitante"], "Resultado"] = "Empate"
        away_matches2.loc[away_matches2["GolesLocal"] <
                          away_matches2["GolesVisitante"], "Resultado"] = "Visitante"
        away_matches2['Pesos'] = away_matches2['Pesos']
        away_results2 = away_matches2.groupby('Resultado')['Pesos'].sum()

        home_prob = home_results1.get('Local', 0) + home_results2.get(
            'Visitante', 0) + away_results1.get('Local', 0) + away_results2.get('Visitante', 0)
        draw_prob = home_results1.get('Empate', 0) + home_results2.get(
            'Empate', 0) + away_results1.get('Empate', 0) + away_results2.get('Empate', 0)
        away_prob = home_results1.get('Visitante', 0) + home_results2.get(
            'Local', 0) + away_results1.get('Visitante', 0) + away_results2.get('Local', 0)

        total_prob = home_prob + draw_prob + away_prob

        prob_home = (home_prob / total_prob) * 100
        prob_draw = (draw_prob / total_prob) * 100
        prob_away = (away_prob / total_prob) * 100

        return (f"{prob_home:.2f}%", f"{prob_draw:.2f}%", f"{prob_away:.2f}%")


def get_total_prediction(prob_home1, prob_draw1, prob_away1, prob_home2, prob_draw2, prob_away2, prob_home3, prob_draw3, prob_away3):

    # Obtiene el promedio de los resultados
    prob_home = (float(prob_home1.strip(
        '%')) + float(prob_home2.strip('%')) + float(prob_home3.strip(
            '%'))) / 3
    prob_draw = (float(prob_draw1.strip(
        '%')) + float(prob_draw2.strip('%')) + float(prob_draw3.strip(
            '%'))) / 3
    prob_away = (float(prob_away1.strip(
        '%')) + float(prob_away2.strip('%')) + float(prob_away3.strip(
            '%'))) / 3

    return (f"{prob_home:.2f}%", f"{prob_draw:.2f}%", f"{prob_away:.2f}%")
