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
            link_to_author = self.base_url + link_to_author[1:]  # cut extra '/'
            new_quote = Quote(text=text, author=author, link_to_author=link_to_author)
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
        while True: # опасна блад!
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
    
    def create_hint(self, link_to_author):
        res = requests.get(link_to_author).text
        soup = BeautifulSoup(res, 'html.parser')
        # подсказки: дата и место рождения; инициалы; мб еще какие-то даты?
        # TODO

    def show_hint(self, hint):
        pass 


class Hint:
    
    def __init__(self, text, answer):
        self.text = text
        self.answer = answer

    
if __name__ == '__main__':
    qf = QuoteFactory()
    qf.get_all_quotes()
    print(len(qf.quotes))
