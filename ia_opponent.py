import socketIO_client
from minimax import get_move, score, minimax_searcher, parse_board, parse_move, alphabeta_searcher, pick_strategy, weighted_score, pick_heuristic

# s = socketIO_client.SocketIO('192.168.1.111', 3000)
s = socketIO_client.SocketIO('localhost', 3000)
s.connect()
s.emit('signin', {'user_name': "Opponent", 'tournament_id': 12, 'user_role': 'player'})


def onok():
    print 'exito en el signin'


def elready(data):
    board = data["board"]
    player = data["player_turn_id"]
    new_board = parse_board(board)

    strategy = alphabeta_searcher(5, score)
    move = get_move(strategy, player, new_board)
    # print('player', player)
    move_parsed = parse_move(move)
    s.emit(
        'play',
        {
            'tournament_id': 12,
            'player_turn_id': data['player_turn_id'],
            'game_id': data['game_id'],
            'movement': move_parsed  # randint(0, 64)
        }
    )


def elfinish(data):
    s.emit('player_ready', {'tournament_id': 12, 'player_turn_id': data['player_turn_id'], 'game_id': data['game_id']})
    if data["player_turn_id"] == data["winner_turn_id"]:
        print("Gane")
    else:
        print("Perdi")
    # print data
    # print 'terminado'


s.on('ok_signin', onok)
s.on('ready', elready)
s.on('finish', elfinish)
s.wait()
