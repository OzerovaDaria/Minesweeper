from blessed import Terminal
from field import Field
from minepoint import MinePoint, Value, Mask, Flag


def printCell(cell):
    if cell == Value.bomb:    color, char = BOMB, '*'
    elif cell == Value.empty: color, char = term.normal, ' '
    else: color, char = colors[cell.value], str(cell)
    print(color + char + term.normal, end='')


term = Terminal()
ONE   = term.color(38)
TWO   = term.color(73)
THREE = term.color(40)
FOUR  = term.color(136)
FIVE  = term.color(172)
SIX   = term.color(202)
SEVEN = term.color(161)
EIGHT = term.color(124)
BOMB  = term.color(9)
colors = [ term.normal, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, BOMB ]


def printPixel(x, y, pixel, color=term.noraml):
    print(term.move_xy(x, y) + color + pixel + term.normal)

def printFieldPixel(field, x, y):
    cell = field[x, y]
    if cell == Mask.closed:
        if   cell == Flag.noflag: printPixel(x, y, '?')
        elif cell == Flag.guess:  printPixel(x, y, '▻')
        elif cell == Flag.sure:   printPixel(x, y, '►')
    else:
        if   cell == Value.bomb:  printPixel(x, y, '*', BOMB)
        elif cell == Value.empty: printPixel(x, y, ' ')
        else: printPixel(x, y, str(cell), colors[cell.value])

def clamp(min, max, val):
    if val < min: return min
    if val > max: return max
    return val

def printField(field):
    print(term.clear)
    for x in range(field.size):
        for y in range(field.size):
            printFieldPixel(field, x, y)
    print(term.normal)


field = Field(5, .1)
cursor = ( 0, 0 )
movement = { 'up': 'w', 'down': 's', 'left': 'a', 'right': 'd' }
keys = { 'open': ' ' }

# print('Field with mask:')
printField(field)
printPixel(*cursor, '◉')
activeBombs = field.bombs
closedCells = field.size * field.size
print(term.move_xy(0, field.size) + 'CHEAT Bombs remain: ' + str(activeBombs))

with term.cbreak(), term.hidden_cursor():
    val = ''
    while val.lower() != 'q':
        val = term.inkey(timeout=3)
        if not val: continue

        if val in movement.values():
            x, y = cursor
            printFieldPixel(field, x, y)
            if   val == movement['up']:    y -= 1
            elif val == movement['down']:  y += 1
            elif val == movement['left']:  x -= 1
            elif val == movement['right']: x += 1
            x = clamp(0, field.size - 1, x)
            y = clamp(0, field.size - 1, y)
            cursor = (x, y)
            printPixel(x, y, '◉')
        elif val == ' ':
            if field[cursor[0], cursor[1]] == Flag.sure: continue
            bombed = field.reveal(*cursor)
            printField(field)
            if bombed:
                print('LMAO')
                break
            printPixel(*cursor, '◉')
            closedCells = 0
            for x in range(field.size):
                for y in range(field.size):
                    if field[x, y] == Mask.closed:
                        closedCells += 1
        elif val == 'm':
            cell = field[cursor[0], cursor[1]]
            flag = cell.flag

            if flag == Flag.noflag:
                flag = Flag.sure
                if cell == Value.bomb:
                    activeBombs -= 1
            elif flag == Flag.sure:
                flag = Flag.guess
                if cell == Value.bomb:
                    activeBombs += 1
            elif flag == Flag.guess:
                flag = Flag.noflag
            field[cursor[0], cursor[1]].set(flag)

        closedMarkedCells = closedCells - field.bombs + activeBombs
        print(term.move_xy(0, field.size) + 'CHEAT Bombs remain: ' + str(activeBombs) + ' '*10)
        print(term.move_xy(0, field.size + 1) + 'Cells remain: ' + str(closedMarkedCells) + ' '*10)
        if closedMarkedCells == 0:
            print('Good job')
            break

exit(1)


#some debug output
print(f'Field size: {field.size}x{field.size}')
print('Bombs:', field.bombs)

print('Field:')
for x in range(field.size):
    for y in range(field.size):
        printCell(field[x, y])
    print()

revCoord = (field.size // 2, field.size // 2)
print(f'Revealed at (0, 0):', not field.reveal(0, 0))
print(f'Revealed at {revCoord}:', not field.reveal(revCoord[0], revCoord[1]))
for x in range(field.size):
    for y in range(field.size):
        print(field[x, y].mask if field[x, y].mask != Mask.closed else ' ', end='')
    print()

