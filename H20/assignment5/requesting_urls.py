import requests as req

def get_html(url, params={}, output=None):
    """Fetch the content of a website of choice using requests.

    Args:
        url (str): the url to the website whose content you want to get
        params (dict, optional): 
            key-value pairs to describe the data you are interested in
        output (str, optional): path to file to which the data will be saved

    Returns:
        resp (Response): the response from the website

    """
    resp = req.get(url, params=params)
    if output:
        with open(output + '.txt', 'w') as outfile:
            endl = '\n'
            outfile.write(resp.url + endl)
            outfile.write(resp.text + endl)
    return resp

if __name__ == '__main__':
    websites = [
            ['https://en.wikipedia.org/wiki/Studio_Ghibli', {}, 'Studio_Ghibli'],
            ['https://en.wikipedia.org/wiki/Star_Wars', {}, 'Star_Wars'],
            ['https://en.wikipedia.org/wiki/Dungeons_%26_Dragons', {}, 'D_n_D'],
            ['https://en.wikipedia.org/w/index.php', 
                {'title': 'MainPage', 'action': 'info'}, 
                'wiki1'
            ],
            ['https://en.wikipedia.org/w/index.php', 
                {'title': 'HurricaneGonzalo', 'oldid': '983056166'}, 
                'wiki2'
            ]
    ]

    path = 'requesting_urls/'
    for url, params, output in websites:
        get_html(url, params, path + output)
