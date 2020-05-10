import PySimpleGUI as sg
import os
import copy
import random
from pattern.es import parse

PATH = '.'

# De la A a la L por ahora
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

# Orientacion de las palabras
ORIENTATION_RIGHT = 1
ORIENTATION_DOWN = 2
ORIENTATION_ERROR = -1
ORIENTATION_NONE = 0

# Tablero en blanco de 10x10
tablero_inicial = [[BLANK, ] * 10, [BLANK, ] * 10, [BLANK, ] * 10, [BLANK, ] * 10, [BLANK, ] * 10,
                 [BLANK, ] * 10, [BLANK, ] * 10, [BLANK, ] * 10, [BLANK, ] * 10, [BLANK, ] * 10]

# Metadata de las letras
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

images_keys = list(images.keys())
images_keys.remove(0)
for i in range(0,9):
    atril_inicial.append(random.choice(images_keys))

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

def get_orientation(movimiento_actual, movimiento_anterior):
    sentido = ORIENTATION_ERROR
    # eje X sumo 1 y la Y quedo igual, se va pa la derecha
    if movimiento_anterior[0] == movimiento_actual[0] and movimiento_anterior[1]+1 == movimiento_actual[1]:
        sentido = ORIENTATION_RIGHT
    if movimiento_anterior[0]+1 == movimiento_actual[0] and movimiento_anterior[1] == movimiento_actual[1]:
        sentido = ORIENTATION_DOWN
    return sentido

def correct_movement(movimiento_actual, movimiento_anterior, sentido):
    if get_orientation(movimiento_actual, movimiento_anterior) == sentido:
        return True
    else:
        return False

def Play():
    board_tablero = copy.deepcopy(tablero_inicial)
    # aqui deberia ir cantidad de atriles como de jugadores
    board_atril = copy.deepcopy(atril_inicial)

    # genero el tablero principal en blanco
    tablero = []
    for i in range(10):
        row = []
        for j in range(10):
            piece_image = images[board_tablero[i][j]]
            row.append(render_square(piece_image['imagen'], key=(i, j), location=(i, j)))
        tablero.append(row)

    # genero el atril con las letras aleatorias
    atril = []
    for i in range(7):
        row = []
        piece_image = images[board_atril[i]]
        row.append(render_square(piece_image['imagen'], key=i, location=j))
        atril.append(row)

    board_tab = [[sg.Button('CHECK')], [sg.Column(atril), sg.Column(tablero)]]
    window = sg.Window('ScrabbleAr', default_button_element_size=(12, 1), auto_size_buttons=False).Layout(board_tab)

    palabra = ''
    move_state = move_from = move_to = 0
    primer_movimiento = True
    sentido = ORIENTATION_NONE

    while True:
        move_state = 0
        while True:
            button, value = window.Read()
            if button == 'CHECK':
                if len(palabra) >= 2 and len(palabra) <=7:
                    sg.Popup('Palabra a chequear: ', palabra)
                    # Chequear existencia de la palabra
                    # Si esta bien, calcular puntos y luego cambia el turno
                else:
                    sg.Popup('Atención: ', 'La palabra formada no cumple con los mínimos ni máximos')
            if button in (None, 'Exit'):
                exit()
            # Click origen
            if type(button) is int:
                if move_from != 0:
                    sg.Popup('Atención: ', 'Click incorrecto, debe insistir en el tablero')
                    break
                move_from = button
                row = move_from
                piece = board_atril[row]
                letra_elegida = images[board_atril[row]]['letra']
                move_state = 1
            # click destino
            if type(button) is tuple:
                move_to = button
                row, col = move_to

                if primer_movimiento == False:
                    if sentido == ORIENTATION_NONE:
                        sentido = get_orientation(move_to, move_to_anterior)
                    if sentido == ORIENTATION_ERROR:
                        sg.Popup('Atención: ', 'No se pudo calcular el sentido')
                        sentido = ORIENTATION_NONE
                        break
                    if not correct_movement(move_to, move_to_anterior, sentido):
                        sg.Popup('Atención: ', 'Movimiento incorrecto')
                        break

                board_atril[move_from] = BLANK
                board_tablero[row][col] = piece
                redraw_atril(window, board_atril)
                redraw_tablero(window, board_tablero)
                palabra = palabra + letra_elegida

                move_to_anterior = move_to
                move_state = move_from = move_to = 0
                primer_movimiento = False
                break

Play()