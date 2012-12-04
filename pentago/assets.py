'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Pentago pieces
'''

from pentago import *;

class BLOCK(object):
    '''
    Represents a game block on the pentago board
    Note: Assigned values are important!
          DO NOT MODIFY!
    '''

    (TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT) = range(1, 5);

    def validate(self, block):
        '''
        Return false if game block is invalid, true otherwise
        '''

        if (block < BLOCK.TOP_LEFT) or (block > BLOCK.BOTTOM_RIGHT):
            return False;

        return True;

    def str(self, block):
        '''
        Returns the human-readable block
        '''

        format = "Game Block %d";

        return format % block;


class Board(object):
    '''
    The game board is a 6x6 grid which can be manipulated as 4 quarters
    called blocks i.e Four 3x3 grids. Each block can also be twisted 
    90 degrees in any direction.
    '''

    EMPTY_CELL = '.';

    def __init__(self):

        self.size = 6;
        self.block_size = self.size / 2;
        self.grid = [ [Board.EMPTY_CELL for col in range(self.size)] for row in range(self.size) ];
        self.state = GAME_STATE.IN_PLAY;

    def is_empty(self, block, cell):
        '''
        Returns True if value at block [block], cell[cell] is Board.EMPTY_CELL
        '''

        row_offset = 0 if block < BLOCK.BOTTOM_LEFT else self.block_size;
        col_offset = 0 if (block % 2 != 0) else self.block_size;

        col = (cell - 1) % self.block_size;
        row = (cell - 1) / self.block_size;

        return self.grid[row + row_offset][col + col_offset] is Board.EMPTY_CELL;

    def update(self, block, cell, colour):
        '''
        Sets value at block [block], cell[cell] to colour
        '''

        row_offset = 0 if block < BLOCK.BOTTOM_LEFT else self.block_size;
        col_offset = 0 if (block % 2 != 0) else self.block_size;

        col = (cell - 1) % self.block_size;
        row = (cell - 1) / self.block_size;

        self.grid[row + row_offset][col + col_offset] = COLOUR().str(colour);

    def rotate(self, block, direction):
        '''
        Rotates the given block of the game board in the specified direction
        '''

        if direction is DIRECTION.RIGHT:
            self.grid = self.rotate_right(block);
        else:
            self.grid = self.rotate_left(block);

    def rotate_left(self, block):
        '''
        Rotates the given block of the game board 90 degrees to the left
        '''

        rotated_grid = [ [self.grid[row][col] for col in range(self.size)] for row in range(self.size) ];

        row_offset = ((block - 1) / 2) * self.block_size;
        col_offset = ((block -1 ) % 2) * self.block_size;

        for i in range(row_offset, (row_offset + self.block_size)):
            for j in range(col_offset, (col_offset + self.block_size)):
                '''
                No idea how this works
                '''
                rotated_grid[2 - j + row_offset + col_offset][i - row_offset + col_offset] = self.grid[i][j];

        return rotated_grid;

    def rotate_right(self, block):
        '''
        Rotates the given block of the game board 90 degrees to the right
        '''

        rotated_grid = [ [self.grid[row][col] for col in range(self.size)] for row in range(self.size) ];

        row_offset = ((block - 1) / 2) * self.block_size;
        col_offset = ((block -1 ) % 2) * self.block_size;

        for i in range(row_offset, (row_offset + self.block_size)):
            for j in range(col_offset, (col_offset + self.block_size)):
                '''
                No idea how this works
                '''
                rotated_grid[j + row_offset - col_offset][2 - i + row_offset + col_offset] = self.grid[i][j];

        return rotated_grid;

    def __str__(self):

        border = "+-------+-------+\n";
        format = "| %s %s %s | %s %s %s |\n";
        output = "";

        for i in range(0, self.size):
            
            row = tuple([ str(x) for x in self.grid[i] ]);
            needs_border = ((i % self.block_size) == 0);
            
            if(needs_border):
                output += border;

            output += (format % row);

        output += border;

        return output;

    def __repr__(self):

        format = "%s %s %s %s %s %s\n";
        output = "";

        for i in range(0, self.size):

            row = tuple([ str(x) for x in self.grid[i] ]);
            output += (format % row);

        return output;

class Player(object):
    '''
    Players must be of a certain colour and may either
        1. Put a piece of their colour on the game board.
        2. Rotate a block of the game board.
    '''

    def __init__(self, name, colour, ai=None):

        self.name = name;
        self.colour = colour;
        self.ai = ai;

    def put(self, block, pos, board):
        '''
        Put player's piece at position [pos] in block [block] 
        of the game board.
        '''
        board.update(block, pos, self.colour);

    def twist(self, block, direction, board):
        '''
        Rotate block [block] of the game board 90 degress in 
        direction [direction]
        '''
        board.rotate(block, direction);

    def __str__(self):
        '''
        Returns the human-readable player value
        '''

        format = "%s (%s)";

        return format % (self.name, COLOUR().str(self.colour));

