

class Game:

    def __init__(self, num_of_guesses=4):
        self.guesses_left = num_of_guesses

    def new_guess(self):
        self.guesses_left -= 1
        pass

