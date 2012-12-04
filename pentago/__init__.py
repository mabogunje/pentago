'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Defines common pentago classes
'''


WIN_CONDITION = 5; # 5 duplicates in a row, column, or diagonal will win the game
LOG_FILE = 'pentago.sav';


class DIRECTION(object):
    '''
    Represents the possible directions a board block may be rotated
    '''

    (LEFT, RIGHT) = range(0, 2);

    def validate(self, direction):
        '''
        Return false if direction is invalid, true otherwise
        '''

        assert( isinstance(direction, int) );

        if (direction < DIRECTION.LEFT) or (direction > DIRECTION.RIGHT):
            return False;

        return True;

    def cast(self, val):
        '''
        Casts a char to a DIRECTION
        '''
        assert( isinstance(val, str) );

        if val == self.str(DIRECTION.LEFT):
            return DIRECTION.LEFT;
        elif val == self.str(DIRECTION.RIGHT):
            return DIRECTION.RIGHT;
        else:
            raise ValueError;


    def str(self, direction):
        '''
        Returns the human-readable direction
        '''

        direction_map = { DIRECTION.LEFT: "L",
                          DIRECTION.RIGHT: "R"
                        };

        return direction_map.get(direction);


class COLOUR(object):
    '''
    Represents the piece colours available for players
    '''

    (WHITE, BLACK) = range(0, 2);

    def validate(self, colour):
        '''
        Return false if colour is invalid, true otherwise
        '''

        if (colour < COLOUR.WHITE) or (colour > COLOUR.BLACK):
            return False;

        return True;
    
    def cast(self, val):
        '''
        Casts a char to a COLOUR
        '''
        assert( isinstance(val, str) );

        if val == self.str(COLOUR.WHITE):
            return COLOUR.WHITE;
        elif val == self.str(COLOUR.BLACK):
            return COLOUR.BLACK;
        else:
            raise ValueError;

    def str(self, colour):
        '''
        Returns the human-readable colour
        '''

        colour_map = { COLOUR.WHITE: 'W',
                       COLOUR.BLACK: 'B'
                     };

        return colour_map.get(colour);

class GAME_STATE(object):
    '''
    Represents the state of the game board
    '''

    (IN_PLAY, WIN, TIE) = range(0, 3);

    def str(self, state):
        '''
        Returns the human-readable game_state
        '''

        state_map = { GAME_STATE.IN_PLAY: "PLAYING",
                      GAME_STATE.WIN: "WIN",
                      GAME_STATE.TIE: "TIE"
                    };

        return state_map.get(state);

