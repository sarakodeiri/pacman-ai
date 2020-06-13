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
import math

from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent
from ghostAgents import GHOST_AGENT_MAX_DEPTH, GhostAgent


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class AdversarialSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxAgent, SmartPacmanAgent, SmartGhostAgent

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # index should be 0 by default
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getOpponentIndex(self):
        return 1 - self.index


class MinimaxAgent(AdversarialSearchAgent):

    def getAction(self, gameState):
        """
        The Agent will receive a GameState and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        minimaxScores = []
        legalActions = gameState.getLegalActions(self.index)
        for action in legalActions:
            score = self.minimax(
                gameState.generateSuccessor(self.index, action),
                self.getOpponentIndex(),
                0
            )
            minimaxScores.append((score, action))

        bestAction = max(minimaxScores)[1]

        return bestAction

    def minimax(self, gameState, maximizingAgent, currentDepth):
        """
        Returns the minimax score for the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        self.index:
            Return your agent's index
        self.getOpponentIndex():
            Return your opponent's index
        gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
        gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

        Args:
            gameState: an instance of pacman.GameState, minimax algorithm should be started on this state
            maximizingAgent: index of agent we're maximizing score for, you can check this paramterer against self.index 
            currentDepth: current depth in minmax tree

        Returns:
            Return minimax score
        """
        if currentDepth == self.depth:
            return self.evaluationFunction(gameState)
        if maximizingAgent == self.index:
            return self.maxvalue(gameState, maximizingAgent, currentDepth)
        else:
            return self.minvalue(gameState, maximizingAgent, currentDepth)

    def maxvalue(self, gameState, maximizingAgent, currentDepth):

        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        if currentDepth == self.depth or self.depth == 0:
            return self.evaluationFunction(gameState)

        v = -float("inf")
        if self.index == maximizingAgent:
            nextAgent = self.getOpponentIndex()
        else:
            nextAgent = self.index
        for moves in gameState.getLegalActions(maximizingAgent):
            v = max(v, self.minimax(gameState.generateSuccessor(maximizingAgent, moves), nextAgent,
                                  currentDepth + 1))
        return v

    def minvalue(self, gameState, maximizingAgent, currentDepth):

        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        if currentDepth == self.depth or self.depth == 0:
            return self.evaluationFunction(gameState)

        v = float("inf")
        if self.index == maximizingAgent:
            nextAgent = self.getOpponentIndex()
        else:
            nextAgent = self.index
        for moves in gameState.getLegalActions(maximizingAgent):
            v = min(v, self.minimax(gameState.generateSuccessor(maximizingAgent, moves), nextAgent,
                                  currentDepth + 1))
        return v


class SmartPacmanAgent(MinimaxAgent):
    def __init__(self, depth='2'):
        self.index = 0
        self.depth = int(depth)

    @staticmethod
    def evaluationFunction(gameState):
        """
        Returns evaluation score for each gameState

        Args:
            gameState: an instance of pacman.GameState
        
        Returns:
            Return the evaluation score
        """
        pacPos = gameState.getPacmanPosition()
        ghostPos = gameState.getGhostPosition(1)
        boxPos = [(8, 5), (9, 5), (10, 5), (11, 5)]

        if gameState.isLose() or boxPos.__contains__(pacPos):
            return -float("inf")
        if gameState.isWin():
            return float("inf")

        foods = gameState.getFood().asList()
        food_dist = float("inf")
        for food in foods:
            food_dist = min(food_dist, util.manhattanDistance(food, pacPos))

        ghost_dist = util.manhattanDistance(pacPos, ghostPos)
        food_count = gameState.getNumFood()
        capsule_count = len(gameState.getCapsules())

        ghost_state = gameState.getGhostState(1)

        # if food_count == 1 and ghost_dist > 4:
        #     return float("inf")
        #
        # temp = [(5, 5), (6, 4)]
        # if temp.__contains__(pacPos) and foods.__contains__((6, 5)) and ghostPos != (6, 5):
        #     return float("inf")
        if ghost_state.scaredTimer:
            return 2 * gameState.getScore() - 20 * food_count - 100 * capsule_count - 5 * ghost_dist - 2 * food_dist

        return 2 * gameState.getScore() - 20 * food_count - 100 * capsule_count + ghost_dist - 2 * food_dist


class SmartGhostAgent(MinimaxAgent):
    def __init__(self, index):
        self.index = 1
        self.depth = GHOST_AGENT_MAX_DEPTH

    @staticmethod
    def evaluationFunction(gameState):
        """
        Similar to SmartPacmanAgent
        """
        util.raiseNotDefined()


class SuperGhostAgent(GhostAgent):
    def __init__(self, index):
        self.index = index
        self.depth = GHOST_AGENT_MAX_DEPTH

    def getAction(self, gameState):
        """
        The Agent will receive a GameState and
        must return an action from Directions.{North, South, East, West}
        """
        util.raiseNotDefined()
