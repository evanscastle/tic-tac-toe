# Authored by Evan Castle on 4/17/20
# The implementation of this project was inspired by the instructions on
# https://towardsdatascience.com/reinforcement-learning-implement-tictactoe-189582bea542

from player import Player
from board import Board
from progress_bar import update_progress


def train(p1, p2, NUMBER_OF_EPISODES):

    print('\n\nTraining ' + str(NUMBER_OF_EPISODES) + ' Episodes')

    for i in range(NUMBER_OF_EPISODES):
        if (i + 1) % 50 == 0:
            update_progress((i + 1) / NUMBER_OF_EPISODES)

        board = Board(p1, p2)
        board.determine_starting_player()

        while not board.isFinished():
            if (board.turns_taken + board.coin_flip) % 2 == 0:
                action = p1.chooseMove(board)
            else:
                action = p2.chooseMove(board)

            board.makeMove(action)
        # board.print()

        # print winner of episode
        # print(board.winner)

        # update state function following episode
        if board.winner == 'p1':
            p1.updateValues('win')
            p2.updateValues('loss')

        elif board.winner == 'p2':
            p1.updateValues('loss')
            p2.updateValues('win')

        else:
            p1.updateValues('tie')
            p2.updateValues('tie')

    p1.saveStates()
    p2.saveStates()

def simulate_gameplay(p1, p2, NUMBER_OF_EPISODES):

    play_record = [0, 0, 0]
    print('\n\nSimulating ' + str(NUMBER_OF_EPISODES) + ' Episodes')

    for i in range(NUMBER_OF_EPISODES):
        if (i + 1) % 50 == 0:
            update_progress((i + 1) / NUMBER_OF_EPISODES)

        board = Board(p1, p2)
        board.determine_starting_player()

        while not board.isFinished():
            if (board.turns_taken + board.coin_flip) % 2 == 0:
                action = p1.chooseMove(board)
            else:
                action = p2.chooseMove(board)

            board.makeMove(action)

        if board.winner == 'p1':
            play_record[0] += 1
        elif board.winner == 'p2':
            play_record[1] += 1
        else:
            play_record[2] += 1

    agent_rating = (play_record[0] + 0.5 * play_record[2]) / NUMBER_OF_EPISODES
    formatted_agent_rating = f"{agent_rating:.4f}"
    print('Record: ' + str(play_record))
    print('Agent Rating: ' + formatted_agent_rating)



if __name__ == '__main__':
    NUMBER_OF_EPISODES = 1000

    p1 = Player('001', NUMBER_OF_EPISODES)
    p2 = Player('002', NUMBER_OF_EPISODES)

    train(p1, p2, NUMBER_OF_EPISODES)

    #p1.loadStates('agents/policy_001.pkl')

    # p1 = Player()
    p2 = Player()

    simulate_gameplay(p1, p2, NUMBER_OF_EPISODES)


