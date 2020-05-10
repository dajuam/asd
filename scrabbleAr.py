import PySimpleGUI as sg
import os
import sys
import copy
import random

PATH = '.'

BLANK = 0
A = 1
B = 2
C = 3
D = 4
E = 5
F = 6
G = 7
H = 8
I = 9
J = 10
K = 11
L = 12

tablero_inicial = [[BLANK, ] * 10,
                 [BLANK, ] * 10,
                 [BLANK, ] * 10,
                 [BLANK, ] * 10,
                 [BLANK, ] * 10,
                 [BLANK, ] * 10,
                 [BLANK, ] * 10,
                 [BLANK, ] * 10,
                 [BLANK, ] * 10,
                 [BLANK, ] * 10]

blank = {'letra': '', 'imagen': os.path.join(PATH, 'blank.png')}
a = {'letra': 'A', 'imagen': os.path.join(PATH, 'a.png')}
b = {'letra': 'B', 'imagen': os.path.join(PATH, 'b.png')}
c = {'letra': 'C', 'imagen': os.path.join(PATH, 'c.png')}
d = {'letra': 'D', 'imagen': os.path.join(PATH, 'd.png')}
e = {'letra': 'E', 'imagen': os.path.join(PATH, 'e.png')}
f = {'letra': 'F', 'imagen': os.path.join(PATH, 'f.png')}
g = {'letra': 'G', 'imagen': os.path.join(PATH, 'g.png')}
h = {'letra': 'H', 'imagen': os.path.join(PATH, 'h.png')}
i = {'letra': 'I', 'imagen': os.path.join(PATH, 'i.png')}
j = {'letra': 'J', 'imagen': os.path.join(PATH, 'j.png')}
k = {'letra': 'K', 'imagen': os.path.join(PATH, 'k.png')}
l = {'letra': 'L', 'imagen': os.path.join(PATH, 'l.png')}

images = {A: a, B: b, C: c, D: d, E: e, F: f,
          G: g, H: h, I: i, J: j, K: k, L: l, BLANK: blank}

atril_inicial = []

for i in range(0,9):
    n = random.choice(list(images.keys()))
    if n == 0:
        # para evitar el blanco
        atril_inicial.append(A)
    else:
        atril_inicial.append(n)

def render_square(image, key, location):
    return sg.RButton('', image_filename=image, size=(1, 1), pad=(0, 0), key=key)

def redraw_atril(window, board):
    for i in range(7):
        piece_image = images[board[i]]['imagen']
        elem = window.FindElement(key=i)
        elem.Update(image_filename=piece_image)

def redraw_tablero(window, board):
    for i in range(10):
        for j in range(10):
            piece_image = images[board[i][j]]['imagen']
            elem = window.FindElement(key=(i, j))
            elem.Update(image_filename=piece_image)

def PlayGame():
    board_tablero = copy.deepcopy(tablero_inicial)
    # cantidad de tableros como de jugadores
    board_atril = copy.deepcopy(atril_inicial)
    print(board_atril)

    # genero el tablero principal
    tablero = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 10') for a in 'abcdefghij']]
    # loop though board and create buttons with images
    for i in range(10):
        row = [sg.T(str(10 - i) + '   ', font='Any 10')]
        for j in range(10):
            piece_image = images[board_tablero[i][j]]
            row.append(render_square(piece_image['imagen'], key=(i, j), location=(i, j)))
        row.append(sg.T(str(10 - i) + '   ', font='Any 10'))
        tablero.append(row)
    # add the labels across bottom of board
    tablero.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 10') for a in 'abcdefghij'])

    # genero el atril
    atril = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 10') for a in 'a']]
    # loop though board and create buttons with images
    for i in range(7):
        row = [sg.T(str(7 - i) + '   ', font='Any 10')]
        piece_image = images[board_atril[i]]
        row.append(render_square(piece_image['imagen'], key=i, location=j))
        row.append(sg.T(str(7 - i) + '   ', font='Any 10'))
        atril.append(row)
    # add the labels across bottom of board
    atril.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 10') for a in 'a'])

    # incluyo todo
    board_tab = [[sg.Column(atril), sg.Column(tablero)]]

    # the main window layout
    layout = [[sg.TabGroup([[sg.Tab('Tablero', board_tab)]], title_color='red')]]

    window = sg.Window('ScrabbleAr',
                       default_button_element_size=(12, 1),
                       auto_size_buttons=False).Layout(layout)

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
                    print("Origen")
                    move_from = button
                    row = move_from
                    piece = board_atril[row]  # get the move-from piece
                    metadata = atril_inicial[row]
                    print(images[board_atril[row]]['letra'])
                    #button_square = window.FindElement(key=(row, col))
                    #button_square.Update(button_color=('white', 'red'))
                    move_state = 1
                if type(button) is tuple:
                    # Destino
                    print("Destino")
                    move_to = button
                    row, col = move_to

                    # if move_to == move_from:  # cancelled move
                    #     color = '#B58863' if (row + col) % 2 else '#F0D9B5'
                    #     #button_square.Update(button_color=('white', color))
                    #     move_state = 0
                    #     continue

                    #picked_move = '{}{}{}{}'.format('abcdefgh'[move_from, 8 - move_from,'abcdefgh'[move_to[1]], 8 - move_to[0])

                    board_atril[move_from] = BLANK  # place blank where piece was
                    board_tablero[row][col] = piece  # place piece in the move-to square

                    redraw_atril(window, board_atril)
                    redraw_tablero(window, board_tablero)
                    move_count += 1
                    turno = "jugador_dos"
                    break
        else:
            print("Juega oponente")
            turno = "jugador_uno"
    sg.Popup('Game over!', 'Thank you for playing')

PlayGame()