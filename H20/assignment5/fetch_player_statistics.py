import re
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from requesting_urls import get_html
from filter_urls import find_urls

def navigate_to_table(soup, sect_type, sect_id):
    """Parse the beautiful soup for a tag of a specific type with a specific id
    and then return the table in that section.

    Args:
        soup (BeautifulSoup): the soup to parse
        sect_type (str): the tag to search for (e.g. 'h2', 'h3', 'table')
        sect_id (str): the id of that section

    Returns:
        soup_table (BeautifulSoup): the soup of the table in the desired section

    """
    soup = soup.find(sect_type)
    while not soup.find('span', {'id': sect_id}):
        soup = soup.find_next(sect_type)
    soup_table = soup.find_next('table')
    return soup_table

def extract_urls(url):
    """Extract a table showing the teams that made it to the conference 
    semifinals of the NBA playoffs.

    Args:
        url (str): url to the Wikipedia page of the playoffs

    Returns:
        table (2D list of str): table of the teams which made it
        urls (list of str): the urls to the Wikipedia page of the teams which made it

    """
    resp = get_html(url)
    base = re.match(r'https?://\w+(?:\.\w+)*/', url).group(0)

    soup = BeautifulSoup(resp.text, 'html.parser')
    soup_table = navigate_to_table(soup, 'h2', 'Bracket')

    team_urls = {}
    seed_pattern = re.compile(r'[EW]\d')
    for tr in soup_table.find_all('tr')[2:]:
        for col, td in enumerate(tr.find_all('td')):
            text = td.text.strip().strip('*')
            if col < 2 and text:
                break

            seed_match = bool(seed_pattern.match(text))
            if col == 2 and not seed_match:
                break

            if col > 3:
                break

            if text:
                if not seed_match:
                    url = find_urls(str(td), base)[0]
                    team_urls[text] = url
    return team_urls

def extract_players(url):
    """Identify all the players that played for a specific team a speficic 
    season by searching through the Wikipedia article whose url is given as 
    input.

    Args:
        url (str): url to the Wikipedia page that will be searched through

    Returns:
        player_urls (list of str): 
            links to the websites of all the players if the team

    """
    resp = get_html(url)
    wiki_base = re.match(r'https?://\w+(?:\.\w+)*/', url).group(0)
    soup = BeautifulSoup(resp.text, 'html.parser')
    soup_table = navigate_to_table(soup, 'h2', 'Roster')
    soup_table = soup_table.find('table')
    player_urls = {}
    for tr in soup_table.find_all('tr')[1:]:            # skip the header row
        player_td = tr.find_all('td')[2]                # names are third col
        url = find_urls(str(player_td), wiki_base)[0]   # list with one url
        player_urls[player_td.text.strip()] = url       # name: url
    return player_urls

