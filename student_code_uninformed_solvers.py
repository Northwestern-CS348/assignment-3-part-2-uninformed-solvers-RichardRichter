from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
       
        if self.currentState.state == self.victoryCondition:
            return True
        self.visited[self.currentState] = True
        #print(self.currentState.state)
        #print(self.gm.getMovables())
        if self.gm.getMovables() != False:
            #visit_spaces = True
            moves = self.gm.getMovables()
            #print(moves)
            for move in moves:
                self.gm.makeMove(move)
                self.currentState.children.append(GameState(self.gm.getGameState(), self.currentState.depth+1, move))
                self.currentState.children[len(self.currentState.children)-1].parent = self.currentState
                self.gm.reverseMove(move)
            for c in self.currentState.children:
                if not self.visited.get(c, False):
                    move = c.requiredMovable
                    self.gm.makeMove(move)
                    self.currentState = c
                    return False      
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False
        # print("this is the post game state")
        # print(self.currentState.state)
        # if self.gm.getGameState() == self.victoryCondition:
        #     return True
        # return False

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    queue = []
    index = 0
    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        #okay so when tower is called, it doesnt work, and because of that the queue and index never get a chance to get cleared
        #so if you only ran puzzle8 it would work, but where it stands now it looks like they all dont work
        if self.currentState.state == self.victoryCondition:
            self.index = 0
            self.queue.clear()
            return True
        