import requests
from bs4 import BeautifulSoup
import helpers


class QuoteFactory:

    def __init__(self, url='http://quotes.toscrape.com/'):
        self.quotes = 0
        self.base_url = url
        self.current_url = url
        self.quotes = []

    def __repr__(self):
        return f'a list of {len(self.quotes)} quotes.'

    @helpers.with_logging
    def get_quotes_from_single_page(self, url):
        res = requests.get(url).text
        soup = BeautifulSoup(res, 'html.parser')
        quote_list = soup.select('.quote')
        for q in quote_list:
            text = q.select('.text')[0].string
            author = q.select('.author')[0].string
            link_to_author = q.select('a')[0]['href']
            link_to_author = self.base_url + \
                link_to_author[1:]  # cut extra '/'
            new_quote = Quote(text=text, author=author,
                              link_to_author=link_to_author)
            self.quotes.append(new_quote)

    @helpers.with_logging
    def get_next_page_url(self, current_url):
        res = requests.get(current_url).text
        soup = BeautifulSoup(res, 'html.parser')
        try:
            nxt = soup.select('.next > a')[0]['href']
        except IndexError:
            return None
        url_next = self.base_url + nxt[1:]
        return url_next

    @helpers.with_logging
    def get_all_quotes(self):
        while True:  # опасна блад!
            self.get_quotes_from_single_page(self.current_url)
            next_url = self.get_next_page_url(self.current_url)
            #print(f'next url: {next_url}')
            if not next_url:
                break
            self.current_url = next_url


class Quote:

    def __init__(self, text, author, link_to_author):
        self.text = text
        self.author = author
        self.link_to_author = link_to_author
        self.hints = []

    def __repr__(self):
        return f'a quote by {self.author}: \n {self.text}'

    def create_hints(self):

        res = requests.get(self.link_to_author).text
        soup = BeautifulSoup(res, 'html.parser')
        # подсказки: дата и место рождения; инициалы; мб еще какие-то даты?
        birth_date = soup.select('.author-born-date')[0].string
        birth_place = soup.select('.author-born-location')[0].string
        initials = '.'.join(
            [letter for letter in self.author if letter.isupper()])
        self.hints.append(f'The author of this quote was born on {birth_date}')
        self.hints.append(
            f'The author of this quote was born in {birth_place}')
        self.hints.append(f'The author\'s initials are {initials}')

    def get_hint(self):
        try:
            hint = self.hints.pop()
            return hint
        except IndexError:
            return None


if __name__ == '__main__':
    qf = QuoteFactory()
    qf.get_all_quotes()
    print(len(qf.quotes))
