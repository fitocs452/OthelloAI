import random

EMPTY, BLACK, WHITE, OUTER = 0, 1, 2, '?'

# Direccions utilizadas para el tablero (los numeros son el offset para llegar
# a la posicion)
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

# Piezas de jugador
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

SQUARE_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]

MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE


def opponent(player):
    """
        Funcion que devuelve la ficha oponente
        Params:
            Player: El jugador actual
        Return:
            Player: El otro jugador
    """
    return BLACK if player is WHITE else WHITE


def squares():
    """
        Funcion que devulve las casillas del tablero
        Return:
            Array: Posiciones de los indices de las casillas
                que se pueden utilizar
    """
    return [i for i in xrange(11, 89) if 1 <= (i % 10) <= 8]


def any_legal_move(player, board):
    """
        Funcion que verifica si un jugador tiene movimientos
        Params:
            Player: Jugador actual
            Board: El estado del tablero
        Return:
            True: Si tiene movimientos
            False: No tiene movimientos
    """
    return any(is_legal(sq, player, board) for sq in squares())


def find_bracket(square, player, board, direction):
    """
        Funcion que sirve para verificar que exista un movimiento valido
        hacia una direccion especifica para el jugador actual

        Params:
            Square: Es el movimiento (Casilla en la que se puede mover en el tablero)
            Player: Jugador actual
            Board: Estado del tablero actual
            Direccion: Posicion de DIRECTION

        Return:
            None: Si no existe
            Bracket: Si existe movimiento (Posicion real de donde se podria mover)
    """
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    return None if board[bracket] in (OUTER, EMPTY) else bracket


def is_legal(move, player, board):
    """
        Funcion que permite verificar si un movimiento es legal
        Que sea legal significa que cumpla con las caracteristicas
        de un movimiento legal en Othello
        Para esto utilizamos FIND_BRACKET
        Params:
            Move: Posicion que deseamos evaluar
            Player: Jugador actual
            Board: Estado actual del tablero
        Return:
            EMPTY: Significa que no es legal
            Move: Movimiento legal
    """
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(map(hasbracket, DIRECTIONS))


def legal_moves(player, board):
    """
        Funcion que devuelve todos los posibles movimientos respecto al tablero
        actual

        Params:
            Player: Jugador actual
            Board: Estado actual del tablero
        Return:
            Array: Posibles movimientos a realizar en el tablero (Posiciones de tablero)
    """
    return [sq for sq in squares() if is_legal(sq, player, board)]


def weighted_score(player, board):
    """
        Obtiene el SCORE del jugador
        Esto se basa en el peso de piezas del jugador menos el peso del oponente
        Params:
            Player: Jugador actual
            Board: Estado actual del tablero
    """
    opp = opponent(player)
    total = 0
    for sq in squares():
        if board[sq] == player:
            total += SQUARE_WEIGHTS[sq]
        elif board[sq] == opp:
            total -= SQUARE_WEIGHTS[sq]
    return total


def score(player, board):
    """
        Obtiene el SCORE del jugador
        Esto se basa en la cantidad de piezas del jugador menos las del oponente
        Params:
            Player: Jugador actual
            Board: Estado actual del tablero
    """
    mine, theirs = 0, 0
    opp = opponent(player)
    for sq in squares():
        piece = board[sq]
        if piece == player:
            mine += 1
        elif piece == opp:
            theirs += 1
    return mine - theirs


def final_value(player, board):
    """
        Funcion que devuelve el valor final de un jugador en el tablero
        con base en el MIN_VALUE y MAX_VALUE
    """
    diff = score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff


def make_move(move, player, board):
    """
        Funcion que aplica el movimiento a el tablero actual para
        generar un nuevo estado
        Params:
            Move: movimiento a aplicar
            Player: Jugador actual
            Board: Estado actual de tablero
        Return:
            Board: Nuevo estado del tablero con el movimiento aplicado
    """
    board[move] = player
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board


def make_flips(move, player, board, direction):
    """
        Funcion que permite hacer el cambio de las fichas en la direccion especificado
        como resultado de aplicar un movimiento
    """
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction


# Algoritmo de Minimax

