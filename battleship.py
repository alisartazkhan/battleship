''' 
File: battleship.py
Author: Ali Sartaz Khan
Description: Built some classes that will be called by
another program. These classes try to simulate the game
of battleship.
'''


class Node:
    '''This class creates a node object.
    The constructor creates 3 attributes, val, ship, coordinate,
    that give the user information on the ship.

    No additional methods created.
   '''
    def __init__(self, ship, coordinate, val):
        '''Constructor for creating 3 attributes. Accepts 3 parameters
        and returns nothing.

        ship: ship object
        coordinate: coordinate in board (list)
        val: name of ship
        '''
        self.val = val
        self.ship = ship
        self.coordinate = coordinate

class Ship:
    '''Class creates a ship object.
    Constructor creates attributes that contain information about
    the ship.

    Additional Methods:
    print(self): prints the ship showing which parts are hit and
    its name.
    is_sunk(self): returns true or false on whether the ship is sunk.
    rotate(self, amount): rotates the coordinates of the ship with
    respect to (0,0).
    '''

    def __init__(self, name, shape):
        '''Constructor for the name creates attributes for name,
        shape, and a backup attribute containing the final coordinates
        of the list. Accepts 2 parameters and returns nothing.

        name: name of ship
        shape: a list of coordinates
        '''
        self.name = name
        self.shape = []
        self.backup_coord = None
        # changing tuples in the shape parameter into lists
        for i in range(len(shape)):
            coordinate = shape[i]
            x = coordinate[0]
            y = coordinate[1]
            self.shape.append([x, y])
        self.final = self.shape


    def print(self):
        '''Prints out the state of the ship. Prints '*' if ship
        is hit. Prints all '*'s if ship is sunk alongside ship name.
        Accepts only self parameter and returns nothing.
        '''

        final = ''
        for coordinate in self.final:
            if coordinate == '*' or coordinate == 'X':
                final += '*'
            else:
                final += self.name[0]
        for_print = '{:10}' + self.name
        print(for_print.format(final))

    def is_sunk(self):
        '''Checks whether ship is sunk. Accepts onlys
        self parameter and returns only True and False.
        '''
        for coordinate in self.final:
            if coordinate != 'X':
                return False

        return True

    def rotate(self, amount):
        '''Rotates the coordinates of the ship with respect to
        (0,0). Rotates in only 90 degree intervals. Accepts 1
        parameter and returns nothing.

        amount: interval amount (int)
        '''
        assert 0 <= amount <= 3
        # attribute containing final coordinates
        self.final = copy_list(self.shape)

        for rotation in range(amount):
            for i in range(len(self.final)):
                coordinate = self.final[i]
                x = coordinate[0]
                y = coordinate[1]
                coordinate = [x, y]
                if x == 0 and y == 0:
                    continue
                elif x == 0:
                    coordinate = [y,x]
                else:
                    coordinate = [y, -x]

                self.final[i] = coordinate


def copy_list(lst):
    '''Helper function used to copy lists.
    Accepts 1 parameter and returns new list.

    lst: list
    '''
    new = []
    for i in lst:
        new.append(i)
    return new


