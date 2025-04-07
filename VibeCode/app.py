from flask import Flask, render_template, request, redirect, url_for
import random
import time

app = Flask(__name__)

# Starting money
money = 1000

# Chaos events
def chaos_event():
    global money
    events = [
        ("IT saw you gambling! lol", lambda: lose_percent(50)),
        ("Classmate steals $20 from you!", lambda: lose_amount(20)),
        ("you didn't crash on your way to school! Gain $30!", lambda: gain_amount(30)),
        ("You got snitched on! You're expelled!", lambda: game_over())
    ]
    event = random.choice(events)
    result = f"[CHAOS] {event[0]}"
    event[1]()
    return result

def lose_percent(percent):
    global money
    loss = int(money * (percent / 100))
    money -= loss
    return f"You lost ${loss}. You now have ${money}."

def lose_amount(amount):
    global money
    money -= amount
    if money < 0:
        money = 0
    return f"You lost ${amount}. You now have ${money}."

def gain_amount(amount):
    global money
    money += amount
    return f"You gained ${amount}. You now have ${money}."

def game_over():
    global money
    money = 0
    return "GAME OVER. You were expelled from the gambling ring."

# Dice Duel Game
def play_dice_duel(bet):
    global money
    player_roll = random.randint(1, 6)
    opponent_roll = random.randint(1, 6)
    result = f"You rolled a {player_roll}. Opponent rolled a {opponent_roll}."

    if player_roll > opponent_roll:
        money += bet
        result += f" You win! New balance: ${money}"
    elif player_roll < opponent_roll:
        money -= bet
        result += f" You lose! New balance: ${money}"
    else:
        result += " It's a tie! No money lost."
    
    return result

# Slots Game
def play_slots(bet):
    global money
    symbols = ['🍒', '🍋', '🍇', '🔔', '7️⃣']
    payouts = {
        '🔔': 25,
        '7️⃣': 100
    }

    def spin():
        return [random.choice(symbols) for _ in range(3)]

    def calculate_payout(reels):
        if reels.count(reels[0]) == 3:
            if reels[0] in payouts:
                return payouts[reels[0]], f"🔥 Triple {reels[0]}! You won x{payouts[reels[0]]}!"
            elif reels[0] in ['🍒', '🍋', '🍇']:
                return 10, f"🍉 Triple fruits! You won x10!"
        elif all(r in ['🍒', '🍋', '🍇'] for r in reels):
            return 2, f"🍓 Mixed fruits! You won x2!"
        else:
            return 0, "😢 No win. Try again!"

    reels = spin()
    result = " | ".join(reels)
    multiplier, message = calculate_payout(reels)
    winnings = bet * multiplier
    money += winnings
    result += f" {message}"

    if winnings == 0:
        money -= bet  # Deduct the bet amount if the player loses

    
    if winnings > 0:
        result += f" You won ${winnings}!"
    
    return result

@app.route('/')
def home():
    return render_template('index.html', money=money)

@app.route('/play', methods=['POST'])
def play():
    global money
    action = request.form['action']
    bet = int(request.form['bet'])

    if action == 'dice_duel':
        result = play_dice_duel(bet)
    elif action == 'slots':
        result = play_slots(bet)
    elif action == 'chaos':
        result = chaos_event()

    return render_template('index.html', money=money, result=result)

@app.route('/quit')
def quit_game():
    return render_template('index.html', money=money, result="You chose to quit the game.")

if __name__ == '__main__':
    app.run(debug=True)