import random
import string

# Word giessing game class
class Game:
    _words: list[str];
    _secret: string;
    _blanks: string;
    _lives: int;
    _used: set;

    # Init class with an external words list
    def __init__(self, words):
        self._words = words;
        self._secret = self.get_random_word()
        self._blanks = self.make_blanks(self._secret)
        self._lives = 6;
        self._used = set()

    # Get a random word from a supplied list
    def get_random_word(self):
        return random.choice(self._words)

    # Hide all letters in a word
    def make_blanks(self, word):
        return ["_" for _ in word]

    # Ask for a letter input
    def prompt_for_letter(self, used_letters):
        while True:
            # Error handling
            guess = input("Guess a letter: ").strip().lower()
            if len(guess) != 1 or guess not in string.ascii_lowercase:
                print(" → Please enter a single A-Z letter.")
                continue
            if guess in used_letters:
                print(" → You already tried that letter.")
                continue
            return guess

    # This method does 2 things:
    # 1. It checks whether a letter is available in the word of question
    # 2. It recovers a letter in a place of a placeholder 
    def reveal_letters(self, word, blanks, letter):
        found_any = False
        for i, ch in enumerate(word):
            if ch == letter and blanks[i] == "_":
                blanks[i] = letter
                found_any = True
        return found_any

    # Game end condition. It checks whether all gaps are filled
    def all_blanks_filled(self, blanks):
        return "_" not in blanks

    # The main game loop
    def play(self):
        print("\nWelcome to Word Guessing!")
        print(f"The word has {len(self._secret)} letters.")
        print(" ".join(self._blanks))

        while True:
            # Ask the user to guess a letter
            guess = self.prompt_for_letter(self._used)
            self._used.add(guess)

            # Is the guessed letter in the word?
            if self.reveal_letters(self._secret, self._blanks, guess):
                print("\n Well done, Nice job! You found a letter.")
                print(" ".join(self._blanks))
                # Are all blanks filled?
                if self.all_blanks_filled(self._blanks):
                    print("\n Congratulation! You guessed the word!")
                    print(f"Word: {self._secret}")
                    print("GAME OVER")
                    break
            else:
                # Lose a life
                self._lives -= 1
                print(f"\nNope. You lose a life. Lives left: {self._lives}")
                print(" ".join(self._blanks))

                # Have they run out of lives?
                if self._lives <= 0:
                    print("\n Out of lives & Sad story!")
                    print(f"The word was: {self._secret}")
                    print("GAME OVER")
                    break

            # (loop continues to ask for another letter)

if __name__ == "__main__":
    # A list of words to guess
    words = [
        "python", "variable", "function", "iterator", "notebook",
        "pipeline", "dataset", "computer", "research", "analytics"
    ]
    Game(words).play();
