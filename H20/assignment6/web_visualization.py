import pandas as pd
from flask import Flask, render_template, send_from_directory
import altair as alt
import os, tempfile

app = Flask(__name__)

fnames = {
    'all counties': ['all_counties', 'alle fylker'],
    'møre og romsdal': ['more_og_romsdal', 'Møre og Romsdal'],
    'troms og finnmark': ['troms_og_finnmark', 'Troms og finnmark'],
    'vestfold og telemark': ['vestfold_og_telemark', 'Vestfold og Telemark'],
    'trondelag': ['trondelag', 'Trøndelag']
}

counties = ['All counties'] + sorted([
    'Agder',
    'Nordland',
    'Trøndelag',
    'Oslo',
    'Vestfold og Telemark',
    'Innlandet',
    'Rogaland',
    'Vestland',
    'Møre og Romsdal',
    'Troms og Finnmark',
    'Viken'
])


def read_from_file(county, start, end):
    """Read a csv data file of number of reported cases.

    Args:
        county (str): the county whose data should be retrieved
        start (datetime object): start date for data extraction, (with utc=True)
        end (datetime object): end date for data extraction, (with utc=True)

    Returns:
        df (pandas dataframe): the cumulative number reported cases
            and total number of reported cases indexed by date
        county_name (str): the name of the county

    """
    path = 'data'
    county = county.lower()
    if county in fnames:
        fname = fnames[county][0]
        county_name = fnames[county][1]
    else:
        fname = county
        county_name = county.capitalize()
    fname += '.csv'
    fname = os.path.join(path, fname)
    try:
        df = pd.read_csv(fname,
            parse_dates=['Dato'],
            date_parser=lambda col: pd.to_datetime(col, utc=True, dayfirst=True),
        )
    except FileNotFoundError:
        raise FileNotFoundError(f'File not found and unknown keyword: {fname}')
    df = df.sort_values('Dato')     # just in case something is out of order
    mask = ((start <= df.loc[:, 'Dato']) & (df.loc[:, 'Dato'] <= end))
    df = df.loc[mask]
    return df, county_name

def plot_reported_cases(
        county='all counties',
        start=pd.to_datetime('21.02.2020', utc=True, dayfirst=True),
        end=pd.to_datetime('19.11.2020', utc=True, dayfirst=True)
    ):
    """Return a bar plot showing the number of reported Covid cases by day in a
    desired county.

    Args:
        county (str): county for which to plot reported cases
            default: 'all counties'
        start (datetime object): start date for plot, (with utc=True)
            default: 21.02.2020
        end (datetime object): end date for plot, (with utc=True)
            default: 19.11.2020

    Returns:
        plot (altair plot): the desired plot object

    """
    df, county_name = read_from_file(county, start, end)
    plot = alt.Chart(df).mark_bar().encode(
        x=alt.X('Dato'),
        y=alt.Y('Nye tilfeller')
    ).properties(
        title='Coronasmittede i ' + county_name
    )
    return plot

def plot_cumulative_cases(
        county='all counties',
        start=pd.to_datetime('21.02.2020', utc=True, dayfirst=True),
        end=pd.to_datetime('19.11.2020', utc=True, dayfirst=True)
    ):
    """Return a line plot showing the cumulative frequency of reported Covid
    cases by day in a desired county.

    Args:
        county (str): county for which to plot reported cases
            default: 'all counties'
        start (datetime object): start date for plot, (with utc=True)
            default: 21.02.2020
        end (datetime object): end date for plot, (with utc=True)
            default: 19.11.2020


    Returns:
        plot (altair plot): the desired plot object

    """
    df, county_name = read_from_file(county, start, end)
    plot = alt.Chart(df).mark_line().encode(
        x=alt.X('Dato'),
        y=alt.Y('Kumulativt antall')
    ).properties(
        title='Coronasmittede i ' + county_name
    )
    return plot

