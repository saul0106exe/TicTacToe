import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import random 

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
    BOT_NAMES = [
        "SL_Bot.exe", "SaulOS v2.7", "S-AI", "BugFinder9000", "SegFault Saul",
        "StackOverBot", "UCMBot", "ChapinBot", "El Juez", "SanSaul",
        "sl_bot.exe", "saulAI_0106", "SaulNet", ".SaulBot", "Lopezinator",
        "Saw", "Sal", "TurboSaul", "NitroBot", "Boost.exe", "Speedster0106",
        "Overdrive Lopez", "DriftChapin", "SaulRacerX", "No16 Saul Lopez",
        "S.Lopez GP", "ElRápido", "LagBeGone", "Botmobile", "TrackLord.exe",
        "VTECChapin", "LopezLapBot", "DraftKingBot", "PitStop.exe"
    ]
    DEFAULT_BOT_NAME = "Bot"


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

        
        self.player_symbol = 'X'  
        self.bot_symbol = 'O'    

        self.game_mode = tk.StringVar(value="PvP") 
        self.is_bot_turn_flag = False 

        game_mode_frame = tk.Frame(master)
        game_mode_frame.grid(row=0, column=0, columnspan=3, pady=(10, 0), padx=10, sticky="w")
        tk.Label(game_mode_frame, text="Game Mode:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 5))
        pvp_radio = tk.Radiobutton(game_mode_frame, text="Player vs Player", variable=self.game_mode, value="PvP", command=self.on_game_mode_change, font=('Arial', 12))
        pvp_radio.pack(side=tk.LEFT)
        pvbot_radio = tk.Radiobutton(game_mode_frame, text="Player vs Bot", variable=self.game_mode, value="PvBot", command=self.on_game_mode_change, font=('Arial', 12))
        pvbot_radio.pack(side=tk.LEFT, padx=(10, 0))

        player_info_frame = tk.Frame(master)
        player_info_frame.grid(row=1, column=0, columnspan=3, pady=(5, 5), padx=10) 

        tk.Label(player_info_frame, text="Player 1:", font=('Arial', 12)).grid(row=0, column=0, padx=(0,5), pady=2, sticky="e")
        self.p1_name_entry = tk.Entry(player_info_frame, textvariable=self.player_name_vars[0], font=('Arial', 12), width=15)
        self.p1_name_entry.grid(row=0, column=1, padx=(0,10), pady=2)

        tk.Label(player_info_frame, text="Player 2:", font=('Arial', 12)).grid(row=1, column=0, padx=(0,5), pady=2, sticky="e")
        self.p2_name_entry = tk.Entry(player_info_frame, textvariable=self.player_name_vars[1], font=('Arial', 12), width=15)
        self.p2_name_entry.grid(row=1, column=1, padx=(0,10), pady=2)

        self.status_label = tk.Label(master, text="", font=('Arial', 14), pady=10)
        self.status_label.grid(row=2, column=0, columnspan=3) 

        self.create_board_buttons() 

        controls_frame = tk.Frame(master)
        controls_frame.grid(row=4, column=0, columnspan=3, pady=10) 

        reset_button = tk.Button(controls_frame, text="Restart Game", command=self.reset_game, font=('Arial', 12))
        reset_button.pack(side=tk.LEFT, padx=10)

        swap_names_button = tk.Button(controls_frame, text="Swap Names", command=self.swap_player_name_entries, font=('Arial', 12))
        swap_names_button.pack(side=tk.LEFT, padx=10)
        
        self.on_game_mode_change() 
        
        self.create_social_bar() 
    def create_board_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=3, column=0, columnspan=3) 
        for r in range(3):
            for c in range(3):
                button = tk.Button(button_frame, text=' ', font=('Arial', 40, 'bold'),
                                   width=3, height=1, relief=tk.GROOVE, borderwidth=2,
                                   command=lambda row=r, col=c: self.on_button_click(row, col))
                button.grid(row=r, column=c, padx=2, pady=2)
                self.board_buttons[r][c] = button
    
    def on_game_mode_change(self):
        current_p2_name_in_var = self.player_name_vars[1].get()
        if self.game_mode.get() == "PvBot":
            self.p2_name_entry.config(state=tk.DISABLED)
        else: 
            self.p2_name_entry.config(state=tk.NORMAL)
            if current_p2_name_in_var in self.BOT_NAMES or current_p2_name_in_var == self.DEFAULT_BOT_NAME:
                self.player_name_vars[1].set("Player 2")

        self.reset_game()

    def configure_new_round(self):
        self.player_names_actual[0] = self.player_name_vars[0].get() or "Player 1"
        
        if self.game_mode.get() == "PvBot":
            self.player_names_actual[1] = self.player_name_vars[1].get()
            if self.starter_player_index == 0:  
                self.player_symbol = 'X' 
                self.bot_symbol = 'O'    
                self.current_turn_player_name = self.player_names_actual[0] 
                self.current_turn_symbol = 'X' 
                self.is_bot_turn_flag = False
            else:  
                self.bot_symbol = 'X'   
                self.player_symbol = 'O' 
                self.current_turn_player_name = self.player_names_actual[1]  
                self.current_turn_symbol = 'X' 
                self.is_bot_turn_flag = True
        else:  
            self.player_names_actual[1] = self.player_name_vars[1].get() or "Player 2"
            if self.player_names_actual[0] == self.player_names_actual[1] and self.player_names_actual[0] != "Bot":
                self.player_names_actual[0] = f"{self.player_names_actual[0]} (X)"
                self.player_names_actual[1] = f"{self.player_names_actual[1]} (O)"
            

            self.current_turn_symbol = 'X'
            self.current_turn_player_name = self.player_names_actual[self.starter_player_index]
            self.is_bot_turn_flag = False

        self.update_status_label(f"{self.current_turn_player_name}'s turn ({self.current_turn_symbol})")

        if self.game_mode.get() == "PvBot" and self.is_bot_turn_flag and not self.game_over:
            self.master.after(100, self.trigger_bot_move) 


    def on_button_click(self, row, col):
        if self.game_over or self.board_state[row][col] != ' ':
            return

        symbol_to_place = self.current_turn_symbol
        self.board_state[row][col] = symbol_to_place
        
        button_color = 'red' if symbol_to_place == 'X' else 'blue'
        self.board_buttons[row][col].config(text=symbol_to_place, state=tk.DISABLED,
                                            disabledforeground=button_color)

        if self.game_mode.get() == "PvBot" and self.is_bot_turn_flag:
            return

        if check_win(self.board_state, symbol_to_place):
            self.game_over = True
            winner_name = self.current_turn_player_name
            self.update_status_label(f"🥳{winner_name} wins!🎉")
            self.disable_all_board_buttons()
            return 
        elif check_draw(self.board_state):
            self.game_over = True
            self.update_status_label("It's a draw!")
            self.disable_all_board_buttons()
            return
        
        if self.game_mode.get() == "PvBot":
        
            self.current_turn_player_name = self.player_names_actual[1]
            self.current_turn_symbol = self.bot_symbol
            self.is_bot_turn_flag = True
            self.update_status_label(f"{self.current_turn_player_name}'s turn ({self.current_turn_symbol})")
            self.master.after(500, self.trigger_bot_move)
        else:
            player_x_name_for_round = self.player_names_actual[self.starter_player_index]
            player_o_name_for_round = self.player_names_actual[1 - self.starter_player_index]

            if self.current_turn_symbol == 'X': 
                self.current_turn_player_name = player_o_name_for_round
                self.current_turn_symbol = 'O'
            else:  
                self.current_turn_player_name = player_x_name_for_round
                self.current_turn_symbol = 'X'
            self.update_status_label(f"{self.current_turn_player_name}'s turn ({self.current_turn_symbol})")

    def trigger_bot_move(self):
        if self.game_over or not self.is_bot_turn_flag:
            return

        move = self._find_best_bot_move()
        if move:
            row, col = move
            
            symbol_to_place = self.bot_symbol
            self.board_state[row][col] = symbol_to_place
            
            button_color = 'red' if symbol_to_place == 'X' else 'blue'
            self.board_buttons[row][col].config(text=symbol_to_place, state=tk.DISABLED,
                                                disabledforeground=button_color)

            if check_win(self.board_state, symbol_to_place):
                self.game_over = True
                winner_name = self.player_names_actual[1] 
                self.update_status_label(f"🥳{winner_name} wins!🎉")
                self.disable_all_board_buttons()
                self.is_bot_turn_flag = False 
                return
            elif check_draw(self.board_state):
                self.game_over = True
                self.update_status_label("It's a draw!")
                self.disable_all_board_buttons()
                self.is_bot_turn_flag = False 
                return
            
            self.current_turn_player_name = self.player_names_actual[0]
            self.current_turn_symbol = self.player_symbol
            self.is_bot_turn_flag = False
            self.update_status_label(f"{self.current_turn_player_name}'s turn ({self.current_turn_symbol})")
        else:
            if not check_draw(self.board_state): 
                 print("Error: Bot couldn't find a move on a non-terminal board.")
            self.is_bot_turn_flag = False

    def _find_best_bot_move(self):
        human_actual_symbol = self.player_symbol

        move = self._find_critical_move(self.board_state, self.bot_symbol)
        if move: return move

        move = self._find_critical_move(self.board_state, human_actual_symbol)
        if move: return move

        if self.board_state[1][1] == ' ':
            return (1, 1)

        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for r_c_tuple in corners:
            if self.board_state[r_c_tuple[0]][r_c_tuple[1]] == ' ':
                return r_c_tuple

        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        random.shuffle(sides)
        for r_c_tuple in sides:
            if self.board_state[r_c_tuple[0]][r_c_tuple[1]] == ' ':
                return r_c_tuple
        
        available_moves = []
        for r_idx in range(3):
            for c_idx in range(3):
                if self.board_state[r_idx][c_idx] == ' ':
                    available_moves.append((r_idx, c_idx))
        if available_moves:
            return random.choice(available_moves)
        return None 

    def _find_critical_move(self, board, symbol_to_check):
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = symbol_to_check
                    if check_win(board, symbol_to_check):
                        board[r][c] = ' '
                        return (r, c)
                    board[r][c] = ' '
        return None

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
        
        current_game_mode = self.game_mode.get()
        if current_game_mode == "PvBot":
            chosen_bot_name = random.choice(self.BOT_NAMES) if self.BOT_NAMES else self.DEFAULT_BOT_NAME
            self.player_name_vars[1].set(chosen_bot_name)
            self.p2_name_entry.config(state=tk.DISABLED)
        else:
            self.p2_name_entry.config(state=tk.NORMAL)
            if self.player_name_vars[1].get() == self.DEFAULT_BOT_NAME: 
                 self.player_name_vars[1].set("Player 2")

        self.configure_new_round()

        for r_idx in range(3): 
            for c_idx in range(3): 
                self.board_buttons[r_idx][c_idx].config(text=' ', state=tk.NORMAL)
        
    def is_any_move_made(self):
        for row_data in self.board_state:
            if any(cell != ' ' for cell in row_data):
                return True
        return False


    def swap_player_name_entries(self):
        if self.game_mode.get() == "PvBot":
            messagebox.showinfo("Swap Names", "Player 2 is the Bot. Names cannot be swapped in this mode.")
            return

        name0 = self.player_name_vars[0].get()
        name1 = self.player_name_vars[1].get()
        self.player_name_vars[0].set(name1)
        self.player_name_vars[1].set(name0)
        
        if self.game_over or not self.is_any_move_made():
            self.reset_game() 

    def open_link(self, url):
        webbrowser.open_new_tab(url)
    def create_social_bar(self):
        social_frame = tk.Frame(self.master, pady=5, bg="gray") 
        social_frame.grid(row=5, column=0, columnspan=3, sticky="ew")

        try:
            img_path = "me1.jpg"
            original_image = Image.open(img_path)
            resized_image = original_image.resize((50, 50), Image.Resampling.LANCZOS)
            self.social_image_tk = ImageTk.PhotoImage(resized_image)
            
            image_label = tk.Label(social_frame, image=self.social_image_tk, bg="gray")
            image_label.pack(side=tk.LEFT, padx=(10, 5))
        except FileNotFoundError:
            print(f"Error: Image file '{img_path}' not found.")
            tk.Label(social_frame, text="[img]", font=('Arial', 10), bg="gray").pack(side=tk.LEFT, padx=(10,5))
        except Exception as e:
            print(f"Error loading image: {e}")
            tk.Label(social_frame, text="[img err]", font=('Arial', 10), bg="gray").pack(side=tk.LEFT, padx=(10,5))

        github_button = tk.Button(social_frame, text="GitHub", font=('Arial', 10), command=lambda: self.open_link("https://github.com/saul0106exe"))
        github_button.pack(side=tk.RIGHT, padx=(5, 10))


        linkedin_button = tk.Button(social_frame, text="LinkedIn", font=('Arial', 10), command=lambda: self.open_link("https://www.linkedin.com/in/saull16/"))
        linkedin_button.pack(side=tk.RIGHT, padx=10)


        insta_button = tk.Button(social_frame, text="Instagram", font=('Arial', 10), command=lambda: self.open_link("https://www.instagram.com/_saul.exe/"))
        insta_button.pack(side=tk.RIGHT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()
