import random
import time
import copy
import math
import asyncio

class ttEntry:
    def __init__(self, flag, depth, actions, value):
        self.flag = flag
        self.depth = depth
        self.actions = actions
        self.value = value


class Transposition_table:
    def __init__(self):
        # table with random 32 bits for zobrist hashing
        self.table = [[[random.getrandbits(32) for _ in range(2)] for _ in range(8)] for _ in range(8)]
        self.data = dict()


    def ZobristHash(self, board):
        h = 0
        for r in range(8):
            for c in range(8):
                if board[r, c] != 0:
                    h ^= self.table[r][c][board[r, c] - 1]

        return h


    def lookup(self, hash_value):
        if hash_value in self.data:
            return self.data[hash_value]
        else:
            return None

    def add_entry(self, hash_value, entry):
        if hash_value in self.data:
            del self.data[hash_value]

        self.data[hash_value] = entry


corners = [(0, 0), (0, 1), (1, 0), (1, 1),
            (0, 7), (0, 6), (1, 7), (1, 6),
            (6, 6), (6, 7), (7, 6), (7, 7),
            (7, 0), (6, 0), (6, 1), (7, 1)]


class AI:
    def __init__(self):
        self.color = 2
        # victory value
        self.victory_value = [0, 1, 2, 4, 16, 256]

        # value distribution
        self.value = [
            [10,-5, 3, 2, 2, 3,-5, 10],
            [-5,-7, 0, 0, 0, 0,-7, -5],
            [ 3, 0, 1, 0, 0, 1, 0,  3],
            [ 2, 0, 0, 1, 1, 0, 0,  2],
            [ 2, 0, 0, 1, 1, 0, 0,  2],
            [ 3, 0, 1, 0, 0, 1, 0,  3],
            [-5,-7, 0, 0, 0, 0,-7, -5],
            [10,-5, 3, 2, 2, 3,-5, 10],
        ]

        # transposition table
        self.tt_table = Transposition_table()


    def clear(self):
        del self.tt_table
        self.tt_table = Transposition_table()
        self.color = 2


    def set_player(self, color):
        self.color = color


    def move_ordering(self, board, best_actions, current_player):
        actions = best_actions

        for r in range(8):
            for c in range(8):
                if board.is_placeable((r, c), current_player) and (r, c) not in best_actions:
                    actions.append((r, c))

        return actions


    def result(self, board, action, player):
        new_board = copy.deepcopy(board)
        new_board.place(action, player)
        return new_board


    def terminate(self, board, player):
        if not board.is_playable(player):
            return True

        victory_cells = board.get_victory_cells()

        v = [0] * 3

        for cell in victory_cells:
            v[board.get_value(cell)] += 1

        if v[1] == 5 or v[2] == 5:
            return True

        return False


    def evaluate(self, board, current_player, is_terminate=False):
        victory_cells = board.get_victory_cells()
        current_opponent = 1 if current_player == 2 else 2

        v = [0] * 3
        n = [0] * 3

        # count number of occupied victory cells
        for cell in victory_cells:
            v[board.get_value(cell)] += 1

        score = [0, self.victory_value[v[1]], self.victory_value[v[2]]]

        # count number of occupied cells of each color and empty cells
        for r in range(8):
            for c in range(8):
                n[board.get_value((r, c))] += 1

        total = n[1] + n[2]

        # begin - mid - end game strategy
        if total < 55:
            # mobility
            score[1] += 1.5 * len(board.available_actions(1))
            score[2] += 1.5 * len(board.available_actions(2))

            # evaporation strategy
            score[1] -= n[1]
            score[2] -= n[2]

            # adding value of each occupied cell
            for r in range(8):
                for c in range(8):
                    score[board.get_value((r, c))] += self.value[r][c]
        else:
            score[1] += n[1] ** 2
            score[2] += n[2] ** 2

        # check if oppenent can control the horizontal borders
        for (r, c) in [(0, 1), (0, 6), (7, 1), (7, 6)]:
            if board.get_value((r, c - 1)) != 0 and board.get_value((r, c + 1)) == board.get_value((r, c - 1)):
                if board.get_value((r, c)) == 0:
                    score[board.get_value((r, c - 1))] -= 7
                else:
                    score[board.get_value((r, c))] += 16

        # check if oppenent can control the vertical borders
        for (r, c) in [(1, 0), (6, 0), (1, 7), (6, 7)]:
            if board.get_value((r - 1, c)) != 0 and board.get_value((r + 1, c)) == board.get_value((r - 1, c)):
                if board.get_value((r, c)) == 0:
                    score[board.get_value((r - 1, c))] -= 7
                else:
                    score[board.get_value((r, c))] += 16

        # winning score
        if is_terminate:
            # adding number of empty cells ^ 2 to the result
            if v[1] == 5:
                score[1] += n[0] ** 2 + 512
            elif v[2] == 5:
                score[2] += n[0] ** 2 + 512
            elif n[1] == n[2]:
                if v[current_player] > v[current_opponent]:
                    score[current_player] += n[0] ** 2
                elif v[current_opponent] > v[current_player]:
                    score[current_opponent] += n[0] ** 2
                else:
                    return 0
            elif n[current_player] > n[current_opponent]:
                score[current_player] += n[0] ** 2
            else:
                score[current_opponent] += n[0] ** 2

        return score[current_player] - score[current_opponent]


    def quiescence_search(self, board, alpha, beta, current_player):
        stand_pat = self.evaluate(board, current_player)
        if stand_pat >= beta:
            return beta

        if stand_pat > alpha:
            alpha = stand_pat

        next_player = 1 if current_player == 2 else 2

        for action in corners:
            if board.is_placeable(action, current_player):
                val = -self.quiescence_search(self.result(board, action, current_player), -beta, -alpha, next_player)

                if val >= beta:
                    return beta
                if val > alpha:
                    alpha = val

        return alpha


    def negascout(self, board, alpha, beta, depth, current_player):
        a = alpha

        # look up the entry
        h = self.tt_table.ZobristHash(board.data)
        entry = self.tt_table.lookup(h)

        # compare the search depth with the previous search depth
        if entry and entry.depth >= depth:
            # if exact return the value
            if entry.flag == 0:
                return entry.value
            elif entry.flag == -1: # if lowerbound, update alpha
                if entry.value > alpha:
                    alpha = entry.value
            elif entry.flag == 1: # if upperbound, update beta
                if entry.value < beta:
                    beta = entry.value

            if alpha >= beta:
                return entry.value

        if self.terminate(board, current_player):
            return self.evaluate(board, current_player, is_terminate=True)
        elif depth == 0:
            return self.quiescence_search(board, alpha, beta, current_player)

        best = -math.inf
        next_player = 1 if current_player == 2 else 2

        if entry:
            actions = self.move_ordering(board, entry.actions, current_player)
        else:
            actions = board.available_actions(current_player)

        first = True
        best_actions = list()

        for action in actions:
            new_board = self.result(board, action, current_player)
            if first:
                val = -self.negascout(new_board, -beta, -alpha, depth - 1, next_player)
                first = False
            else:
                # search with a NULL window
                val = -self.negascout(new_board, -alpha - 1, -alpha, depth - 1, next_player)
                if alpha < val and val < beta:
                    # re-search
                    val = -self.negascout(self.result(board, action, current_player), -beta, -val, depth - 1, next_player)

            if val > best:
                best_actions.append(action)
                best = val

                if val > alpha:
                    alpha = val

            if alpha >= beta:
                break

        if best <= a:
            flag = 1    # Upperbound
        elif best >= beta:
            flag = -1   # Lowerbound
        else:
            flag = 0    # Exact

        # list all best actions
        best_actions.reverse()

        # store to transposition table
        self.tt_table.add_entry(h, ttEntry(flag, depth, best_actions, best))

        return best


    def make_decision(self, board, hash_value, depth, opponent):
        alpha = -math.inf
        beta = math.inf

        # look up the entry
        entry = self.tt_table.lookup(hash_value)

        # compare the search depth with the previous search depth
        if entry and entry.depth >= depth:
            # if exact return the best action
            if entry.flag == 0:
                return entry.actions[0]
            elif entry.flag == -1: # if lowerbound then update alpha
                if entry.value > alpha:
                    alpha = entry.value
            elif entry.flag == 1: # if upperbound then update beta
                if entry.value < beta:
                    beta = entry.value

        if entry:
            actions = self.move_ordering(board, entry.actions, self.color)
        else:
            actions = board.available_actions(self.color)

        first = True
        best = -math.inf
        best_actions = list()

        for action in actions:
            new_board = self.result(board, action, self.color)
            if first:
                val = -self.negascout(new_board, -beta, -alpha, depth - 1, opponent)
                first = False
            else:
                # search with a NULL window
                val = -self.negascout(new_board, -alpha - 1, -alpha, depth - 1, opponent)
                if alpha < val and val < beta:
                    # re-search
                    val = -self.negascout(self.result(board, action, self.color), -beta, -val, depth - 1, opponent)

            if val > best:
                best_actions.append(action)
                best = val

                if val > alpha:
                    alpha = val

        # list all best actions
        best_actions.reverse()

        # store to transposition table
        self.tt_table.add_entry(hash_value, ttEntry(0, depth, best_actions, best))

        return best_actions[0]


    def iterative_deepening(self, board):
        opponent = 1 if self.color == 2 else 2
        depth = 1
        execution_time = 0
        start_time = time.time()

        hash_value = self.tt_table.ZobristHash(board.get_data())

        while execution_time < 3 and depth < 10:
            best_action = self.make_decision(board, hash_value, depth, opponent)
            execution_time = time.time() - start_time
            depth += 1

        return best_action


    async def play(self, board):
        if board.is_playable(self.color):
            return board.make_action(self.iterative_deepening(board))
