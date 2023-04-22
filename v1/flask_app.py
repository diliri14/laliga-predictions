from flask import Flask, render_template, request
import pandas as pd
import laliga_functions


# se importan las librerías y se define la aplicación Flask. También se definen dos variables: years, que contiene una lista de temporadas de la Liga Española, y matches_to_shape, que indica cuántos partidos se consideran para calcular la forma reciente de un equipo.
app = Flask(__name__)

years = ['2017-18', '2018-19', '2019-20', '2020-21', '2021-22']
matches_to_shape = 15


# se cargan los datos históricos y actuales de la Liga Española. Se combinan en un único DataFrame (df_total) y se eliminan dos columnas (Temporada y Fecha). Luego se calcula la fuerza de los equipos utilizando la función team_strength del módulo laliga_functions.
df_past_data = laliga_functions.get_historical_data(years)
# df_current_data = laliga_functions.get_current_results()
# df_past_data = pd.read_csv('historical_results.csv')
df_current_data = pd.read_csv('current_results.csv')

df_total = pd.concat([df_past_data, df_current_data])
df_total = df_total.drop(['Temporada', 'Fecha'], axis=1)
df_homestrength, df_awaystrength, home_scored, away_scored = laliga_functions.team_strength(
    df_total)

# esta función recibe dos equipos como entrada y calcula las probabilidades de victoria, empate o derrota utilizando tres métodos diferentes: Poisson, enfrentamiento directo y forma reciente. Luego calcula una predicción general tomando el promedio de las tres probabilidades calculadas anteriormente.


def get_prediction(local_team, visitor_team):

    win_local, draw, win_visitor = laliga_functions.prob_poisson(
        local_team, visitor_team, df_homestrength, df_awaystrength, home_scored, away_scored)
    win2_local, draw2, win2_visitor = laliga_functions.prob_headtohead(
        local_team, visitor_team, df_total)
    win3_local, draw3, win3_visitor = laliga_functions.prob_recentform(
        local_team, visitor_team, matches_to_shape, df_current_data)

    # Calcula la predicción general como el promedio entre la predicción por Poisson y la predicción por enfrentamiento directo
    general_win_local, general_draw, general_win_visitor = laliga_functions.get_total_prediction(
        win_local, draw, win_visitor, win2_local, draw2, win2_visitor, win3_local, draw3, win3_visitor)
    general_win_local = float(general_win_local.rstrip('%'))
    general_draw = float(general_draw.rstrip('%'))
    general_win_visitor = float(general_win_visitor.rstrip('%'))

    return win_local, draw, win_visitor, win2_local, draw2, win2_visitor, win3_local, draw3, win3_visitor, general_win_local, general_draw, general_win_visitor

# define la ruta principal de la aplicación y se usa para mostrar la página principal (index.html).


@app.route('/', methods=['GET'])
def index():
    if request.method == 'POST':
        local_team = request.form['local_team']
        visitor_team = request.form['visitor_team']
        poisson_win_local, poisson_draw, poisson_win_visitor, headtohead_win_local, headtohead_draw, headtohead_win_visitor = get_prediction(
            local_team, visitor_team)
        return render_template('result.html', local_team=local_team, visitor_team=visitor_team, poisson_win_local=poisson_win_local, poisson_draw=poisson_draw, poisson_win_visitor=poisson_win_visitor, headtohead_win_local=headtohead_win_local, headtohead_draw=headtohead_draw, headtohead_win_visitor=headtohead_win_visitor)
    else:
        teams = laliga_functions.get_teams()
        return render_template('index.html', teams=teams)

# define la ruta '/result', que se utiliza para mostrar los resultados después de que el usuario envíe el formulario.


@app.route('/result', methods=['POST'])
@app.route("/result", methods=["GET", "POST"])
def result():
    # obtiene los datos del formulario de entrada
    local_team = request.form.get("local_team")
    visitor_team = request.form.get("visitor_team")
    # max_goals = int(request.form.get("max_goals"))

    # llama a la función get_prediction para obtener los resultados
    (poisson_win_local, poisson_draw, poisson_win_visitor, headtohead_win_local,
     headtohead_draw, headtohead_win_visitor, shape_win_local, shape_draw, shape_win_visitor, general_win_local, general_draw,
     general_win_visitor) = get_prediction(local_team, visitor_team)

    # calcula las probabilidades
    local_win_probability = round(
        (general_win_local / (general_win_local + general_draw + general_win_visitor)) * 100, 2)
    draw_probability = round(
        (general_draw / (general_win_local + general_draw + general_win_visitor)) * 100, 2)
    visitor_win_probability = round(
        (general_win_visitor / (general_win_local + general_draw + general_win_visitor)) * 100, 2)

    # renderiza la plantilla con los resultados
    return render_template(
        "result.html",
        local_team=local_team,
        visitor_team=visitor_team,
        poisson_win_local=poisson_win_local,
        poisson_draw=poisson_draw,
        poisson_win_visitor=poisson_win_visitor,
        headtohead_win_local=headtohead_win_local,
        headtohead_draw=headtohead_draw,
        headtohead_win_visitor=headtohead_win_visitor,
        shape_win_local=shape_win_local,
        shape_draw=shape_draw,
        shape_win_visitor=shape_win_visitor,
        general_win_local=general_win_local,
        general_draw=general_draw,
        general_win_visitor=general_win_visitor,
        local_win_probability=local_win_probability,
        draw_probability=draw_probability,
        visitor_win_probability=visitor_win_probability
    )


if __name__ == '__main__':
    app.run(debug=True)
