import customtkinter as ctk
from turtle import Turtle, Screen
import random

# Global variables for tracking the game state
bet_amount = 0
user_bet = 0
num_players = 0
total_profit = 0

# Global variable for Turtle screen
turtle_screen = None

# Reset function to start a new game
def reset_game():
    global turtle_screen
    if turtle_screen:
        turtle_screen.bye()  # Close the previous Turtle screen
    main_game_interface()

# Start the game logic with turtle race
def start_race():
    global num_players, bet_amount, root, user_bet
    try:
        difficulty = difficulty_var.get()
        bet_amount = int(entry_money.get())
        
        if difficulty == "easy":
            num_players = 3
        elif difficulty == "medium":
            num_players = 5
        elif difficulty == "hard":
            num_players = 7
        
        root.destroy()  # Close the Tkinter window after getting the input
        select_turtle()

    except ValueError as e:
        error_label.configure(text=str(e))

# Function to choose the turtle for betting
def select_turtle():
    global user_bet, bet_window
    bet_window = ctk.CTk()
    bet_window.title("Choose Your Turtle")
    bet_window.geometry("400x400")

    label = ctk.CTkLabel(bet_window, text="Choose your turtle to bet on:", font=("Arial", 16))
    label.pack(pady=10)

    turtle_choices = [str(i + 1) for i in range(num_players)]
    turtle_var = ctk.StringVar(value=turtle_choices[0])

    option_menu = ctk.CTkOptionMenu(bet_window, values=turtle_choices, variable=turtle_var)
    option_menu.pack(pady=20)

    button = ctk.CTkButton(bet_window, text="Start Race", command=lambda: start_race_with_bet(int(turtle_var.get())))
    button.pack(pady=20)

    bet_window.mainloop()

# Function to start the race with the chosen bet
def start_race_with_bet(bet):
    global user_bet, bet_window
    user_bet = bet
    bet_window.destroy()  # Close the bet window after user makes a selection
    turtle_race()

# Function to handle the turtle race
def turtle_race():
    global num_players, total_profit, bet_amount, user_bet, turtle_screen
    turtle_screen = Screen()  # Create a new Turtle screen
    turtle_screen.setup(width=1.0, height=1.0)  # Fullscreen mode
    turtle_screen.bgcolor("black")

    # Set up the finish line
    finish_line = turtle_screen.window_width() // 2 - 100
    for i in range(3):
        line = Turtle()
        line.shape("square")
        line.shapesize(stretch_wid=0.2, stretch_len=30)  # Making line thick
        line.color("white" if i != 1 else "black")
        line.penup()
        line.goto(finish_line + (i - 1) * 10, turtle_screen.window_height() // 2)
        line.pendown()
        line.right(90)
        line.forward(turtle_screen.window_height())
        line.hideturtle()

    # Create turtles and evenly space them
    turtles = []
    colors = ["coral2", "DarkGreen", "aquamarine2", "DarkOliveGreen2", "DarkGoldenrod1", "bisque2", "purple", "cyan"]
    for i in range(num_players):
        new_turtle = Turtle(shape="turtle")
        new_turtle.shapesize(stretch_wid=2, stretch_len=2)  # Increase turtle size
        new_turtle.speed(0)
        new_turtle.color(colors[i % len(colors)])
        new_turtle.penup()
        new_turtle.goto(-turtle_screen.window_width() // 2 + 50, (i - num_players // 2) * 100)  # Evenly spaced turtles
        turtles.append(new_turtle)
        
        # Label each turtle with its number
        label = Turtle()
        label.hideturtle()
        label.penup()
        label.goto(new_turtle.xcor(), new_turtle.ycor() + 30)
        label.write(f"Turtle {i+1}", align="center", font=("Arial", 12, "bold"))

    # Race logic
    winner = None
    while winner is None:
        for i in turtles:
            i.forward(random.randint(1, 10))
            if i.xcor() > finish_line:
                winner = i
                break

    # Announce winner
    turtle_screen.bye()  # Close the Turtle screen
    announce_winner(turtles.index(winner) + 1)

# Function to announce the winner and show the result
def announce_winner(winner_num):
    global total_profit, bet_amount, user_bet
    
    winner_screen = ctk.CTk()
    winner_screen.title("Winner Announcement")
    result = f"Turtle {winner_num} Wins!\n"

    if winner_num == user_bet:
        result += f"Congratulations! You won the bet and earned ${bet_amount * 2}!"
        total_profit += bet_amount * 2
    else:
        result += f"Sorry, you lost the bet of ${bet_amount}."
        total_profit -= bet_amount

    # Display the result
    label = ctk.CTkLabel(winner_screen, text=result, font=("Arial", 24))
    label.pack(pady=20)

    # Display profit/loss summary
    summary = f"Net Profit/Loss: ${total_profit}"
    summary_label = ctk.CTkLabel(winner_screen, text=summary, font=("Arial", 18))
    summary_label.pack(pady=20)

    # Re-bet and Exit buttons
    rebet_button = ctk.CTkButton(winner_screen, text="Re-bet", command=lambda: [winner_screen.destroy(), reset_game()], font=("Arial", 14))
    rebet_button.pack(pady=10)

    exit_button = ctk.CTkButton(winner_screen, text="Exit", command=winner_screen.destroy, font=("Arial", 14))
    exit_button.pack(pady=10)

    winner_screen.mainloop()

# Main Tkinter window for user input using CustomTkinter
def main_game_interface():
    global error_label, entry_money, difficulty_var, root
    root = ctk.CTk()  # Now root is a global variable
    root.title("Turtle Betting Game")
    root.geometry("400x400")

    # Game description label
    description = "Welcome to the betting game! Choose difficulty and bet amount to start."
    description_label = ctk.CTkLabel(root, text=description, font=("Arial", 14), wraplength=380)
    description_label.pack(pady=10)

    # Difficulty selection
    label_diff = ctk.CTkLabel(root, text="Choose difficulty:", font=("Arial", 14))
    label_diff.pack(pady=10)

    difficulty_var = ctk.StringVar(value="easy")
    difficulty_menu = ctk.CTkOptionMenu(root, values=["easy", "medium", "hard"], variable=difficulty_var)
    difficulty_menu.pack(pady=10)

    # Bet amount input
    label_money = ctk.CTkLabel(root, text="Enter your bet amount ($):", font=("Arial", 14))
    label_money.pack(pady=10)

    entry_money = ctk.CTkEntry(root, font=("Arial", 14))
    entry_money.pack(pady=10)

    # Error label
    error_label = ctk.CTkLabel(root, text="", font=("Arial", 12), text_color="red")
    error_label.pack(pady=10)

    # Continue button
    button = ctk.CTkButton(root, text="Continue", command=start_race, font=("Arial", 14))
    button.pack(pady=10)

    root.mainloop()

# Start the game interface
main_game_interface()