class Board:
    '''Class creates a board object to play battleship on.
    The constructor creates a size and board attribute.

    Additional methods:
    add_ship(self, ship, position): adds ship object onto the board.
    print(self): prints out the board.
    has_been_used(self, position): checks whether that position has
    been used before.
    attempt_move(self, position): makes moves on the board.
    '''

    def __init__(self, size):
        '''Constructor tht initializes attributes that contain
        size and a 2D list of objects that represent the board.append
        Accepts 1 parameter and returns nothing,

        size: size of board
        '''
        assert size > 0
        self.size = size
        self.board = []
        for i in range(size):
            temp = []
            for j in range(size):
                temp.append(Node(None, None, '.'))
            self.board.append(temp)

    def add_ship(self, ship, position):
        '''Adds ship to the board object. First it changes the coordinates
        of the ship based on the position parameter and then changes values
        in the nodes of the board list. Accepts 2 parameters and
        returns nothing.

        ship: ship object made beforehand
        position: tuple containing position on board
        '''
        x_pos = position[0]
        y_pos = position[1]
        assert 0 <= x_pos < self.size and 0 <= y_pos < self.size
        coordinates = ship.final

        temp = []
        for i in range(len(coordinates)):
            coordinate = coordinates[i]
            x = coordinate[0]
            y = coordinate[1]
            assert 0 <= x+x_pos < self.size and 0<= y+y_pos < self.size
            temp.append([x+x_pos, y+y_pos])

        for i in range(len(coordinates)):
            ship.final[i] = temp[i]


        # changes node values inside the board list
        change_node_val(self.board, ship)
        # final coordinates of ship that stays unchanged
        ship.backup_coord = copy_list(ship.final)


    def print(self):
        '''Prints the entire board. This prints the values inside
        the nodes of the board list. Accepts only self parameter
        and returns nothing.
        '''
        if self.size > 10:
            numbering = '{:>2}'
        else:
            numbering = '{:>1}'

        print(numbering.format(' '),'+-' + '--'*self.size + '+')

        for i in range(self.size-1, -1, -1):
            print(numbering.format(str(i)),'| ', end = '')
            for j in range(self.size):
                print(self.board[i][j].val[0]+' ', end = '')
            print('|')

        print(numbering.format(' '),'+-' + '--'*self.size + '+')

        # last row of index numbers
        if self.size > 10:
            numbers = []
            for i in range(self.size):
                if i < 10:
                    numbers.append('0'+str(i))
                else:
                    numbers.append(str(i))

            for j in range(2):
                print(numbering.format(' '),'  ', end = '')
                for number in numbers:
                    if j == 0 and number[0] == '0':
                        print('  ', end = '')
                    else:
                        print(number[j]+' ', end = '')
                print()
        else:
            print(numbering.format(' '),'  ', end = '')
            for i in range(self.size):
                print(str(i) + ' ', end = '')
        print()

    def has_been_used(self, position):
        '''Checks whether a particular position on the board
        has been used before. Accepts 1 parameter and returns
        True or False.

        position: tuple containing position on board
        '''
        x = position[0]
        y = position[1]
        assert 0 <= x <self.size and 0 <= y < self.size

        shot_val_list = ['o', '*', 'X']
        if self.board[y][x].val in shot_val_list:
            return True
        return False

    def attempt_move(self, position):
        '''Function to attack a particular position on the board.
        Afterward it prints out a string on whether the attack hit
        or missed or sunk a boat. Accepts 1 parameter and returns
        string.

        position: tuple containing position on board
        '''
        x = position[0]
        y = position[1]

        assert 0 <= x <self.size and 0 <= y < self.size
        assert not self.has_been_used(position)

        slot = self.board[y][x]
        retval = ''
        if slot.val == '.':
            retval = 'Miss'
            slot.val = 'o'

        else:
            retval = 'Hit'
            slot.val = '*'
            # change coordinate if one part of ship is hit
            for i in range(len(slot.ship.final)):
                coordinate = slot.ship.final[i]
                if [x, y] == coordinate:
                    slot.ship.final[i] = '*'
            # check if all points are hit
            if all_points_hit(self.board, slot.ship):
                retval = 'Sunk '+ '('+slot.ship.name+')'

        return retval

def all_points_hit(board, ship):
    '''Helper function checks whether all points of ship are hit ('*').
    It they are, then they are changed to 'X's. This change is then also
    made to the nodes in the board list using the backup coordinates of the
    ship in the ship class. Accepts 2 parameters and returns True or False.

    board: board list
    ship: ship object
    '''
    all_hit = True
    for coordinate in ship.final:
        if coordinate != '*':
            all_hit = False
            break

    if all_hit:
        for i in range(len(ship.final)):
            ship.final[i] = 'X'

        for coordinate in ship.backup_coord:
            x = coordinate[0]
            y = coordinate[1]
            board[y][x].val = 'X'

        return True

    return False




def change_node_val(board, ship):
    '''Helper function used inside the Board class for add_ship.
    This goes through the ships final coordinates and then adds new
    nodes inside the board list that contains information about the ship.
    Accepts two parameters and returns nothing.

    board: board list
    ship: ship object
    '''

    for coordinate in ship.final:
        x = coordinate[0]
        y = coordinate[1]
        assert board[y][x].val[0] == '.'
        board[y][x] = Node(ship, [x, y], ship.name)


