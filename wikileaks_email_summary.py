import requests
import time

import networkx as nx

from bs4 import BeautifulSoup

BASE_URL = 'https://wikileaks.org/clinton-emails/?q=&mfrom=&mto=&title=&notitle=&date_from=1995-03-02&date_to=2014-12-14&nofrom=&noto=&count=200&sort=0'

def main():
    G = nx.DiGraph()
    for i in range(1,153):
        print 'Fetching page {}'.format(i)
        response = requests.get('{}&page={}'.format(BASE_URL, i))

        if not response.ok:
            print 'Error fetching page: {}'.format(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table',
            {'class' : 'table table-striped search-result'})

        for row in table.find_all('tr')[1:]:
            mail_from = row.find_all('td')[3].text.strip()
            mail_to = row.find_all('td')[4].text.strip()

            if not mail_from:
                mail_from = 'Unknown'

            if not mail_to:
                mail_to = 'Unknown'

            G.add_node(mail_from)
            G.add_node(mail_to)

            if G.has_edge(mail_from, mail_to):
                G[mail_from][mail_to]['weight'] += 1
            else:
                G.add_edge(mail_from, mail_to, weight=1)

        # Don't be rude.
        time.sleep(.5)

    nx.write_gexf(G, 'emails.gexf')
    

if __name__ == '__main__':
    main()
