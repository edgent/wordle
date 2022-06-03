from guesser import Guesser

class Game:
    def __init__(self, answer) -> None:
        self.answer = answer.lower()
        self.current_round = 1
        self.guess_count = 0
        self.latest_guess = ''
        self.game_won = False
        self.game_lost = False
        self.letter_lists = {
            'green':{x:'' for x in range(5)}, # empty dictionary with keys 1 through 5
            'yellow':set(), # going to be a set
            'yellow_position_history':{},
            'grey':set() # going to be a set
        }
        self.guesses = {x:'' for x in range(5)} # empty dictionary keys 1 to 5 to populate with guesses - effectively the game board

    

    def evaluate_guess(self, word):
        word = word.lower()
        # - check for exact matches --> update green list, remove any new greens from yellow list
        # - excluding exact matches and yellow letters already guessed, check overlap between guess submitted and answer --> update yellow list
        # - subtract new green and yellow letters from the guess --> update grey letters
        for i in range(len(self.answer)):
            letter = word[i]
            # for an exact match, update green list and remove from yellows if it came from there
            if self.answer[i] == letter:
                print(f'{letter} is a match')
                self.letter_lists['green'][i] = letter
                # if a yellow turns into a green, remove it from the yellow list
                if letter in self.letter_lists['yellow']:
                    self.letter_lists['yellow'].remove(letter)
            # yellow matches
            elif letter in self.answer:
                print(f'{letter} is somewhere else in the answer')
                self.letter_lists['yellow'].add(letter)
                try:
                    self.letter_lists['yellow_position_history'][i].append(letter)
                except:
                    self.letter_lists['yellow_position_history'][i] = [letter]
            
            else:
                print(f'{letter} is not in the answer')
                self.letter_lists['grey'].add(letter)
        
        # checking if the game is won
        if list(self.letter_lists['green'].values()) == list(self.answer):
            self.game_won = True
            print(f'Game won in {self.guess_count} turns!')
        
        # checking if the game is lost
        elif (self.game_won == False) and (self.guess_count >= 5):
            self.game_lost = True
            print('Game over, guess limit reached')

        else:
            print('Guess evaluated')
    
    def submit_guess(self,word):
        word = word.lower()
        self.guesses[self.guess_count]=word
        self.current_round += 1
        self.guess_count += 1
        self.latest_guess = word
        print(f'Guess "{word}" submitted')
        self.evaluate_guess(word)

    def autoplay_single_round(
        self
        # ,Guesser # a Guesser class which we will instantiate and use to make guesses
    ):
        auto = Guesser()
        # play first round
        if True in [self.game_lost, self.game_won]:
            return 'Game has ended'

        if self.guess_count == 0:
                self.submit_guess(auto.generate_first_guess())
        else:
            self.submit_guess(auto.generate_guess(self.letter_lists))
        
    def autoplay_whole_game(
        self 
        #, Guesser
    ):
        while self.game_lost == False and self.game_won == False:
            self.autoplay_single_round()
        else:
            print('Game has ended')

