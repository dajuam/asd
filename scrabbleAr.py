import PySimpleGUI as sg
import os
import sys
import copy
import random

PATH = '.'

BLANK = 0
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

tablero_inicial = [[BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8]

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

atril_inicial = []
for i in range(0,6):
    n = random.choice(list(images.keys()))
    if n == 0:
        # para evitar el blanco
        atril_inicial.append(KINGB)
    else:
        atril_inicial.append(n)

def render_square(image, key, location):
    return sg.RButton('', image_filename=image, size=(1, 1), pad=(0, 0), key=key)

def redraw_atril(window, board):
    for i in range(6):
        piece_image = images[board[i]]
        elem = window.FindElement(key=i)
        elem.Update(image_filename=piece_image)

def redraw_tablero(window, board):
    for i in range(8):
        for j in range(8):
            piece_image = images[board[i][j]]
            elem = window.FindElement(key=(i, j))
            elem.Update(image_filename=piece_image)

def PlayGame():
    psg_board = copy.deepcopy(tablero_inicial)
    # cantidad de tableros como de jugadores
    board_atril = copy.deepcopy(atril_inicial)

    # genero el tablero principal
    tablero = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'abcdefgh']]
    # loop though board and create buttons with images
    for i in range(8):
        row = [sg.T(str(8 - i) + '   ', font='Any 13')]
        for j in range(8):
            piece_image = images[psg_board[i][j]]
            row.append(render_square(piece_image, key=(i, j), location=(i, j)))
        row.append(sg.T(str(8 - i) + '   ', font='Any 13'))
        tablero.append(row)
    # add the labels across bottom of board
    tablero.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'abcdefgh'])

    # genero el atril
    atril = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'a']]
    # loop though board and create buttons with images
    for i in range(6):
        row = [sg.T(str(6 - i) + '   ', font='Any 13')]
        piece_image = images[board_atril[i]]
        row.append(render_square(piece_image, key=i, location=j))
        row.append(sg.T(str(6 - i) + '   ', font='Any 13'))
        atril.append(row)
    # add the labels across bottom of board
    atril.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'a'])

    board_tab = [[sg.Column(atril), sg.Column(tablero)]]

    # the main window layout
    layout = [[sg.TabGroup([[sg.Tab('Tablero', board_tab)]], title_color='red')]]

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
                if type(button) is int:            
                    print("origen")
                    move_from = button
                    row = move_from
                    piece = board_atril[row]  # get the move-from piece
                    #button_square = window.FindElement(key=(row, col))
                    #button_square.Update(button_color=('white', 'red'))
                    move_state = 1
                if type(button) is tuple:
                    # Destino
                    print("destino")
                    move_to = button
                    row, col = move_to

                    # if move_to == move_from:  # cancelled move
                    #     color = '#B58863' if (row + col) % 2 else '#F0D9B5'
                    #     #button_square.Update(button_color=('white', color))
                    #     move_state = 0
                    #     continue

                    #picked_move = '{}{}{}{}'.format('abcdefgh'[move_from, 8 - move_from,'abcdefgh'[move_to[1]], 8 - move_to[0])

                    #board.push(chess.Move.from_uci(picked_move))

                    board_atril[move_from] = BLANK  # place blank where piece was
                    psg_board[row][col] = piece  # place piece in the move-to square

                    redraw_atril(window, board_atril)
                    redraw_tablero(window, psg_board)
                    move_count += 1
                    turno = "jugador_dos"
                    break
        else:
            print("Juega oponente")
            turno = "jugador_uno"
    sg.Popup('Game over!', 'Thank you for playing')

PlayGame()