# Las estrategias del maximizador son muy cortas de vista, y un jugador
# que puede considerar las implicaciones de un movimiento varias vueltas por
# adelantado podria tener una ventaja significativa.
# El algoritmo ** minimax ** hace precisamente eso.
def minimax(player, board, depth, evaluate):
    """
    El objetivo del minimax es encontrar el mejor movimiento legal del jugador
    actual, lo hace buscando en el arbol con el DEPTH (profundidad) especificado

    Params:
        Player: Jugador actual
        Board: Estado actual del tablero
        Depth: Constante de profundidad
        Evaluate: Heuristica a utilizar
    Return:
        Tuple (move, min_score):
            - move: Movimiento a aplicar
            - min_score: Minimo de puntos que se pueden alcanzar al aplicar el movimiento
    """

    # Definimos el valor el valor del tablero del oponente, esto es tan simple
    # como una llamada recursiva a minimax para el otro jugador
    def value(board):
        return -minimax(opponent(player), board, depth - 1, evaluate)[0]

    # Si no tenemos depth solo devolvemos una evaluacion del movimiento
    # sobre el tablero actual con la heuristica
    if depth == 0:
        return evaluate(player, board), None

    # Ya que queremos evaluar todas las posibilidades considerando la implicacion
    # de ventaja que tendria (tomando en cuenta el DEPTH). Obtenemos los posibles movimientos
    moves = legal_moves(player, board)

    # En caso ya no tenemos movimientos
    if not moves:
        # Eso significaria que el juego termino, entonces ganamos o perdimos
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        return value(board), None

    # Escogemos el mejor movimiento, nuestro criterio es el maximize el valor
    # de la heuristica sobre los tableros
    return max((value(make_move(m, player, list(board))), m) for m in moves)


# Alpha-Beta search

# Considerando lo que sucede cuando minimax esta evaluando dos movimientos,
# Mov1 y Mov2, en un nivel de un arbol de busqueda. Supongamos que minimax determina
# que Mov1 puede resultar en una puntuacion de ResBoard. Al evaluar Mov2, si minimax
# encuentra un movimiento en su subarbol que podria resultar en una mejor
# puntuacion que ResBoard, el algoritmo debe dejar inmediatamente de evaluar Mov2:
# el oponente nos obligara a jugar Mov1 para evitar la mayor puntuacion
# resultante de Mov2, por lo que no debe perder el tiempo determinar lo mucho mejor
# Mov2 es Mov1.

# Solo se necesita mantener la pista de 2 valores:

# - alpha: EL maximo Score que se puede alcanzar por cualquier movimiento encontrado
# - beta: EL Score con el que el oponente mantiene la ventaja
#
# Cuando el algorimo inicia, Alpha es el menor valor y Beta el mayor.
# Al seguir evaluando, si encontrar un movimiento que cause (Alpha >= Beta),
# entonces podemos dejar de buscar en los SubArboles ya que nuestro oponente
# nos puede evitar hacer ese movimiento

def alphabeta(player, board, alpha, beta, depth, evaluate):
    """
    El objetivo del minimax es encontrar el mejor movimiento legal del jugador
    actual, lo hace buscando en el arbol con el DEPTH (profundidad) especificado
    pero en este caso tomamos en cuenta Alpha y Beta para evitar seguir leyendo
    en los subarboles

    Params:
        Player: Jugador actual
        Board: Estado actual del tablero
        Depth: Constante de profundidad
        Evaluate: Heuristica a utilizar
    Return:
        Tuple (move, min_score):
            - move: Movimiento a aplicar
            - min_score: Minimo de puntos que se pueden alcanzar al aplicar el movimiento
    """

    # Si no tenemos depth solo devolvemos una evaluacion del movimiento
    # sobre el tablero actual con la heuristica
    if depth == 0:
        return evaluate(player, board), None

    def value(board, alpha, beta):
        # Like in `minimax`, the value of a board is the opposite of its value
        # to the opponent.  We pass in `-beta` and `-alpha` as the alpha and
        # beta values, respectively, for the opponent, since `alpha` represents
        # the best score we know we can achieve and is therefore the worst score
        # achievable by the opponent.  Similarly, `beta` is the worst score that
        # our opponent can hold us to, so it is the best score that they can
        # achieve.
        return -alphabeta(opponent(player), board, -beta, -alpha, depth-1, evaluate)[0]

    moves = legal_moves(player, board)
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta), None

    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            # En el caso de que uno de los movimientos da un mejor resultado que
            # beta, entonces el oponente nos evitara jugar este movimiento, entones
            # podemos dejar de buscar
            break
        val = value(make_move(move, player, list(board)), alpha, beta)
        if val > alpha:
            # Si uno de los movimientos da un mejor resultado que el mejor resultado
            # actual entonces lo sobreescribimos
            alpha = val
            best_move = move
    return alpha, best_move


