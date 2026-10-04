import os
import tkinter as tk

# Game choices
CHOICES = ["Rock", "Paper", "Scissors"]

# Score counters
player_one_score = 0
player_two_score = 0
draw_count = 0
player_one_choice = ""
player_two_choice = ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create the default root window first so StringVar objects can be created safely.
root = tk.Tk()
root.withdraw()
window_icon_path = os.path.join(BASE_DIR, "window_icon.png")
window_icon = tk.PhotoImage(file=window_icon_path)
root.iconphoto(True, window_icon)

# Dark modern color palette
BG_COLOR = "#0f172a"
PANEL_COLOR = "#111827"
CARD_COLOR = "#1f2937"
TEXT_COLOR = "#e5e7eb"
MUTED_TEXT = "#cbd5e1"
BLUE_ACCENT = "#60a5fa"
RED_ACCENT = "#f87171"
GREEN_ACCENT = "#34d399"
YELLOW_ACCENT = "#fbbf24"

# String variables used to update labels
player_one_choice_var = tk.StringVar(root, value="Waiting...")
player_two_choice_var = tk.StringVar(root, value="Waiting...")
result_var = tk.StringVar(root, value="Player 1, choose your move!")
player_one_score_var = tk.StringVar(root, value="0")
player_two_score_var = tk.StringVar(root, value="0")
draw_score_var = tk.StringVar(root, value="0")
winner_banner_var = tk.StringVar(root, value="")
winner_label = None


def determine_winner(choice_one, choice_two):
    """Return the winner of the round."""
    if choice_one == choice_two:
        return "draw"

    winning_pairs = {
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper",
    }

    if winning_pairs[choice_one] == choice_two:
        return "player_one"

    return "player_two"


def update_scoreboard():
    """Refresh score labels on the screen."""
    player_one_score_var.set(str(player_one_score))
    player_two_score_var.set(str(player_two_score))
    draw_score_var.set(str(draw_count))


def animate_winner_glow(label_widget, color):
    """Give the winner banner a simple glow-like animation effect."""
    label_widget.config(bg=color)
    label_widget.after(150, lambda: label_widget.config(bg="#111827"))
    label_widget.after(300, lambda: label_widget.config(bg=color))
    label_widget.after(450, lambda: label_widget.config(bg="#111827"))


def reset_game():
    """Reset the game completely."""
    global player_one_score, player_two_score, draw_count, player_one_choice, player_two_choice

    player_one_score = 0
    player_two_score = 0
    draw_count = 0
    player_one_choice = ""
    player_two_choice = ""

    player_one_choice_var.set("Waiting...")
    player_two_choice_var.set("Waiting...")
    result_var.set("Player 1, choose your move!")
    winner_banner_var.set("")
    update_scoreboard()


def quit_game():
    """Close the application window."""
    root.destroy()


def choose_move(player_number, choice):
    """Handle when a player clicks a move button."""
    global player_one_choice, player_two_choice, player_one_score, player_two_score, draw_count

    if player_number == 1:
        player_one_choice = choice
        player_one_choice_var.set(choice)
        result_var.set("Player 2, choose your move!")
        return

    if player_one_choice == "":
        result_var.set("Player 1 must choose first!")
        return

    player_two_choice = choice
    player_two_choice_var.set(choice)

    winner = determine_winner(player_one_choice, player_two_choice)

    if winner == "player_one":
        player_one_score += 1
        result_var.set("Player 1 wins this round!")
        winner_banner_var.set("🎉 Player 1 Wins! 🎉")
        glow_color = "#1d4ed8"
    elif winner == "player_two":
        player_two_score += 1
        result_var.set("Player 2 wins this round!")
        winner_banner_var.set("🎉 Player 2 Wins! 🎉")
        glow_color = "#dc2626"
    else:
        draw_count += 1
        result_var.set("It's a draw!")
        winner_banner_var.set("🤝 It's a Draw! 🤝")
        glow_color = "#f59e0b"

    update_scoreboard()
    player_one_choice = ""
    player_two_choice = ""
    player_one_choice_var.set("Waiting...")
    player_two_choice_var.set("Waiting...")

    if winner_label is not None:
        animate_winner_glow(winner_label, glow_color)


