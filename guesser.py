import itertools

WORD_LENGTH=5
NOT_PRESENT=1
PRESENT=2
PLACED=3

class GuessLetter:
    def __init__(self, letter, status):
        self._letter = letter
        self._status = status

    @property
    def value(self):
        return self._letter.lower()

    @property
    def status(self):
        return self._status

    
class Guesser:
    def __init__(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self._slots = [list(alphabet) for slot in range(WORD_LENGTH)]
        self._unplaced = list()
        self._guesses = list()

    def guess(self, guess):
        self._guesses.append([letter.value for letter in guess])
        for slot_i, letter in enumerate(guess):
            if letter.status == NOT_PRESENT:
                for slot in self._slots:
                    if letter.value in slot:
                        slot.remove(letter.value)
            if letter.status == PLACED:
                if letter.value in self._unplaced:
                    self._unplaced.remove(letter.value)
                self._slots[slot_i] = [letter.value]
            if letter.status == PRESENT:
                if letter.value not in self._unplaced:
                    self._unplaced.append(letter.value)
                self._slots[slot_i].remove(letter.value)
               
    @property
    def guesses(self):
        return self._guesses
                
    @property
    def remaining(self):
        for word in itertools.product(*self._slots):
            valid = True
            for required in self._unplaced:
                if required not in word:
                    valid = False
                    break
            if valid:
                yield ''.join(word)

                
def print_remaining(guesser):
    h = 12
    for i, word in enumerate(guesser.remaining):
        if i > 0 and not i % h:
            print()
        print(word, end=' ')
    if i % h:
        print()

def test():
    r = GuessLetter('r', PRESENT)
    a = GuessLetter('a', PRESENT)
    t = GuessLetter('t', PLACED)
    i = GuessLetter('i', NOT_PRESENT)
    o = GuessLetter('o', PRESENT)

    G = Guesser()
    G.guess((r,a,t,i,o))
    print_remaining(G)

def status_str(status):
    if status == PRESENT:
        out = "PRESENT but in the wrong location"
    elif status == NOT_PRESENT:
        out = "NOT PRESENT in the word"
    elif status == PLACED:
        out = "in the CORRECT location"
    else:
        raise ValueError("Invalid status.")
    return out
    
class UI:
    def __init__(self):
        self._guesser = Guesser()

    def _guess_letter(self, letter):
        help = "Tell me if the letter was (A) not present, (B) present"\
            " but in the wrong location, or (C) in the correct"\
            " location."
        err = "Input not recognized. Please enter A, B, C or ?."
        while True:
            status = input("%s > " % letter.upper()).upper()
            if status not in 'ABC?':
                print(err)
            elif status == '?':
                print(help)
            elif status == 'A':
                return GuessLetter(letter, NOT_PRESENT)
            elif status == 'B':
                return GuessLetter(letter, PRESENT)
            elif status == 'C':
                return GuessLetter(letter, PLACED)

    def _register_guess(self, guess):
        help = "For each letter, tell me if it was (A) not present, (B)"\
            " present but in the wrong location, or (C) in the correct"\
            " location."
        print(help)
        word = list()
        while True:
            for letter in guess:
                word.append(self._guess_letter(letter))            
            print("Your guess was:")
            for letter in word:
                print(" * %s: %s" % (letter.value, status_str(letter.status)))
            while True:
                p = "Is that correct? (y/n) "
                x = input(p).lower()
                if x == 'y':
                    return self._guesser.guess(word)
                elif x == 'n':
                    print("Ok, let's try again.")
                    word = list()
                    break
                else:
                    print("Please enter 'y' or 'n'.")    

    def _get_guess(self):
        while True:
            guess = input("Please enter your guess: ").strip()
            if len(guess) != WORD_LENGTH:
                print("Sorry, guess needs to be %i letters." % WORD_LENGTH)
            while True:
                p = "Your guess is '%s', correct? (y/n) " % guess.upper()
                x = input(p).lower()
                if x == 'y':
                    return guess
                elif x == 'n':
                    print("Ok, let's try again.")
                    break
                else:
                    print("Please enter 'y' or 'n'.")
        
    def run(self):
        while True:
            guess = self._get_guess()
            self._register_guess(guess)
            while True:
                p = "Enter another guess? (y/n) "
                x = input(p).lower()
                if x == 'y':
                    break
                elif x == 'n':
                    print("Ok, here are your remaining options:")
                    print_remaining(self._guesser)
                    return None
                else:
                    print("Please enter 'y' or 'n'.")
        

    
if __name__ == '__main__':
    g = UI()
    g.run()
