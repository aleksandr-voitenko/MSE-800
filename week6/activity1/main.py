import random

def deal_card():
    # Face cards are worth 10. An ace starts at 11 and can count as 1
    #                                                 J   Q   K   Ace
    return random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])

def calculate_score(cards):
    score = sum(cards)
    aces = cards.count(11)

    # Handling Ace case
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1

    return score

def is_blackjack(cards):
    return len(cards) == 2 and calculate_score(cards) == 21

def get_result(player_cards, computer_cards):
    player_score = calculate_score(player_cards)
    computer_score = calculate_score(computer_cards)

    if is_blackjack(player_cards) and is_blackjack(computer_cards):
        return "Draw. Both have Blackjack."
    if is_blackjack(computer_cards):
        return "You lose. Computer has Blackjack."
    if is_blackjack(player_cards):
        return "You win with Blackjack!"
    if player_score > 21:
        return "You went over 21. You lose."
    if computer_score > 21:
        return "Computer went over 21. You win!"
    if player_score > computer_score:
        return "You win!"
    if player_score < computer_score:
        return "You lose."
    return "Draw."

def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("Please type 'y' or 'n'.")

def play_game():
    player_cards = [deal_card(), deal_card()]
    computer_cards = [deal_card(), deal_card()]

    while True:
        print(f"\nYour cards: {player_cards}, current score: {calculate_score(player_cards)}")
        print(f"Computer's first card: {computer_cards[0]}")

        if calculate_score(player_cards) >= 21 or is_blackjack(computer_cards):
            break
        if not ask_yes_no("Type 'y' to get another card, type 'n' to pass: "):
            break
        player_cards.append(deal_card())

    if calculate_score(player_cards) <= 21 and not is_blackjack(player_cards):
        while calculate_score(computer_cards) < 17:
            computer_cards.append(deal_card())

    print(f"\nYour final hand: {player_cards}, final score: {calculate_score(player_cards)}")
    print(f"Computer's final hand: {computer_cards}, final score: {calculate_score(computer_cards)}")
    print(get_result(player_cards, computer_cards))
    print()

def main():
    print("Welcome to Blackjack!")
    try:
        while ask_yes_no("Do you want to play a game of Blackjack? Type 'y' or 'n': "):
            play_game()
    except (EOFError, KeyboardInterrupt):
        print()
    print("Goodbye!")

if __name__ == "__main__":
    main()
