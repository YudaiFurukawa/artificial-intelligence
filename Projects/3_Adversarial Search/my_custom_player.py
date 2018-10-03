
from sample_players import DataPlayer
from isolation import DebugState
import random

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        alpha = float("-inf")
        beta = float("inf")

        def minitax(state, depth_remaining, depth_count, heuristic_type):
            def custom_heuristic(state):
                own_moves = len(state.liberties(state.locs[self.player_id]))
                opp_moves = len(state.liberties(state.locs[self.player_id - 1]))

                if own_moves < 5:
                    return (2 * own_moves) - (opp_moves)
                else:
                    return (own_moves) - (2 * opp_moves)
            def baseline_heuristic(state):
                return len(state.liberties(state.locs[self.player_id])) - len(state.liberties(state.locs[self.player_id-1]))
            def minimum(state, alpha, beta, depth_remaining, depth_count):
                if state.terminal_test():
                    return state.utility(self.player_id)
                if depth_remaining <= 0:
                    if heuristic_type == 'custom':
                        return custom_heuristic(state)
                    if heuristic_type == 'baseline':
                        # print(baseline_heuristic(state))
                        return baseline_heuristic(state)
                value = float("inf")
                for action in state.actions():
                    value = min(value, maximum(state.result(action),alpha, beta, depth_remaining - 1, depth_count + 1))
                    if value <=alpha: return value
                    beta = min(beta, value)
                return value

            def maximum(state, alpha, beta, depth_remaining, depth_count):
                # print(depth_remaining)
                if state.terminal_test():
                    return state.utility(self.player_id)
                if depth_remaining <= 0:
                    if heuristic_type == 'custom':
                        return custom_heuristic(state)
                    if heuristic_type == 'baseline':
                        return baseline_heuristic(state)
                value = float("-inf")
                for action in state.actions():
                    value = max(value, minimum(state.result(action),alpha, beta, depth_remaining - 1, depth_count + 1))
                    if value >=beta: return value
                    alpha = max(beta, value)
                return value

            return max(state.actions(), key = lambda x:minimum(state.result(x),alpha,beta,depth_remaining -1, depth_count + 1))

        def greedy_play(state):
            return max(state.actions(), key = lambda x:len(state.result(x).liberties(state.locs[self.player_id])))

        if state.ply_count <= 2:
            self.queue.put(greedy_play(state))
        else:
            self.queue.put(minitax(state,depth_remaining=7, depth_count=0,heuristic_type='custom'))