def is_valid(move):
    """
        Funcion que evalua si un movimiento es valido
        Params:
            Move: movimiento o posicion en tablero
        Return:
            True: movimiento valido
            False: movimiento invalido
    """
    return isinstance(move, int) and move in squares()


def get_move(strategy, player, board):
    """
        Funcion que devuelve el movimiento escogido por la estrategia
        a utilizar con base en el tablero actual y el jugador actual
        Params:
            Strategy: Estrategia a utilizar (minimax o alphabeta)
    """
    copy = list(board)
    move = strategy(player, copy)
    if not is_valid(move) or not is_legal(move, player, board):
        raise IllegalMoveError(player, move, copy)
    return move


class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)


def minimax_searcher(depth, evaluate):
    """
        Construye la estrategia a utilizar (MINIMAX) con el depth y la heuristica
        especificada
    """
    def strategy(player, board):
        return minimax(player, board, depth, evaluate)[1]
    return strategy


def alphabeta_searcher(depth, evaluate):
    """
        Construye la estrategia a utilizar (ALPHA-BETA) con el depth y la heuristica
        especificada
    """
    def strategy(player, board):
        return alphabeta(player, board, MIN_VALUE, MAX_VALUE, depth, evaluate)[1]
    return strategy


# move = get_move(strategy(player), player, board)

def print_board(board):
    """Get a string representation of the board."""
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in xrange(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        add_symbol = board[begin:end]
        if isinstance(add_symbol, int):
            add_symbol = str(add_symbol)
        print(add_symbol, type(add_symbol))
        rep += '%d %s\n' % (row, ' '.join(add_symbol))
    return rep


def parse_board(server_board):
    """
        Generamos un tablero (tablero que entienda nuestro algoritmo implementado)
        a partir del tablero actual.
    """
    my_board = [OUTER] * 100
    # print(my_board, len(my_board))
    # print(squares(), len(squares()))
    server_board_pos = 0
    # print(server_board)
    for i in squares():
        my_board[i] = server_board[server_board_pos]
        server_board_pos += 1

    # print(my_board)
    # print_board(my_board)
    return my_board


def parse_move(move):
    """
        Funcion que parsea el movimiento escogido por el algoritmo utilizado
        hacia un movimiento que entienda el protocolo
    """
    if move >= 11 and move <= 18:
        return move - 11
    elif move >= 21 and move <= 28:
        return move - 13
    elif move >= 31 and move <= 38:
        return move - 15
    elif move >= 41 and move <= 48:
        return move - 17
    elif move >= 51 and move <= 58:
        return move - 19
    elif move >= 61 and move <= 68:
        return move - 21
    elif move >= 71 and move <= 78:
        return move - 23
    elif move >= 81 and move <= 88:
        return move - 25


def pick_strategy(N, ndice, nsix):
    M = 0                     # Cantidad de experimentos exitosos
    for i in range(N):        # Repetir experimento N veces
        alpha = 0               # Minimax
        for j in range(ndice):
            r = random.randint(1, 2)
            if r == 1:
                alpha += 1
        if alpha >= nsix:       # successful event?
            M += 1
    p = float(M) / N
    return p


def pick_heuristic(N, ndice, nsix):
    M = 0                     # Cantidad de experimentos exitosos
    for i in range(N):        # Repetir experimento N veces
        score = 0               # Minimax
        for j in range(ndice):
            r = random.randint(1, 2)
            if r == 1:
                score += 1
        if score >= nsix:       # successful event?
            M += 1
    p = float(M) / N
    return p
