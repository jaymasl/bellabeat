from flask import Flask, render_template
from flask_caching import Cache
from table import format_table_data
from graph import steps_distance_scatterplot, calorie_active_scatterplot, heart_sleep_scatterplot
import plotly.io as pio

app = Flask(__name__)
app.config['DB_PATH'] = 'fitbit.ddb'
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 600
})

@app.route('/')
@cache.cached(timeout=600)
def home():
    return render_template('home.jinja')

@app.route('/insight')
@cache.cached(timeout=600)
def insight():
    return render_template('insight.jinja')

@app.route('/visual')
@cache.cached(timeout=600)
def visual():
    fig0, config0 = steps_distance_scatterplot()
    fig1, config1 = calorie_active_scatterplot()
    fig2, config2 = heart_sleep_scatterplot()

    plot0 = pio.to_html(fig0, full_html=False, config=config0)
    plot1 = pio.to_html(fig1, full_html=False, config=config1)
    plot2 = pio.to_html(fig2, full_html=False, config=config2)

    return render_template('visual.jinja', plot0=plot0, plot1=plot1, plot2=plot2)

@app.route('/recommend')
@cache.cached(timeout=600)
def recommend():
    return render_template('recommend.jinja')

@app.route('/table')
@cache.cached(timeout=600)
def table():
    data = format_table_data()
    return render_template('table.jinja', data=data)

if __name__ == "__main__":
    app.run(debug=True)