def plot_both(
        county='all counties',
        start=pd.to_datetime('21.02.2020', utc=True, dayfirst=True),
        end=pd.to_datetime('19.11.2020', utc=True, dayfirst=True)
    ):
    """Return a plot of both the number of new cases and the cumulative
    frequency of Covid infection by day in a desired county.

    Args:
        county (str): county for which to plot reported cases
            default: 'all counties'
        start (datetime object): start date for plot
            default: 21.02.2020
        end (datetime object): end date for plot
            default: 19.11.2020

    Returns:
        combined (altair plot): the desired plot object

    """
    df, county_name = read_from_file(county, start, end)
    base = alt.Chart(df).encode(
        x=alt.X('Dato')
    ).properties(
        title='Coronasmittede i ' + county_name
    )

    red = '#db0404'
    blue = '#5276A7'

    reported = base.mark_bar(color=blue).encode(
        y=alt.Y('Nye tilfeller',
        axis=alt.Axis(title='Nye tilfeller per dag', titleColor=blue)),
        tooltip=['Dato', 'Nye tilfeller', 'Kumulativt antall']
    ).interactive()

    cumulative = base.mark_line(color=red).encode(
        y=alt.Y('Kumulativt antall', axis=alt.Axis(titleColor=red)),
        tooltip=['Dato', 'Nye tilfeller', 'Kumulativt antall']
    ).interactive()

    combined = alt.layer(reported, cumulative).resolve_scale(
        y = 'independent'
    )

    return combined

@app.route('/')
def start_page():
    """Return the html of the start page.

    Returns:
        (str): the html code of the start page

    """
    return render_template('start_page.html')

@app.route('/reported_cases')
def plot_reported_cases_html():
    """Return the html of the reported cases page.

    Returns:
        (str): the html code of the reported cases page

    """
    return render_template('reported_cases.html')

@app.route('/reported_cases.json')
def plot_reported_cases_json():
    """Call the plot_reported_cases function to create the plot showing the
    number of reported cases by day. Return the json data for the plot.

    Returns:
        (str): the json data of the plot

    """
    plot = plot_reported_cases()
    tmp = tempfile.NamedTemporaryFile(suffix='.json')
    plot.save(tmp.name)
    with open(tmp.name, 'r') as infile:
        return infile.read()

@app.route('/cumulative_cases')
def plot_cumulative_cases_html():
    """Return the html of the cumulative cases page.

    Returns:
        (str): the html code of the cumulative cases page

    """
    return render_template('cumulative_cases.html')

@app.route('/cumulative_cases.json')
def plot_cumulative_cases_json():
    """Call the plot_cumulative_cases function to create the plot showing the
    cumulative frequency of number of infected by day. Return the json data for
    the plot.

    Returns:
        (str): the json data of the plot

    """
    plot = plot_cumulative_cases()
    tmp = tempfile.NamedTemporaryFile(suffix='.json')
    plot.save(tmp.name)
    with open(tmp.name, 'r') as infile:
        return infile.read()

@app.route('/plot_both')
def plot_both_html():
    """Return the html of the page with both plots.

    Returns:
        (str): the html code of the page with both plots

    """
    return render_template('plot_both.html', counties=counties)

@app.route('/plot_both.json')
def plot_both_json():
    """Call the plot_both function to create the plot showing both the number
    of reported cases by day and the cumulative frequency of number of infected
    by day. Return the json data for the plot.

    Returns:
        (str): the json data of the plot

    """
    plot = plot_both()
    tmp = tempfile.NamedTemporaryFile(suffix='.json')
    plot.save(tmp.name)
    with open(tmp.name, 'r') as infile:
        return infile.read()

@app.route('/reported_cases_files/<script>')
@app.route('/cumulative_cases_files/<script>')
@app.route('/plot_both_files/<script>')
def load_script(script):
    """Return the vega scripts used to display the plots.

    Args:
        script (str): the name of the desired script

    Returns:
        (str): the desired script

    """
    with open(f'templates/scripts/{script}', 'r') as infile:
        return infile.read()

@app.route('/favicon.ico')
def favicon():
    """Display a favicon for the page.

    """
    # not sure if this works
    # the favicon is displayed on my computer, but changing this code seems to
    # have delayed effects making it hard to figure out
    return send_from_directory(os.path.join(app.root_path, 'static'),
                        'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
