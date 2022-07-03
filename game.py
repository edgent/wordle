from guesser import Guesser
from wordle_data import import_wordle_data

class Game:
    def __init__(self, answer) -> None:
        self.answer = answer.lower()
        self.current_round = 1
        self.guess_count = 0
        self.latest_guess = ''
        self.game_won = False
        self.game_lost = False
        self.letter_lists = {
            'green':{x:'' for x in range(5)}, # empty dictionary with keys 1 through 6 to represent 6 turns in wordle
            'yellow':set(), # ** to do ** this should really be a list, since you can have more than one yellow of the same letter
            'yellow_position_history':{},
            'grey':set() # going to be a set
        }
        self.guesses = {x:'' for x in range(6)} # empty dictionary keys 1 to 5 to populate with guesses - effectively the game board
        self.wordle_data = import_wordle_data()
        if answer not in self.wordle_data.index:
            print("Warning - answer not in the database so it won't be possible to guess")
    

    def evaluate_guess(self, word):
        word = word.lower()
        # - check for exact matches --> update green list, remove any new greens from yellow list
        # - excluding exact matches and yellow letters already guessed, check overlap between guess submitted and answer --> update yellow list
        # - subtract new green and yellow letters from the guess --> update grey letters
        
        # alt way to evalute:
        # 1. find all greens, update the letter lists and remove them from the remaining 'answer' letters to guess
        # 2. find all greys in the remaining answer letters 
        # 3. find all yellows one by one and update answer letter list as you go 
        guess_dic = {i:x for i, x in enumerate(word)} # making a copy to remove items from as we go
        answer_working = list(self.answer)
        # greens 
        for i, letter in enumerate(word):
            # letter = guess_dic[i]
            if self.answer == '': # inefficient way to handle a game with no answer - ideally don't want to waste time looping here
                continue 
            elif letter == self.answer[i]:
                self.letter_lists['green'][i] = letter
                if letter in self.letter_lists['yellow']:
                    self.letter_lists['yellow'].remove(letter)
                del guess_dic[i]
                answer_working.remove(letter) # removing greens from the working lists to let us check yellows and greys
            else:
                continue 
        
        # yellows/greys: if guessed letters are in the remaining 
        for i in guess_dic:
            letter = guess_dic[i]
            if letter in answer_working:
                self.letter_lists['yellow'].add(letter)
                try:
                    self.letter_lists['yellow_position_history'][i].append(letter)
                except:
                    self.letter_lists['yellow_position_history'][i] = [letter]
                answer_working.remove(letter) # remove the letter from the potential answer list in case the same letter is guessed multiple times
            else:
                if letter not in self.letter_lists['yellow']: # if we have the same letter twice (e.g. "o" in "solon" when trying to get "scour"), we don't want it to reach the grey list
                    self.letter_lists['grey'].add(letter)

        # checking if the game is won
        if list(self.letter_lists['green'].values()) == list(self.answer):
            self.game_won = True
            print(f'Game won in {self.guess_count} turns!')
        
        # checking if the game is lost
        elif (self.game_won == False) and (self.guess_count >= 6):
            self.game_lost = True
            print('Game over, guess limit reached')

        else:
            print('Guess evaluated')
            print(self.letter_lists)
    
    def submit_guess(self,word):
        word = word.lower()
        self.guesses[self.guess_count]=word
        self.current_round += 1
        self.guess_count += 1
        self.latest_guess = word
        print(f'Guess "{word}" submitted')
        self.evaluate_guess(word)

    def autoplay_single_round(self):
        auto = Guesser() # imported globally at the top
        # play first round
        if True in [self.game_lost, self.game_won]:
            return 'Game has ended'

        # if self.guess_count == 0:
        #     self.submit_guess(auto.generate_guess)
        # else:
        #     self.submit_guess(auto.generate_guess(self.letter_lists))
        
        # v2: if fewer then 5, go by popularity. If 2nd go, go by last 2 letters. If 3rd go, go by middle 3. else go by letter frequency score.
        elif len(auto.generate_options(self.letter_lists)) <= 5:
            self.submit_guess(
                auto.generate_guess(self.letter_lists,method='word_frequency_rank')
            )
        elif self.guess_count == 1: # 2nd guess
            self.submit_guess(auto.generate_guess(self.letter_lists,method='last_2_letter_frequency'))
        elif self.guess_count == 2: # 2nd guess
            self.submit_guess(auto.generate_guess(self.letter_lists,method='middle_3_letter_frequency'))
        else:
            self.submit_guess(auto.generate_guess(self.letter_lists,method='letter_frequency'))

    def autoplay_whole_game(self):
        while self.game_lost == False and self.game_won == False:
            self.autoplay_single_round()
        else:
            print('Game has ended')