def load_logo_widget(parent):
    """Return the real application logo when available, otherwise a fallback badge."""
    logo_paths = [
        os.path.join(BASE_DIR, "logo.png"),
        os.path.join(BASE_DIR, "image logo.png"),
        os.path.join(BASE_DIR, "assets", "logo.png"),
        os.path.join(BASE_DIR, "images", "logo.png"),
        os.path.join(BASE_DIR, "..", "image logo.png"),
        os.path.join(BASE_DIR, "..", "logo.png"),
    ]

    for logo_path in logo_paths:
        candidate = os.path.abspath(logo_path)
        if os.path.exists(candidate):
            try:
                logo_image = tk.PhotoImage(file=candidate)
                label = tk.Label(parent, image=logo_image, bg=BG_COLOR, borderwidth=0)
                label.image = logo_image
                return label
            except tk.TclError:
                continue

    canvas = tk.Canvas(parent, width=90, height=90, bg=BG_COLOR, highlightthickness=0)
    canvas.create_oval(12, 12, 78, 78, fill="#1d4ed8", outline="#93c5fd", width=3)
    canvas.create_oval(20, 20, 70, 70, fill="#0f172a", outline="#93c5fd", width=2)
    canvas.create_text(45, 45, text="RPS", fill="#f8fafc", font=("Arial", 18, "bold"))
    return canvas


