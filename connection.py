import socketIO_client
from minimax import get_move, score, minimax_searcher, parse_board, parse_move, alphabeta_searcher, pick_strategy, weighted_score, pick_heuristic

# s = socketIO_client.SocketIO('192.168.1.111', 3000)
tournament_id = 12
s = socketIO_client.SocketIO('localhost', 3000)
s.connect()
s.emit('signin', {'user_name': "Adolfo Morales", 'tournament_id': tournament_id, 'user_role': 'player'})


def onok():
    print 'exito en el signin'


def elready(data):
    board = data["board"]
    player = data["player_turn_id"]
    new_board = parse_board(board)
    strategy_picked = pick_strategy(30, 30, 15)
    print(strategy_picked)
    heuristic_picked = pick_heuristic(30, 30, 15)
    if (heuristic_picked < 0.5):
        heuristic = weighted_score
    else:
        heuristic = score
    if (strategy_picked < 0.5):
        strategy = minimax_searcher(4, heuristic)
    else:
        strategy = alphabeta_searcher(5, heuristic)
    move = get_move(strategy, player, new_board)
    # print('player', player)
    move_parsed = parse_move(move)
    s.emit(
        'play',
        {
            'tournament_id': tournament_id,
            'player_turn_id': data['player_turn_id'],
            'game_id': data['game_id'],
            'movement': move_parsed  # randint(0, 64)
        }
    )


def elfinish(data):
    s.emit('player_ready', {'tournament_id': tournament_id, 'player_turn_id': data['player_turn_id'], 'game_id': data['game_id']})
    key = "winner_turn_id"
    if key in data:
        if data["player_turn_id"] == data["winner_turn_id"]:
            print("Gane")
        else:
            print("Perdi")
    else:
        print("Empate")
    # print data
    # print 'terminado'


s.on('ok_signin', onok)
s.on('ready', elready)
s.on('finish', elfinish)
s.wait()
