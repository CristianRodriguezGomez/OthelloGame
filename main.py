import tkinter as tk
from tkinter import messagebox
from game_logic import OthelloGame, Element

class OthelloGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Othello con AI")
        self.game = OthelloGame()

        self.board_frame = tk.Frame(root)
        self.board_frame.pack()
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.create_board()

        self.info_frame = tk.Frame(root)
        self.info_frame.pack()
        self.info_label = tk.Label(self.info_frame, text="Turno: X", font=("Arial", 14))
        self.info_label.pack()

        self.reset_button = tk.Button(self.info_frame, text="Reiniciar", command=self.reset_game)
        self.reset_button.pack()

    def create_board(self):
        for row in range(8):
            for col in range(8):
                button = tk.Button(
                    self.board_frame,
                    text=' ',
                    width=4,
                    height=2,
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button
        self.update_board()

    def update_board(self):
        # Actualiza el tablero visualmente en función del estado del juego
        for row in range(8):
            for col in range(8):
                piece = self.game.board[row][col]
                button = self.buttons[row][col]
                # Actualiza el texto del botón con la pieza correspondiente (X o O)
                button['text'] = piece.value if piece != Element.E else ' '
                # Marca los movimientos válidos en verde
                valid_moves = self.game.has_valid_moves(self.game.current_player)
                if (row, col) in valid_moves:
                    button.config(bg='lightgreen')  # Casilla válida
                else:
                    button.config(bg='lightgray')  # Casilla no válida (color normal)

        # Verifica si el juego ha terminado
        if self.game.game_over():
            winner = self.game.winner()
            self.show_winner(winner)

    def make_move(self, row, col):
        current_player = self.game.current_player
        if self.game.apply_move(row, col, current_player):
            self.update_board()
            x_count, o_count = self.game.count_pieces()
            self.info_label['text'] = f"Turno: {self.game.current_player.value} | X: {x_count}, O: {o_count}"
        else:
            messagebox.showerror("Movimiento inválido", "¡Esa casilla no es válida!")

    def reset_game(self):
        self.game = OthelloGame()
        self.update_board()
        self.info_label['text'] = "Turno: X"

    def show_winner(self, winner):
        if winner is None:
            messagebox.showinfo("Fin del juego", "¡Es un empate!")
        else:
            messagebox.showinfo("Fin del juego", f"¡El ganador es {winner.value}!")
        self.reset_game()  # Reinicia el juego después de mostrar el ganador

if __name__ == "__main__":
    root = tk.Tk()
    gui = OthelloGUI(root)
    root.mainloop()