def create_window():
    """Build the two-player interface."""
    root.title("Rock Paper Scissors - Two Players")
    root.geometry("650x700")
    root.minsize(560, 620)
    root.configure(bg=BG_COLOR)

    top_bar = tk.Frame(root, bg=BG_COLOR)
    top_bar.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=(18, 8))
    top_bar.columnconfigure(0, weight=1)

    logo_widget = load_logo_widget(top_bar)
    logo_widget.grid(row=0, column=0, sticky="nsew", pady=6)

    instruction_label = tk.Label(
        root,
        text="Player 1 chooses first, then Player 2 chooses. The winner is announced after both selections.",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=MUTED_TEXT,
        wraplength=560,
        pady=8,
    )
    instruction_label.grid(row=1, column=0, columnspan=3, sticky="nsew")

    p1_title = tk.Label(root, text="Player 1", font=("Arial", 14, "bold"), bg=BG_COLOR, fg=BLUE_ACCENT)
    p1_title.grid(row=2, column=0, pady=(10, 4))

    p2_title = tk.Label(root, text="Player 2", font=("Arial", 14, "bold"), bg=BG_COLOR, fg=RED_ACCENT)
    p2_title.grid(row=2, column=2, pady=(10, 4))

    button_style = {
        "font": ("Arial", 12, "bold"),
        "width": 12,
        "height": 2,
        "bg": "#1e293b",
        "fg": "#f8fafc",
        "relief": "flat",
        "cursor": "hand2",
        "activebackground": "#334155",
    }

    for index, choice in enumerate(CHOICES):
        tk.Button(root, text=choice, command=lambda ch=choice: choose_move(1, ch), **button_style).grid(
            row=3 + index, column=0, padx=18, pady=8, sticky="ew"
        )
        tk.Button(root, text=choice, command=lambda ch=choice: choose_move(2, ch), **button_style).grid(
            row=3 + index, column=2, padx=18, pady=8, sticky="ew"
        )

    p1_choice_label = tk.Label(root, text="Choice:", font=("Arial", 12, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
    p1_choice_label.grid(row=6, column=0, pady=8)

    p2_choice_label = tk.Label(root, text="Choice:", font=("Arial", 12, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
    p2_choice_label.grid(row=6, column=2, pady=8)

    p1_choice_display = tk.Label(root, textvariable=player_one_choice_var, font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR)
    p1_choice_display.grid(row=7, column=0, pady=(0, 10))

    p2_choice_display = tk.Label(root, textvariable=player_two_choice_var, font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR)
    p2_choice_display.grid(row=7, column=2, pady=(0, 10))

    global winner_label

    winner_label = tk.Label(
        root,
        textvariable=winner_banner_var,
        font=("Arial", 18, "bold"),
        bg="#111827",
        fg="#f8fafc",
        padx=18,
        pady=12,
        relief="solid",
        borderwidth=2,
        highlightbackground="#fbbf24",
    )
    winner_label.grid(row=8, column=0, columnspan=3, padx=20, pady=(0, 8), sticky="ew")

    result_label = tk.Label(
        root,
        textvariable=result_var,
        font=("Arial", 16, "bold"),
        bg="#14532d",
        fg="#ecfdf5",
        padx=20,
        pady=12,
        relief="solid",
        borderwidth=1,
    )
    result_label.grid(row=9, column=0, columnspan=3, padx=20, pady=8, sticky="ew")

    scoreboard = tk.Frame(root, bg="#111827", bd=2, relief="ridge", padx=18, pady=12)
    scoreboard.grid(row=10, column=0, columnspan=3, padx=18, pady=8, sticky="ew")
    scoreboard.columnconfigure(0, weight=1)
    scoreboard.columnconfigure(1, weight=1)
    scoreboard.columnconfigure(2, weight=1)

    score_title = tk.Label(scoreboard, text="Scoreboard", font=("Arial", 16, "bold"), bg="#111827", fg="#f8fafc")
    score_title.grid(row=0, column=0, columnspan=3, pady=(0, 10))

    player_one_label = tk.Label(scoreboard, text="Player 1", font=("Arial", 11, "bold"), bg="#111827", fg=BLUE_ACCENT)
    player_one_label.grid(row=1, column=0, padx=8, pady=4)

    player_two_label = tk.Label(scoreboard, text="Player 2", font=("Arial", 11, "bold"), bg="#111827", fg=RED_ACCENT)
    player_two_label.grid(row=1, column=1, padx=8, pady=4)

    draw_label = tk.Label(scoreboard, text="Draws", font=("Arial", 11, "bold"), bg="#111827", fg=YELLOW_ACCENT)
    draw_label.grid(row=1, column=2, padx=8, pady=4)

    player_one_score_label = tk.Label(scoreboard, textvariable=player_one_score_var, font=("Arial", 15, "bold"), fg=BLUE_ACCENT, bg="#111827")
    player_one_score_label.grid(row=2, column=0, padx=8, pady=4)

    player_two_score_label = tk.Label(scoreboard, textvariable=player_two_score_var, font=("Arial", 15, "bold"), fg=RED_ACCENT, bg="#111827")
    player_two_score_label.grid(row=2, column=1, padx=8, pady=4)

    draw_score_label = tk.Label(scoreboard, textvariable=draw_score_var, font=("Arial", 15, "bold"), fg=YELLOW_ACCENT, bg="#111827")
    draw_score_label.grid(row=2, column=2, padx=8, pady=4)

    reset_button = tk.Button(
        root,
        text="Reset Game",
        command=reset_game,
        bg="#3b82f6",
        fg="#eff6ff",
        font=("Arial", 12, "bold"),
        width=16,
        height=2,
    )
    reset_button.grid(row=11, column=0, padx=18, pady=16, sticky="ew")

    quit_button = tk.Button(
        root,
        text="Quit",
        command=quit_game,
        bg="#ef4444",
        fg="#fff1f2",
        font=("Arial", 12, "bold"),
        width=16,
        height=2,
    )
    quit_button.grid(row=11, column=2, padx=18, pady=16, sticky="ew")

    for column in range(3):
        root.columnconfigure(column, weight=1)

    update_scoreboard()


def main():
    """Create the application window and run it."""
    create_window()
    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    main()
