import PySimpleGUI as sg
import os
import copy
import random
from pattern.es import tag

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
LL = 13
M = 14
N = 15
Ñ = 16
O = 17
P = 18
Q = 19
R = 20
RR = 21
S = 22
T = 23
U = 24
V = 25
W = 26
X = 27
Y = 28
Z = 29

# Orientacion de las palabras
ORIENTATION_RIGHT = 1
ORIENTATION_DOWN = 2
ORIENTATION_ERROR = -1
ORIENTATION_NONE = 0

# Tablero en blanco de 10x10
initial_tablero = [[BLANK, ] * 10, [BLANK, ] * 10, [BLANK, ] * 10, [BLANK, ] * 10, [BLANK, ] * 10,
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
ll = {'letra': 'LL', 'imagen': os.path.join(PATH, 'll.png')}
m = {'letra': 'M', 'imagen': os.path.join(PATH, 'm.png')}
n = {'letra': 'N', 'imagen': os.path.join(PATH, 'n.png')}
ñ = {'letra': 'Ñ', 'imagen': os.path.join(PATH, 'ñ.png')}
o = {'letra': 'O', 'imagen': os.path.join(PATH, 'o.png')}
p = {'letra': 'P', 'imagen': os.path.join(PATH, 'p.png')}
q = {'letra': 'Q', 'imagen': os.path.join(PATH, 'q.png')}
r = {'letra': 'R', 'imagen': os.path.join(PATH, 'r.png')}
rr = {'letra': 'RR', 'imagen': os.path.join(PATH, 'rr.png')}
s = {'letra': 'S', 'imagen': os.path.join(PATH, 's.png')}
t = {'letra': 'T', 'imagen': os.path.join(PATH, 't.png')}
u = {'letra': 'U', 'imagen': os.path.join(PATH, 'u.png')}
v = {'letra': 'V', 'imagen': os.path.join(PATH, 'v.png')}
w = {'letra': 'W', 'imagen': os.path.join(PATH, 'w.png')}
x = {'letra': 'X', 'imagen': os.path.join(PATH, 'x.png')}
y = {'letra': 'Y', 'imagen': os.path.join(PATH, 'y.png')}
z = {'letra': 'Z', 'imagen': os.path.join(PATH, 'z.png')}

images = {BLANK: blank, A: a, B: b, C: c, D: d, E: e, F: f,
          G: g, H: h, I: i, J: j, K: k, L: l, LL: ll, M: m, 
          N: n, Ñ: ñ, O: o, P: p, Q: q, R: r, RR: rr, S: s,
          T: t, U: u, V: v, W: w, X: x, Y: y, Z: z}

initial_atril = []

images_keys = list(images.keys())
images_keys.remove(0)
for i in range(0,7):
    initial_atril.append(random.choice(images_keys))

def render_square(image, key, location):
    return sg.RButton('', image_filename=image, size=(1, 1), pad=(0, 0), key=key)

'''
Refresca el atril en base a un movimiento. Esto se realiza haciendo un update en
los botones dependiento los nuevos valores del "board"
En este caso, si encuentra valores en 0,
actualizaría la imagen del boton con un "blank"
'''
def redraw_atril(window, board):
    for i in range(7):
        piece_image = images[board[i]]['imagen']
        elem = window.FindElement(key=i)
        elem.Update(image_filename=piece_image)

'''
Refresca el tablero en base a un movimiento. Esto se realiza haciendo un update en
los botones dependiento los nuevos valores del "board"
'''
def redraw_tablero(window, board):
    for i in range(10):
        for j in range(10):
            piece_image = images[board[i][j]]['imagen']
            elem = window.FindElement(key=(i, j))
            elem.Update(image_filename=piece_image)

# Define qué tipo de movimiento se debera seguir en la agregacion de letras al tablero
def get_orientation(movimiento_actual, movimiento_anterior):
    orientation = ORIENTATION_ERROR
    # eje X sumo 1 y la Y quedo igual, se va pa la derecha
    if movimiento_anterior[0] == movimiento_actual[0] and movimiento_anterior[1]+1 == movimiento_actual[1]:
        orientation = ORIENTATION_RIGHT
    if movimiento_anterior[0]+1 == movimiento_actual[0] and movimiento_anterior[1] == movimiento_actual[1]:
        orientation = ORIENTATION_DOWN
    return orientation

'''
Define si el movimiento es el correcto dependiendo de qué sentido se haya
fijado al principio de agregada la segunda letra
'''
def correct_movement(movimiento_actual, movimiento_anterior, orientation):
    if get_orientation(movimiento_actual, movimiento_anterior) == orientation:
        return True
    else:
        return False

def Play():
    board_tablero = copy.deepcopy(initial_tablero)
    board_atril = copy.deepcopy(initial_atril)

    # Genero una matriz de 10x10 de tipo RButton con las imagenes en blanco
    tablero = []
    for i in range(10):
        row = []
        for j in range(10):
            piece_image = images[board_tablero[i][j]]
            row.append(render_square(piece_image['imagen'], key=(i, j), location=(i, j)))
        tablero.append(row)

    # Genero un array de 7 elementos de tipo RButton con las imágenes de las letras aleatorias
    atril = []
    for i in range(7):
        row = []
        piece_image = images[board_atril[i]]
        row.append(render_square(piece_image['imagen'], key=i, location=i))
        atril.append(row)

    board_tab = [[sg.Button('CHECK')], [sg.Column(atril), sg.Column(tablero)]]
    window = sg.Window('ScrabbleAr', default_button_element_size=(12, 1), auto_size_buttons=False).Layout(board_tab)

    word = ''
    move_from = move_to = -1
    first_movement = True
    orientation = ORIENTATION_NONE
    # Temporal para no permitir el click en el atril de los "blancos"
    keys_chosen = []

    while True:
        while True:
            button, value = window.Read()
            if button == 'CHECK':
                if len(word) >= 2 and len(word) <=7:
                    wordType = tag(word)[0][1]
                    if wordType == 'VB':
                        sg.Popup('La palabra existe y es un verbo: ', word)
                    else:
                        sg.Popup('La palabra no es un verbo: ', word)
                    # Si esta bien, calcular puntos y luego cambia el turno
                else:
                    sg.Popup('Atención: ', 'La palabra formada no cumple con los mínimos ni máximos')
            if button in (None, 'Exit'):
                exit()
            # Click origen
            if type(button) is int:
                if button in keys_chosen:
                    sg.Popup('Atención: ', 'Click incorrecto, este elemento esta vacio')
                    break
                if move_from != -1:
                    sg.Popup('Atención: ', 'Click incorrecto, debe insistir en el tablero')
                    break
                move_from = button
                # Busco que numero de letra esta en la posicion clickeada
                piece = board_atril[move_from]
                letter_choosen = images[board_atril[move_from]]['letra']
                keys_chosen.append(button)
            # click destino
            if type(button) is tuple:
                if move_from == -1:
                    sg.Popup('Atención: ', 'Click incorrecto, debe insistir en el atril')
                    break
                move_to = button
                row, col = move_to

                if first_movement == False:
                    if orientation == ORIENTATION_NONE:
                        orientation = get_orientation(move_to, move_to_anterior)
                    if orientation == ORIENTATION_ERROR:
                        sg.Popup('Atención: ', 'No se pudo calcular el sentido')
                        orientation = ORIENTATION_NONE
                        break
                    if not correct_movement(move_to, move_to_anterior, orientation):
                        sg.Popup('Atención: ', 'Movimiento incorrecto')
                        break

                # La posicion de la letra que se fue queda en 0
                board_atril[move_from] = BLANK
                # El tablero queda con el numero "nuevo"
                board_tablero[row][col] = piece
                # Luego tengo que "redibujar" ambos tableros
                redraw_atril(window, board_atril)
                redraw_tablero(window, board_tablero)
                word = word + letter_choosen

                move_to_anterior = move_to
                move_from = move_to = -1
                first_movement = False
                break

Play()