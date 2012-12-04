'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Pentago Input/Output i.e For Loading and Saving Games
'''

from pentago import *;
from pentago.assets import *;
from pentago.ai import Move;

class Loader(object):
    '''
    Responsible for loading a pentago game from a log file.
    '''

    def __init__(self):
        self.players = [];
        self.board = None;
        self.moves = [];
        self.turn = 0;

    def load(self, filepath):
        names = [];
        colours = [];

        file = open(filepath, 'r');

        for line in file:
            line = line.strip();

            if len(line) == 1:
                try:
                    colours.append( COLOUR().cast(line) );
                except ValueError:
                    self.turn = int(line);
                except TypeError:
                    pass;
                
            elif '.' in line:
                pass;

            else:
                try:
                    move = Move(1,1,1,'J'); # Must be an invalid move
                    self.moves.append( move.parse(line) );
                except:
                    names.append(line);

        assert( len(names) == len(colours) );

        for i in range( len(names) ):
            self.players.append( Player(names[i], colours[i]) );

        self.board = Board();

        # Advance board to current state
        for i, move in enumerate(self.moves):
            turn = i % len(self.players);
            print self.board;

            self.players[turn].put(move.block, move.cell, self.board);
            self.players[turn].twist(move.twist, move.direction, self.board);

        return self;
