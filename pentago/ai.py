'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Defines pentago game logic
'''

from pentago import *;
from pentago.assets import BLOCK, Board;

class Move(object):
    '''
    Represents a player's move
    '''

    SEP = {'TWIST': " ", 'BLOCK': "/"};

    def __init__(self, block, cell, twistblock, direction):
        
        self.block = block;
        self.cell = cell;
        self.twist = twistblock;
        self.direction = direction;

    def parse(self, value):
        
        #print value;
        assert( isinstance(value, str) );

        move = value.split(Move.SEP['TWIST']);
        rotation_vals = move.pop();
        position_vals = [ int(x) for x in move[0].split(Move.SEP['BLOCK']) ];

        block = position_vals[0];
        cell = position_vals[1];
        twist = int(rotation_vals[0]);
        direction = DIRECTION().cast( rotation_vals[-1].upper() );

        assert( BLOCK().validate(block) );
        assert( BLOCK().validate(twist) );
        assert( DIRECTION().validate(direction) );
        assert( cell in range(10));

        self.block = position_vals[0];
        self.cell = position_vals[1];
        self.twist = int(rotation_vals[0]);
        self.direction = DIRECTION().cast(rotation_vals[-1].upper());

        return self;

    def __str__(self):

        format = "Place piece in block %d, cell %d.\nTwist block %d %s";
        direction = "right" if self.direction is DIRECTION.RIGHT else "left";

        return format % (self.block, self.cell, self.twist, direction);
    
    def __repr__(self):

        format = "%d/%d %d%c";

        return format % (self.block, self.cell, self.twist, DIRECTION().str(self.direction));




def is_valid_move(move, board):
    '''
    Determines if a move is valid
    '''

    assert( isinstance(move, Move) );

    return (move.block != move.twist) and  board.is_empty(move.block, move.cell); 


def evaluate_state(board):
    '''
    Analyzes the game board to determine win/loss/tie
    Side-Effect: Sets the board.state to a new GAME_STATE 
    '''

    for i in range(board.size - WIN_CONDITION + 1): # The + 1 accounts for range() not including the last value in a range
        for j in range(board.size - WIN_CONDITION + 1):
            
            val = board.grid[i][j];
            win_count = {COLOUR().str(COLOUR.WHITE): 0, COLOUR().str(COLOUR.BLACK): 0};

            # Current column subset is the current cell for 5 rows from the current row
            col_checklist = [ board.grid[row][j] for row in range(i, i + WIN_CONDITION) ]; 

            # Current row subset is the current cell + 5 cells after it
            row_checklist = board.grid[i][j:j + WIN_CONDITION];

            if i == j:
                # Current diagonal subset is the current cell + 5 cells diagonally following it
                diag_checklist = [ [board.grid[x][y] for y in range(i, i + WIN_CONDITION) ] for x in range(j, j + WIN_CONDITION) ];
                #print diag_checklist;

                # Player wins if 5 sequential elements in a diagonal are the same
                if all( [(x == val) for x in diag_checklist] ) and any( [(x != Board.EMPTY_CELL) for x in diag_checklist] ):
                    win_count[val] += 1;
                    board.state = GAME_STATE.WIN;


            # Player wins if 5 sequential elements in a row are the same
            if all( [(x == val) for x in row_checklist] ) and any( [(x != Board.EMPTY_CELL) for x in row_checklist] ):
                win_count[val] += 1;
                board.state = GAME_STATE.WIN;

            # Player wins if 5 sequential elements in a column are the same
            if all( [(x == val) for x in col_checklist] ) and any( [(x != Board.EMPTY_CELL) for x in col_checklist] ):
                win_count[val] += 1;
                board.state == GAME_STATE.WIN;

            # It's a tie if both players have acheived a win
            if all( [(x > 0) for x in win_count.values()] ):
                board_state = GAME_STATE.TIE;

            return board.state;

