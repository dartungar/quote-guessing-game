import random
from quote import QuoteFactory, Quote


class Game:

    def __init__(self, num_of_guesses=4):
        self.quotefactory = QuoteFactory()
        self.quotefactory.get_all_quotes()
        self.num_of_guesses = num_of_guesses
        self.player_has_won = False

    def start_game(self):
        while not self.player_has_won:
            r = self.new_round()
            if r:
                self.player_has_won = True
                print('Congratulations, you have won!')
                return
            start_new_round = input(
                'Alas, you have not beaten me! Do you want to play again? (yes/no): ')
            if start_new_round.lower() == 'no':
                return
            elif start_new_round.lower() == 'yes':
                continue

    def new_round(self):
        self.quote = random.choice(self.quotefactory.quotes)
        self.quote.create_hints()
        self.guesses_left = self.num_of_guesses
        print(
            f'Who is the author of this quote: {self.quote.text}? \n You have four guesses.')
        while self.guesses_left:
            self.guesses_left -= 1
            g = self.guess()
            if g:
                return True
        return False

    def guess(self):
        answer = input('Enter the author: ')
        if answer == self.quote.author:
            return True
        hint = self.quote.get_hint()
        if hint:
            print(f'Here\'s a hint. {hint}')
        return False


if __name__ == '__main__':
    game = Game()
    game.start_game()