def extract_player_data(url, name, team):
    """Extract points per game, blocks per game, and rebounds per game for the 
    2019-20 season for the NBA player with the Wikipedia page given as input.

    Args:
        url (str): url to the Wikipedia page of the player

    Returns:
        player_data (dict): dictionary containing the player data
            keys (str): {'ppg', 'bpg', 'rpg'}
            values (float)

    """
    resp = get_html(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # had trouble matching the - from Wiki, 
    # so matching any character between the numbers
    year_pattern = re.compile(r'2019.20')

    cols = {'rpg': 8, 'bpg': 11, 'ppg': 12}
    player_data = {
            'name': name, 
            'team': team, 
            'ppg': 0.0      # default if other data is not found
    }

    soup_table = None
    tags = ['h4', 'h3']
    header_ids = ['Regular_season', 'NBA']
    for header_id in header_ids:
        for tag in tags:
            try:
                soup_table = navigate_to_table(soup, tag, header_id)
                break
            except:
                pass
    if not soup_table:
        print(f'No data for {name} ({team})')
        return player_data

    for tr in soup_table.find_all('tr')[1:]:
        year_data = tr.find_all('td')
        year = year_data[0].text.strip()    # the year/season is in the first col
        is_correct_year = bool(year_pattern.match(year))
        if is_correct_year:
            for attr, col in cols.items():
                value = year_data[col].text.strip()
                try:
                    value = float(value)
                except ValueError:
                    value = 0.0
                player_data[attr] = value
    return player_data

def top_three_players(player_urls, team):
    """Return a list of the top three players of a team sorted by points per game.

    Args:
        player_urls (dict): 
            dictionary of names to urls for the Wikipedia page of that player
        team (str): the team of the player

    Returns:
        sorted_players (list of dicts): list of the dicts representing the top 
            three players in ascending order

    """
    players = []
    for player, player_url in player_urls.items():
        player_data = extract_player_data(player_url, player, team)
        players.append(player_data)
    sorted_players = sorted(players, key=lambda d: d['ppg'])
    return sorted_players[-3:]

def pool_of_players(url):
    """Return a list of the top three players of every team that made it to the 
    second round of the playoffs. The data is collected from Wikipedia, starting
    from the url given as input which should point to the Wikipedia playoff 
    overview of the desired season.

    Args:
        url (str): the url to the Wiki page containing the overview of the NBA 
            playoffs for the desired season

    Returns:
        players (list of dicts): list of dictionaries of length 24, each 
            representing one of the top three players of one of the teams that 
            made it to the second round

    """
    team_urls = extract_urls(url)
    players = []
    for team, team_url in team_urls.items():
        print('Fetching players for', team, '...')
        player_urls = extract_players(team_url)
        players += top_three_players(player_urls, team)
    return players

def plot(players):
    """Plot the performance of the three players from each team. The players are
    grouped together by team.

    Args:
        players (list of dicts): a list of dicttionaries each representing one player

    """
    plt.style.use('seaborn')
    attributes = ['ppg', 'rpg', 'bpg']
    teams = [player['team'] for player in players[::3]]
    x = np.arange(len(teams))
    width = 0.2
    labels = ['Best', '2nd best', '3rd best']
    # get the surnames for ticks
    names = [player['name'].split(',')[0] for player in players]

    xticks = []
    for i, team in enumerate(teams):
        tick = r'$\bf{' + team.replace(' ', '\ ') + ':}$' + '\n' 
        tick += '\n'.join(names[3*i:3*i+3])
        xticks.append(tick)

    for attribute in attributes:
        fig, ax = plt.subplots()
        for i in range(2, -1, -1):
            score = [player[attribute] for player in players[i::3]]
            ax.bar(x + (i - 1)*width, score, width, label=labels[-i-1])
        ax.set_title(attribute.upper() + '\nPlayers are listed left to right')
        ax.set_xticks(x)
        ax.set_xticklabels(xticks, rotation=20)
        ax.legend()
        fig.tight_layout()
        fig.savefig(f'NBA_player_statistics/players_over_{attribute}.png')

if __name__ == '__main__':
    print('1) Download data or \n2) use pre-downloaded?')
    ans = input('1 or 2: ')
    if ans == '1':
        url = 'https://en.wikipedia.org/wiki/2020_NBA_playoffs'
        top_players = pool_of_players(url)
        plot(top_players)
    elif ans == '2':
        top_players = [
            {'name': 'Bledsoe, Eric', 'team': 'Milwaukee', 'ppg': 14.9, 'rpg': 4.6, 'bpg': 0.4},
            {'name': 'Middleton, Khris', 'team': 'Milwaukee', 'ppg': 20.9, 'rpg': 6.2, 'bpg': 0.1},
            {'name': 'Antetokounmpo, Giannis', 'team': 'Milwaukee', 'ppg': 29.5, 'rpg': 13.6, 'bpg': 1.0},
            {'name': 'Nunn, Kendrick', 'team': 'Miami', 'ppg': 15.3, 'rpg': 2.7, 'bpg': 0.2},
            {'name': 'Adebayo, Bam', 'team': 'Miami', 'ppg': 15.9, 'rpg': 10.2, 'bpg': 1.3},
            {'name': 'Butler, Jimmy\xa0(C)', 'team': 'Miami', 'ppg': 19.9, 'rpg': 6.7, 'bpg': 0.6},
            {'name': 'Brown, Jaylen', 'team': 'Boston', 'ppg': 20.3, 'rpg': 6.4, 'bpg': 0.4},
            {'name': 'Walker, Kemba', 'team': 'Boston', 'ppg': 20.4, 'rpg': 3.9, 'bpg': 0.5},
            {'name': 'Tatum, Jayson', 'team': 'Boston', 'ppg': 23.4, 'rpg': 7.0, 'bpg': 0.9},
            {'name': 'VanVleet, Fred', 'team': 'Toronto', 'ppg': 17.6, 'rpg': 3.8, 'bpg': 0.3},
            {'name': 'Lowry, Kyle', 'team': 'Toronto', 'ppg': 19.4, 'rpg': 5.0, 'bpg': 0.4},
            {'name': 'Siakam, Pascal', 'team': 'Toronto', 'ppg': 22.9, 'rpg': 7.3, 'bpg': 0.9},
            {'name': 'Kuzma, Kyle', 'team': 'LA Lakers', 'ppg': 12.8, 'rpg': 4.5, 'bpg': 0.4},
            {'name': 'James, LeBron', 'team': 'LA Lakers', 'ppg': 25.3, 'rpg': 7.8, 'bpg': 0.5},
            {'name': 'Davis, Anthony', 'team': 'LA Lakers', 'ppg': 26.1, 'rpg': 9.3, 'bpg': 2.3},
            {'name': 'Green, Jeff', 'team': 'Houston', 'ppg': 12.2, 'rpg': 2.9, 'bpg': 0.5},
            {'name': 'Gordon, Eric', 'team': 'Houston', 'ppg': 14.4, 'rpg': 2.0, 'bpg': 0.3},
            {'name': 'Westbrook, Russell', 'team': 'Houston', 'ppg': 27.2, 'rpg': 7.9, 'bpg': 0.4},
            {'name': 'Barton, Will', 'team': 'Denver', 'ppg': 15.1, 'rpg': 6.3, 'bpg': 0.5},
            {'name': 'Murray, Jamal', 'team': 'Denver', 'ppg': 18.5, 'rpg': 4.0, 'bpg': 0.3},
            {'name': 'Jokić, Nikola\xa0(C)', 'team': 'Denver', 'ppg': 19.9, 'rpg': 9.7, 'bpg': 0.6},
            {'name': 'Harrell, Montrezl', 'team': 'LA Clippers', 'ppg': 18.6, 'rpg': 7.1, 'bpg': 1.1},
            {'name': 'George, Paul', 'team': 'LA Clippers', 'ppg': 21.5, 'rpg': 5.2, 'bpg': 0.4},
            {'name': 'Leonard, Kawhi', 'team': 'LA Clippers', 'ppg': 27.1, 'rpg': 7.1, 'bpg': 0.6}
        ]
        plot(top_players)
    else:
        print('Unknown option', ans)
