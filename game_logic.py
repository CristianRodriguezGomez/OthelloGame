from enum import Enum

class Element(Enum):
    O = 'O'
    X = 'X'
    E = ' '  # Empty
    L = 'L'  # Limit (optional)

class OthelloGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = Element.X

    def initialize_board(self):
        # Tablero inicial de 8x8
        board = [[Element.E for _ in range(8)] for _ in range(8)]
        # Posiciones iniciales
        board[3][3] = Element.O
        board[3][4] = Element.X
        board[4][3] = Element.X
        board[4][4] = Element.O
        return board

    def is_valid_move(self, row, col, player):
        # Verifica si un movimiento es válido
        if self.board[row][col] != Element.E:
            return False
        
        # Lógica para verificar si una dirección contiene piezas que pueden ser volteadas
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for direction in directions:
            x, y = row, col
            x += direction[0]
            y += direction[1]
            has_opponent = False

            # Buscar las piezas del oponente en esa dirección
            while 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] != Element.E:
                if self.board[x][y] != player:
                    has_opponent = True
                elif self.board[x][y] == player and has_opponent:
                    return True
                else:
                    break
                x += direction[0]
                y += direction[1]

        return False

    def apply_move(self, row, col, player):
        if not self.is_valid_move(row, col, player):
            return False
        self.board[row][col] = player
        self.flip_pieces(row, col, player)
        self.current_player = Element.O if player == Element.X else Element.X
        return True

    def flip_pieces(self, row, col, player):
        # Voltear las piezas según las reglas de Othello
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for direction in directions:
            x, y = row, col
            x += direction[0]
            y += direction[1]
            to_flip = []

            # Buscar piezas para voltear
            while 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] != Element.E:
                if self.board[x][y] == player:
                    for fx, fy in to_flip:
                        self.board[fx][fy] = player
                    break
                elif self.board[x][y] != player:
                    to_flip.append((x, y))
                x += direction[0]
                y += direction[1]

    def count_pieces(self):
        x_count = sum(row.count(Element.X) for row in self.board)
        o_count = sum(row.count(Element.O) for row in self.board)
        return x_count, o_count

    def has_valid_moves(self, player):
        # Devuelve una lista de coordenadas válidas para un movimiento
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def game_over(self):
        # Verifica si el juego ha terminado (sin movimientos válidos para ambos jugadores)
        x_valid_moves = self.has_valid_moves(Element.X)
        o_valid_moves = self.has_valid_moves(Element.O)
        if not x_valid_moves and not o_valid_moves:
            return True  # El juego terminó
        return False

    def winner(self):
        # Calcula quién ganó el juego
        x_count, o_count = self.count_pieces()
        if x_count > o_count:
            return Element.X
        elif o_count > x_count:
            return Element.O
        else:
            return None  # Empate
