import re
from bs4 import BeautifulSoup
from requesting_urls import get_html

def extract_events(url):
    """Extracts the data in the date, venue and discipline column of the
    Wikipedia article whose url is given as input argument.

    Args:
        url (str): url to the Wikipedia article

    Returns:
        table (2D list): the table as a nested list (nrows, ncols)

    """
    resp = get_html(url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    soup_table = soup.find('table', {'class': 'wikitable plainrowheaders'})

    # header is the first row
    header = []
    table_header = soup_table.find('tr')
    width = 0
    for header_col in table_header.find_all('th'):
        header.append(header_col.text.strip())
        width += 1

    desired = [
        'date',
        'venue',
        'type'      # discipline
    ]

    indices = [i for i, col in enumerate(header) if col.lower() in desired]
    table = [[col for i, col in enumerate(header) if i in indices]]
    row_corrections = {col_idx: 0 for col_idx in range(width)}

    start_row = 0
    for i, tr in enumerate(soup_table.find_all('tr')):
        row = []
        j = start_row
        if row_corrections[0]:
            row_corrections[0] -= 1

        if not row_corrections[0]:
            start_row = 0

        for td in tr.find_all('td'):
            if j > max(indices):
                break
            row_span = td.get('rowspan')
            col_span = td.get('colspan')
            if row_span:
                row_corrections[j] += int(row_span) - 1
                if col_span and j == 0:
                    start_row = int(col_span)
            elif row_corrections[j]:
                if j in indices:
                    row.append(table[-1][indices.index(j)])
                row_corrections[j] -= 1
                j += 1

            if col_span:
                counter = 0
                while counter < int(col_span) - 1:
                    if j in indices:
                        row.append('')
                    j += 1
                    counter += 1

            if j in indices:
                row.append(td.text.strip())
            j += 1

        if row:     # no need to append an empty list
            table.append(row)

    pattern = re.compile(r'\[nb \d+\]')     # remove som noise 
    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = pattern.sub('', table[i][j])
    return table

def markdown(table, output=None):
    """Return a nicely markdown formatted version of the table given as input.

    Args:
        table (2D list of str): the table for which to create markdown
        output (str, optional): path to file to which the output data will be saved

    Returns:
        markdown (1D list of str): a list of rows in the markdown formatted table

    """
    width = len(table[0])
    for row in table:
        if not len(row) == width:
            raise ValueError('All rows must be of equal length')

    markdown = [' | '.join(table[0] + ['Who Wins?'])]
    markdown += [' | '.join(row + ['']) for row in table[1:]]
    markdown.insert(1, '---' + ' | ---'*(len(table[0]) - 1) + '| ---')
    if output:
        with open(output, 'w') as outfile:
            [outfile.write(line + '\n') for line in markdown]
    return markdown

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup'
    table = extract_events(url)
    markdown(table, 'datetime_filter/betting_slip_empty1.md')

    url = 'https://en.wikipedia.org/wiki/2020%E2%80%9321_FIS_Alpine_Ski_World_Cup'
    table = extract_events(url)
    markdown(table, 'datetime_filter/betting_slip_empty2.md')
