import random
from capitals import states


class User:
    def __init__(self):
        self.correct_answer = 0
        self.incorrect_answer = 0

    def all_correct(self, total_states):
        return self.correct_answer == total_states

    def all_incorrect(self, total_states):
        return self.incorrect_answer == total_states

    def total_score(self):
        return self.correct_answer - self.incorrect_answer

    def display_score(self):
        print(f"Your total score is {self.total_score()}")

    def hint(self, state):
        capital = state.get('capital')
        if capital:
            print(f"Hint: The first three letters of the capital are {capital[:3]}")
        else:
            print("Invalid state. Capital not found.")

    def out_of_guesses(self, state):
        capital = state.get('capital')
        if capital:
            play_again = input(f"Incorrect. You've run out of guesses. The correct answer is {capital}. Would you like to play again? (yes/no)")
            if play_again.lower() == 'yes':
                self.correct_answer = 0
                self.incorrect_answer = 0
                return True
            elif play_again.lower() == 'no':
                print("Thanks for playing!")
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            print("Invalid state. Capital not found.")

    def reset_answers(self):
        self.correct_answer = 0
        self.incorrect_answer = 0


class Game:
    def __init__(self, states):
        self.states = states
        random.shuffle(self.states)
        self.user = User()

    def reset_states(self):
        self.states = [state for state in self.states if state.get("incorrect") is None]
        random.shuffle(self.states)

    def play_again(self):
        incorrect_states = [state for state in self.states if state.get("incorrect") is not None]
        if incorrect_states:
            descending_sorted_states = sorted(incorrect_states, key=lambda x: x.get("incorrect", 0), reverse=True)
            random.shuffle(descending_sorted_states)
            self.states = descending_sorted_states

    def start(self):
        print("Welcome to the game of State Capitals.")
        print("There are 50 states in the US.")
        print("Your job is to identify the capital of each state.")

        while True:
            for state in self.states:
                print(f"What is the capital of {state['name']}?")
                user_input = input().strip()

                if not user_input or not state.get("capital"):
                    print("Invalid input. Please enter a valid capital.")
                elif user_input == state["capital"]:
                    self.user.correct_answer += 1
                    print(f"Correct! The capital of {state['name']} is {state['capital']}")
                    self.user.display_score()
                elif self.user.all_correct(len(self.states)):
                    print("All 50 answers are correct! Congratulations!")
                    play_again = input("Would you like to play again? (yes/no)\n").lower()
                    if play_again == "yes":
                        self.user.reset_answers()
                        self.reset_states()
                    elif play_again == 'no':
                        print("Thanks for playing!")
                        self.user.reset_answers()
                        self.reset_states()
                        exit()
                else:
                    self.user.incorrect_answer += 1
                    self.user.hint(state)
                    user_input = input()
                    self.user.display_score()

                if self.user.total_score() == 0:
                    if not self.user.out_of_guesses(state):
                        break


game = Game(states)
game.start()

