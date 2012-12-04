'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Implementation of the Pentago game as described at: 
          http://www.pentago.com/pdfs/30_sec_quick%20guide.pdf
'''

import traceback;
import sys;
import os;
import argparse;

from pentago import *;
from pentago.assets import *;
from pentago.ai import *;
from pentago.io import *;

def run(saved_game=None):

    preloaded = Loader().load(saved_game) if saved_game else None;
    
    game_log = [];
    player_names = ["PLAYER 1", "PLAYER 2"];
    player_types = [COLOUR.WHITE, COLOUR.BLACK];

    help = '''
           HOW TO PLAY
           -----------
           Pentago is a 2-player game played on a 6x6 grid. The players alternate turns. 
           The players are referred to as "W" and "B" which also identifies their marbles. 
           Each turn consists of placing one marble, anywhere on the board and twisting 
           any of the game blocks 90 degrees,in either direction. 
           
           You can place your marble on one game block and twist any other game block.
           The object is to get five marbles in a row in any direction, before your opponent.

           PLAYING YOUR TURN
           -----------------
           To play your turn enter a block and cell for your marble as well as a block to rotate
           Example: 3/8 2L
           This command places your marble in block 3 cell 8, and rotates block 2 90degrees left

           ENJOY!

           '''

    prompt = '''Before we start the game please choose a colour for PLAYER 1:
    [%d] %s
    [%d] %s
    ''';

    prompt_values = [ player_types[0], COLOUR().str(player_types[0]), 
                      player_types[1], COLOUR().str(player_types[1])
                    ];
    choice = -1;
    
    if not preloaded:
        print help;
        while (not COLOUR().validate(choice)):
            try:
                choice = int( raw_input( (prompt % tuple(prompt_values)) ) );
            except:
                print "Invalid choice";

    players = preloaded.players if preloaded else [ Player(player_names.pop(0), player_types.pop(player_types.index(choice))),
                                                    Player(player_names.pop(0), player_types.pop()),
                                                  ];

    board = preloaded.board if preloaded else Board();

    # Save player data at beginning of logfile
    for p in players:
        game_log.append(p.name + "\n");

    for p in players:
        game_log.append(COLOUR().str(p.colour) + "\n");

    move_prompt = "%s's turn: ";

    game_over = { GAME_STATE.WIN: "GAME OVER: %(player)s's %(result)s",
                  GAME_STATE.TIE: "GAME OVER: %(player)s. It is a %(result)s"
                };

    game_log.append(None); # Placeholder for Player to move next
    game_log.append(None); # Placeholder for Board state

    if preloaded: # Reorder players by turn
        first = players[preloaded.turn-1:];
        last = players[:preloaded.turn-1];
        players = [];

        players.extend(first);
        players.extend(last);

    while board.state == GAME_STATE.IN_PLAY:
        
        for turn, player in enumerate(players):
            print board;
            move = Move(1,1,1,'J'); # Must be an invalid move 

            while not is_valid_move(move, board):
                input = raw_input(  (move_prompt % player) );
                    
                try:
                    move = move.parse(input);
                except:
                    print "Unrecognized move!";
                    break;

            print move;
                    
            try:
                player.put(move.block, move.cell, board);
                evaluate_state(board);
                assert(board.state == GAME_STATE.IN_PLAY);

                player.twist(move.twist, move.direction, board);
                evaluate_state(board);
                assert(board.state == GAME_STATE.IN_PLAY);
            except:
                results = {"player": player, "result": GAME_STATE().str(board.state)};
                print game_over[board.state] % results;
                        
                sys.exit();
            else:
                next_turn = (preloaded.turn - turn + 1) if preloaded else (len(players) - turn);
                game_log[4] = str(next_turn) + "\n";
                game_log[5] = repr(board);

                if preloaded:
                    if not set(preloaded.moves).issubset(set(game_log)): # Update game log with moves from save file
                        game_log.extend(map(lambda m: repr(m) + "\n", preloaded.moves));

                game_log.append(repr(move) + "\n");
                        
                LOG = open(LOG_FILE, 'w');
                LOG.writelines(game_log);


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Play Pentago!');
    parser.add_argument('-f', '--file', nargs='?', help='Saved Game File');

    args = parser.parse_args();

    if args.file:
        run(args.file);
    else:
        run();

