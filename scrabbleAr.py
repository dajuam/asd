import PySimpleGUI as sg
import os
import sys
import copy

PATH = '.'  # path to the chess pieces

BLANK = 0  # piece names
PAWNB = 1
KNIGHTB = 2
BISHOPB = 3
ROOKB = 4
KINGB = 5
QUEENB = 6
PAWNW = 7
KNIGHTW = 8
BISHOPW = 9
ROOKW = 10
KINGW = 11
QUEENW = 12

initial_board = [[BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8]

atril_inicial = [[BISHOPB, ] * 6]

blank = os.path.join(PATH, 'blank.png')
bishopB = os.path.join(PATH, 'nbishopb.png')
bishopW = os.path.join(PATH, 'nbishopw.png')
pawnB = os.path.join(PATH, 'npawnb.png')
pawnW = os.path.join(PATH, 'npawnw.png')
knightB = os.path.join(PATH, 'nknightb.png')
knightW = os.path.join(PATH, 'nknightw.png')
rookB = os.path.join(PATH, 'nrookb.png')
rookW = os.path.join(PATH, 'nrookw.png')
queenB = os.path.join(PATH, 'nqueenb.png')
queenW = os.path.join(PATH, 'nqueenw.png')
kingB = os.path.join(PATH, 'nkingb.png')
kingW = os.path.join(PATH, 'nkingw.png')

images = {BISHOPB: bishopB, BISHOPW: bishopW, PAWNB: pawnB, PAWNW: pawnW, KNIGHTB: knightB, KNIGHTW: knightW,
          ROOKB: rookB, ROOKW: rookW, KINGB: kingB, KINGW: kingW, QUEENB: queenB, QUEENW: queenW, BLANK: blank}

def render_square(image, key, location):
    if (location[0] + location[1]) % 2:
        color = '#B58863'
    else:
        color = '#F0D9B5'
    return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=key)

def redraw_board(window, board):
    for i in range(1):
        for j in range(6):
            color = '#B58863' if (i + j) % 2 else '#F0D9B5'
            piece_image = images[board[i][j]]
            elem = window.FindElement(key=(i, j))
            elem.Update(button_color=('white', color),
                        image_filename=piece_image, )

def redraw_board2(window, board):
    for i in range(8):
        for j in range(8):
            color = '#B58863' if (i + j) % 2 else '#F0D9B5'
            piece_image = images[board[i][j]]
            elem = window.FindElement(key=(i, j))
            elem.Update(button_color=('white', color),
                        image_filename=piece_image, )

def PlayGame():
    menu_def = [['&File', ['&Open PGN File', 'E&xit']],
                ['&Help', '&About...'], ]

    # sg.SetOptions(margins=(0,0))
    sg.ChangeLookAndFeel('GreenTan')
    # create initial board setup
    psg_board = copy.deepcopy(initial_board)
    psg_board2 = copy.deepcopy(atril_inicial)

    # the main board display layout
    board_layout = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'abcdefgh']]
    # loop though board and create buttons with images
    for i in range(8):
        row = [sg.T(str(8 - i) + '   ', font='Any 13')]
        for j in range(8):
            piece_image = images[psg_board[i][j]]
            row.append(render_square(piece_image, key=(i, j), location=(i, j)))
        row.append(sg.T(str(8 - i) + '   ', font='Any 13'))
        board_layout.append(row)
    # add the labels across bottom of board
    board_layout.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'abcdefgh'])

    atril = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'abcdef']]
    # loop though board and create buttons with images
    for i in range(1):
        row = [sg.T(str(1 - i) + '   ', font='Any 13')]
        for j in range(6):
            piece_image = images[psg_board2[i][j]]
            row.append(render_square(piece_image, key=(i, j), location=(i, j)))
        row.append(sg.T(str(1 - i) + '   ', font='Any 13'))
        atril.append(row)
    # add the labels across bottom of board
    atril.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'abcdef'])

    board_tab = [[sg.Column(atril), sg.Column(board_layout)]]

    # the main window layout
    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.TabGroup([[sg.Tab('Tablero', board_tab)]], title_color='red')]]

    window = sg.Window('ScrabbleAr',
                       default_button_element_size=(12, 1),
                       auto_size_buttons=False,
                       icon='kingb.ico').Layout(layout)

    turno = "jugador_uno"
    move_count = 1
    move_state = move_from = move_to = 0

    while True:
        if turno == "jugador_uno":
            move_state = 0
            while True:
                button, value = window.Read()
                if button in (None, 'Exit'):
                    exit()
                if type(button) is tuple:
                    # Origen
                    if move_state == 0:
                        print("origen")
                        move_from = button
                        row, col = move_from
                        piece = psg_board2[row][col]  # get the move-from piece
                        #button_square = window.FindElement(key=(row, col))
                        #button_square.Update(button_color=('white', 'red'))
                        move_state = 1
                    # Destino
                    elif move_state == 1:
                        print("destino")
                        move_to = button
                        row, col = move_to

                        # if move_to == move_from:  # cancelled move
                        #     color = '#B58863' if (row + col) % 2 else '#F0D9B5'
                        #     #button_square.Update(button_color=('white', color))
                        #     move_state = 0
                        #     continue

                        picked_move = '{}{}{}{}'.format('abcdefgh'[move_from[1]], 8 - move_from[0],'abcdefgh'[move_to[1]], 8 - move_to[0])

                        #board.push(chess.Move.from_uci(picked_move))

                        psg_board2[move_from[0]][move_from[1]] = BLANK  # place blank where piece was
                        psg_board[row][col] = piece  # place piece in the move-to square

                        redraw_board2(window, psg_board)
                        move_count += 1
                        turno = "jugador_dos"
                        break
        else:
            print("Juega oponente")
            turno = "jugador_uno"
    sg.Popup('Game over!', 'Thank you for playing')

PlayGame()
