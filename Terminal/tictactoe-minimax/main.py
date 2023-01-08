from tkinter import *
import sys
import os
import time
import random


def rcd_generator(matrix):
    return ((matrix['1'], matrix['2'], matrix['3']),
            (matrix['4'], matrix['5'], matrix['6']),
            (matrix['7'], matrix['8'], matrix['9']),
            (matrix['1'], matrix['4'], matrix['7']),
            (matrix['2'], matrix['5'], matrix['8']),
            (matrix['3'], matrix['6'], matrix['9']),
            (matrix['1'], matrix['5'], matrix['9']),
            (matrix['7'], matrix['5'], matrix['3']))


def win(rcd):
    for i in rcd:
        if i[0] == i[1] == i[2]:
            if [] not in i:
                return True
    return False


def win_check(rcd, mark):
    for i in rcd:
        if i[0] == i[1] == i[2] == mark:
            if [] not in i:
                return True
    return False


def run_turn(x):
    current_button.set(x)


def play_game(game_mode, player, symbol, matrix, counter):
    if counter < 9:
        single_turn = game_mode(
            player[counter % 2], symbol[counter % 2], matrix
        )
        if not single_turn:
            play_game(game_mode, player, symbol, matrix, counter)
        if win(rcd_generator(matrix)) == True:
            result_label.config(
                text=f"Congratulations! {player[counter % 2]} wins!")
            print(f"{player[counter % 2]} wins!")
        else:
            play_game(game_mode, player, symbol, matrix, counter+1)
    else:
        result_label.config(text="Draw! Tie! Draw!")
        print('Tie')


def start_game(game_mode):
    play_game(game_mode, ('player1', 'player2'),
              (' X', ' O'),
              {'1': [], '2': [], '3': [],
              '4': [], '5': [], '6': [],
               '7': [], '8': [], '9': []},
              0)


def minimax_algorithm(matrix, depth, isMaximizing):
    if (win_check(rcd_generator(matrix), ' X')):
        return 1
    if (win_check(rcd_generator(matrix), ' O')):
        return -1
    if (check_for_a_tie(matrix)):
        return 0

    if (isMaximizing):
        best_score = -800
        for key in matrix.keys():
            if not matrix[key]:
                matrix[key] = ' X'
                score = minimax_algorithm(matrix, depth + 1, False)
                matrix[key] = []
                if (score > best_score):
                    best_score = score
        return best_score

    best_score = 800
    for key in matrix.keys():
        if not matrix[key]:
            matrix[key] = ' O'
            score = minimax_algorithm(matrix, depth + 1, True)
            matrix[key] = []
            if (score < best_score):
                best_score = score
    return best_score


def check_for_a_tie(board):
    for key in board.keys():
        if (board[key] == []):
            return False
    return True


def game_mode_two_real_players(player, symbol, matrix):
    instructions_label.config(
        text="Two real players mode")
    window.wait_variable(current_button)
    if matrix[current_button.get()]:
        return False
    matrix[current_button.get()] = symbol
    buttons[int(current_button.get())-1]['text'] = symbol
    return True


def game_mode_ai_vs_player(player, symbol, matrix):
    instructions_label.config(
        text="AI vs Player mode")
    if player == "player1":
        best_score = -800
        bestMove = 0
        for key in matrix.keys():
            if not matrix[key]:
                matrix[key] = symbol
                score = minimax_algorithm(matrix, 0, False)
                matrix[key] = []
                if (score > best_score):
                    best_score = score
                    bestMove = key
        matrix[bestMove] = symbol
        buttons[int(bestMove)-1]['text'] = symbol
    else:
        window.wait_variable(current_button)
        enter = current_button.get()
        time.sleep(1)
        if matrix[enter]:
            return False
        matrix[enter] = symbol
        buttons[int(current_button.get())-1]['text'] = symbol
    return True


def game_mode_player_vs_ai(player, symbol, matrix):
    instructions_label.config(
        text="Player vs AI mode")
    if player == "player1":
        window.wait_variable(current_button)
        enter = current_button.get()
        if matrix[enter]:
            return False
        matrix[enter] = symbol
        buttons[int(current_button.get())-1]['text'] = symbol
    else:
        best_score = 800
        bestMove = 0

        for key in matrix.keys():
            if not matrix[key]:
                matrix[key] = symbol
                score = minimax_algorithm(matrix, 0, True)
                matrix[key] = []
                if (score < best_score):
                    best_score = score
                    bestMove = key
        matrix[bestMove] = symbol
        buttons[int(bestMove)-1]['text'] = symbol
    return True


def game_mode_player_vs_random(player, symbol, matrix):
    instructions_label.config(
        text="Player vs Random mode")
    if player == "player1":
        window.wait_variable(current_button)
        enter = current_button.get()
        if matrix[enter]:
            return False
        matrix[enter] = symbol
        buttons[int(current_button.get())-1]['text'] = symbol
    else:
        empty_items = [key for key, values in matrix.items() if values == []]
        x = random.choice(empty_items)
        matrix[x] = symbol
        buttons[int(x)-1]['text'] = symbol
    return True


def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)


window = Tk()
window.title('Tic Tac Toe Game')
window.config(padx=10, pady=10)

current_button = StringVar()

menu_buttons = [Button(width=12, text='Two real players', bd=3, fg='navy blue', command=lambda: start_game(game_mode_two_real_players)),
                Button(width=12, text='Player vs Random', bd=3,
                       fg='navy blue', command=lambda: start_game(game_mode_player_vs_random)),
                Button(width=12, text='AI vs player', bd=3,
                       fg='navy blue', command=lambda: start_game(game_mode_ai_vs_player)),
                Button(width=12, text='Player vs AI', bd=3,
                       fg='navy blue', command=lambda: start_game(game_mode_player_vs_ai))
                ]
menu_bar_buttons = [menu_buttons[i].grid(
    row=1, column=i, sticky=W, pady=20, padx=10) for i in range(4)]

buttons = [Button(text="", font=('calibri', 60),  bd=6, fg='navy blue',
                  command=lambda x=n: run_turn(str(x))) for n in range(1, 10)]

row = 2
col = 0
for i in range(9):
    buttons[i].grid(row=row, column=col,  sticky=N+W+S+E)
    col += 1
    if col == 3:
        row += 1
        col = 0


restart_button = Button(text='r\ne\ns\nt\na\nr\nt', font=(
    'calibri', 20),  width=2, height=10, fg='purple', bd=4, command=restart)
restart_button.grid(row=2, column=3, rowspan=3)

result_label = Label(text="",
                     font=('calibri', 20),  bd=6, fg='navy blue', pady=20, padx=10)
result_label.grid(row=6, column=0, columnspan=4, sticky=W)
instructions_label = Label(text="Choose the game mode first :)",
                           font=('calibri', 12),  bd=6, fg='navy blue', pady=0, padx=5)
instructions_label.grid(row=0, column=0, columnspan=4, sticky=W)

mainloop()
