import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser 

def initialize_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

def check_win(board_state, player_symbol):
    for row_data in board_state:
        if all(s == player_symbol for s in row_data):
            return True
    for col_idx in range(3):
        if all(board_state[row_idx][col_idx] == player_symbol for row_idx in range(3)):
            return True
    if all(board_state[i][i] == player_symbol for i in range(3)):
        return True
    if all(board_state[i][2 - i] == player_symbol for i in range(3)):
        return True
    return False

def check_draw(board_state):
    for row_data in board_state:
        if ' ' in row_data:
            return False
    return True

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Saul's TicTacToe Game")
        master.resizable(False, False)

        self.board_buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board_state = initialize_board()
        self.game_over = False

        self.player_name_vars = [tk.StringVar(value="Player 1"), tk.StringVar(value="Player 2")]
        self.player_names_actual = ["", ""]
        self.starter_player_index = 0
        
        self.current_turn_player_name = ""
        self.current_turn_symbol = 'X'

        player_info_frame = tk.Frame(master)
        player_info_frame.grid(row=0, column=0, columnspan=3, pady=(10,5), padx=10)

        tk.Label(player_info_frame, text="Player 1:", font=('Arial', 12)).grid(row=0, column=0, padx=(0,5), pady=2, sticky="e")
        self.p1_name_entry = tk.Entry(player_info_frame, textvariable=self.player_name_vars[0], font=('Arial', 12), width=15)
        self.p1_name_entry.grid(row=0, column=1, padx=(0,10), pady=2)

        tk.Label(player_info_frame, text="Player 2:", font=('Arial', 12)).grid(row=1, column=0, padx=(0,5), pady=2, sticky="e")
        self.p2_name_entry = tk.Entry(player_info_frame, textvariable=self.player_name_vars[1], font=('Arial', 12), width=15)
        self.p2_name_entry.grid(row=1, column=1, padx=(0,10), pady=2)

        self.status_label = tk.Label(master, text="", font=('Arial', 14), pady=10)
        self.status_label.grid(row=1, column=0, columnspan=3)

        self.create_board_buttons()

        controls_frame = tk.Frame(master)
        controls_frame.grid(row=3, column=0, columnspan=3, pady=10)

        reset_button = tk.Button(controls_frame, text="Restart Game", command=self.reset_game, font=('Arial', 12))
        reset_button.pack(side=tk.LEFT, padx=10)

        swap_names_button = tk.Button(controls_frame, text="Swap Names", command=self.swap_player_name_entries, font=('Arial', 12))
        swap_names_button.pack(side=tk.LEFT, padx=10)

        self.configure_new_round()
        
        self.create_social_bar()

    def create_board_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=2, column=0, columnspan=3)
        for r in range(3):
            for c in range(3):
                button = tk.Button(button_frame, text=' ', font=('Arial', 40, 'bold'),
                                   width=3, height=1, relief=tk.GROOVE, borderwidth=2,
                                   command=lambda row=r, col=c: self.on_button_click(row, col))
                button.grid(row=r, column=c, padx=2, pady=2)
                self.board_buttons[r][c] = button

    def configure_new_round(self):
        self.player_names_actual[0] = self.player_name_vars[0].get() or "Player 1"
        self.player_names_actual[1] = self.player_name_vars[1].get() or "Player 2"

        if self.player_names_actual[0] == self.player_names_actual[1]:
            self.player_names_actual[0] = f"{self.player_names_actual[0]} (1)"
            self.player_names_actual[1] = f"{self.player_names_actual[1]} (2)"

        self.current_turn_player_name = self.player_names_actual[self.starter_player_index]
        self.current_turn_symbol = 'X'
        self.update_status_label(f"{self.current_turn_player_name}'s turn ({self.current_turn_symbol})")

    def on_button_click(self, row, col):
        if self.game_over or self.board_state[row][col] != ' ':
            return

        symbol_to_place = self.current_turn_symbol
        self.board_state[row][col] = symbol_to_place
        
        button_color = 'red' if symbol_to_place == 'X' else 'blue'
        self.board_buttons[row][col].config(text=symbol_to_place, state=tk.DISABLED,
                                            disabledforeground=button_color)

        if check_win(self.board_state, symbol_to_place):
            self.game_over = True
            winner_name = self.current_turn_player_name
            self.update_status_label(f"🥳{winner_name} wins!🎉")
            self.disable_all_board_buttons()
        elif check_draw(self.board_state):
            self.game_over = True
            self.update_status_label("It's a draw!")
            self.disable_all_board_buttons()
        else:
            if self.current_turn_symbol == 'X':
                self.current_turn_player_name = self.player_names_actual[1 - self.starter_player_index]
                self.current_turn_symbol = 'O'
            else:
                self.current_turn_player_name = self.player_names_actual[self.starter_player_index]
                self.current_turn_symbol = 'X'
            self.update_status_label(f"{self.current_turn_player_name}'s turn ({self.current_turn_symbol})")

    def update_status_label(self, message):
        self.status_label.config(text=message)

    def disable_all_board_buttons(self):
        for r in range(3):
            for c in range(3):
                if self.board_buttons[r][c]['state'] == tk.NORMAL:
                    self.board_buttons[r][c].config(state=tk.DISABLED)

    def reset_game(self):
        self.board_state = initialize_board()
        self.game_over = False
        self.starter_player_index = 1 - self.starter_player_index
        self.configure_new_round()

        for r in range(3):
            for c in range(3):
                self.board_buttons[r][c].config(text=' ', state=tk.NORMAL)

    def swap_player_name_entries(self):
        name0 = self.player_name_vars[0].get()
        name1 = self.player_name_vars[1].get()
        self.player_name_vars[0].set(name1)
        self.player_name_vars[1].set(name0)
        if self.game_over or not self.current_turn_player_name: 
            self.configure_new_round()

    def open_link(self, url):
        webbrowser.open_new_tab(url)

    def create_social_bar(self):
        social_frame = tk.Frame(self.master, pady=5, bg="gray") 
        social_frame.grid(row=4, column=0, columnspan=3, sticky="ew")

        try:
            img_path = "me1.jpg"
            original_image = Image.open(img_path)
            resized_image = original_image.resize((50, 50), Image.Resampling.LANCZOS)
            self.social_image_tk = ImageTk.PhotoImage(resized_image)
            
            image_label = tk.Label(social_frame, image=self.social_image_tk)
            image_label.pack(side=tk.LEFT, padx=(10, 5))
        except FileNotFoundError:
            print(f"Error: Image file '{img_path}' not found.")
            tk.Label(social_frame, text="[img]", font=('Arial', 10)).pack(side=tk.LEFT, padx=(10,5))
        except Exception as e:
            print(f"Error loading image: {e}")
            tk.Label(social_frame, text="[img err]", font=('Arial', 10)).pack(side=tk.LEFT, padx=(10,5))

 
        insta_button = tk.Button(social_frame, text="Instagram", font=('Arial', 10), command=lambda: self.open_link("https://www.instagram.com/_saul.exe/"))
        insta_button.pack(side=tk.LEFT, padx=5)

        linkedin_button = tk.Button(social_frame, text="LinkedIn", font=('Arial', 10), command=lambda: self.open_link("https://www.linkedin.com/in/saull16/"))
        linkedin_button.pack(side=tk.LEFT, padx=5)

        github_button = tk.Button(social_frame, text="GitHub", font=('Arial', 10), command=lambda: self.open_link("https://github.com/saul0106exe"))
        github_button.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()