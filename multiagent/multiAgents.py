# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        # newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if action == Directions.STOP:
            return -100
        
        for ghost in newGhostStates:
            if ghost.getPosition() == newPos:
                return -1000
        score = 0
        foods = currentGameState.getFood().asList()
        m = 99999
        for food in foods:
            man = manhattanDistance(food, newPos)
            if man < m:
                m = man 
        
        score -= m
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        
        return self.max_agent(0,0,gameState)[1]



    def min_agent(self, depth, agent_idx, gameState):
        if(depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState),None
        best_score = 99999999
        best_action = None

        for action in gameState.getLegalActions(agent_idx):
            next_gamestate = gameState.generateSuccessor(agent_idx, action)
            if agent_idx == gameState.getNumAgents()-1:
                max_Score = self.max_agent(depth+1,0, next_gamestate )[0]
            else:
                max_Score = self.min_agent(depth, agent_idx+1, next_gamestate)[0]

            if best_score > max_Score:
                best_score = max_Score
                best_action = action

        return best_score,best_action
        
    def max_agent(self, depth, agent_idx, gameState):
        if(depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState),None

        best_score = -99999999
        best_action = None
        for action in gameState.getLegalActions(agent_idx):
            next_gamestate = gameState.generateSuccessor(agent_idx, action)
            
            min_Score = self.min_agent(depth, agent_idx +1, next_gamestate)[0]

            if best_score < min_Score:
                best_score = min_Score
                best_action = action

        return best_score,best_action

        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.max_agent(0,0,gameState, -99999, 99999)[1]



    def min_agent(self, depth, agent_idx, gameState, alpha, beta):
        if(depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState),None
        best_score = 99999999
        best_action = None

        for action in gameState.getLegalActions(agent_idx):
            next_gamestate = gameState.generateSuccessor(agent_idx, action)
            if agent_idx == gameState.getNumAgents()-1:
                max_Score = self.max_agent(depth+1,0, next_gamestate, alpha, beta )[0]
            else:
                max_Score = self.min_agent(depth, agent_idx+1, next_gamestate, alpha, beta)[0]

            if best_score > max_Score:
                best_score = max_Score
                best_action = action
            
            beta = min(best_score, beta)
            if beta < alpha :
                break
            
            
        return best_score,best_action
    
    def max_agent(self, depth, agent_idx, gameState, alpha, beta):
        if(depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState),None

        best_score = -99999999
        best_action = None
        for action in gameState.getLegalActions(agent_idx):
            next_gamestate = gameState.generateSuccessor(agent_idx, action)
            
            min_Score = self.min_agent(depth, agent_idx +1, next_gamestate, alpha, beta)[0]

            if best_score < min_Score:
                best_score = min_Score
                best_action = action
            
            alpha = max(best_score, alpha)
            if alpha > beta :
                break
            
            
        return best_score,best_action

        


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        return self.max_agent(0,0,gameState, -99999, 99999)[1]



    def min_agent(self, depth, agent_idx, gameState, alpha, beta):
        if(depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState),None
        best_score = 99999999
        best_action = None

        suum = 0
        for action in gameState.getLegalActions(agent_idx):
            next_gamestate = gameState.generateSuccessor(agent_idx, action)
            if agent_idx == gameState.getNumAgents()-1:
                max_Score = self.max_agent(depth+1,0, next_gamestate, alpha, beta )[0]
            else:
                max_Score = self.min_agent(depth, agent_idx+1, next_gamestate, alpha, beta)[0]

            if best_score > max_Score:
                best_score = max_Score
                best_action = action
            
            suum += max_Score 

            
        return (suum/len(gameState.getLegalActions(agent_idx))),best_action
    
    def max_agent(self, depth, agent_idx, gameState, alpha, beta):
        if(depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState),None

        best_score = -99999999
        best_action = None
        for action in gameState.getLegalActions(agent_idx):
            next_gamestate = gameState.generateSuccessor(agent_idx, action)
            
            min_Score = self.min_agent(depth, agent_idx +1, next_gamestate, alpha, beta)[0]

            if best_score < min_Score:
                best_score = min_Score
                best_action = action

        return best_score,best_action


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what yo   u did>
    """
    "*** YOUR CODE HERE ***"
    PacmanPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    FoodCo = 1.8
    NumberOfFoodsCo = 16
    GhostCo = 1
    CapsuleCo = 7
    NumberOfcapsulesCo = 150
    
    score = 0
    minimumDistanceToGhosts = min([manhattanDistance(ghostState.getPosition(), PacmanPos) for ghostState in ghostStates])
    if minimumDistanceToGhosts <= 1:
        score -= 10000
    else:
        score += minimumDistanceToGhosts*GhostCo
    foodNumbers = len(foods)
    score -= foodNumbers * NumberOfFoodsCo
    minimumDistanceToFood = -1
    if(len(foods) > 0):
        minimumDistanceToFood = min([manhattanDistance(food, PacmanPos) for food in foods])
        score -= minimumDistanceToFood*FoodCo
    minimumDistanceToCapsule = -1
    if(len(capsules) > 0):
        minimumDistanceToCapsule =  min([manhattanDistance(capsule, PacmanPos) for capsule in capsules])
        score -= minimumDistanceToCapsule * CapsuleCo
    capsuleNumbers = len(capsules)
    score -= capsuleNumbers * NumberOfcapsulesCo
    # print("pacman position: ", PacmanPos)
    # print("ghost *",GhostCo,": ", minimumDistanceToGhosts*GhostCo, "   food numbers *",NumberOfFoodsCo,": " ,-1*foodNumbers * NumberOfFoodsCo, "   nearest food *",FoodCo,": " ,-1*minimumDistanceToFood*FoodCo, "   capsule *",CapsuleCo,": " ,-1*minimumDistanceToCapsule*CapsuleCo, "   number of capsules *",NumberOfcapsulesCo,": " ,-1*capsuleNumbers*NumberOfcapsulesCo, "     score: " ,score)

    return score

# Abbreviation
better = betterEvaluationFunction

