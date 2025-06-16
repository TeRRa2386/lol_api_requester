from flask import Flask, render_template, request
from classes import *
import requests

app = Flask(__name__)
app.jinja_env.cache = {}


response = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
response.raise_for_status()
lol_version = response.json()[0]


# ------------ #

def player_data_filter(top_10_data, region, version):

    top_10_list = []

    for player in top_10_data:
        top_player= LolPlayer(region=region,
                              puuid=player['puuid'],
                              leaguepoints=player['leaguePoints'],
                              wins=player['wins'],
                              losses=player['losses'])
        top_player.get_player_info(version)
        top_10_list.append(top_player)

    return top_10_list


# ------------ #


@app.route('/', methods=['GET', 'POST'])
def index():

    lol_connection = LolConnection()

    if request.method == 'POST':

        region = request.form.get('region')
        tier = request.form.get('tier')
        queue = request.form.get('queue')
        division = request.form.get('division')

        lol_connection.get_urls(region=region, tier=tier, queue=queue, division=division)
        lol_connection.get_data()

        top_10_list = player_data_filter(lol_connection.top_data, region, lol_version)
        server_status = True if not lol_connection.region_data['maintenances'] else False

        return render_template('index.html', top_10=top_10_list, server_on=server_status)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)