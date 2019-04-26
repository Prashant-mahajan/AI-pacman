def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    next_pacman_position = currentGameState.getPacmanPosition()
    next_food = [food for food in currentGameState.getFood().asList() if food]
    next_ghosts_states = currentGameState.getGhostStates()
    next_ghosts_scared_timers = [ghostState.scaredTimer for ghostState in next_ghosts_states]
    "*** YOUR CODE HERE ***"
    # Calculations
    ghost_distance = min(
        self.manhattanDistance(next_pacman_position, ghost.configuration.pos) for ghost in next_ghosts_states)
    closest_food_distance = min(
        self.manhattanDistance(next_pacman_position, nextFood) for nextFood in next_food) if next_food else 0
    scared_time = min(next_ghosts_scared_timers)

    # It is bad to have remaining pellets, very bad!
    remaining_food_feature = -len(next_food)
    # It is bad to be close to ghosts, but if they are harmless, is not so bad (better not to eat them)
    ghost_distance_feature = -2 / (ghost_distance + 1) if scared_time == 0 else 0.5 / (ghost_distance + 1)
    # It is bad to be far from food
    closest_food_feature = 0.4 / (closest_food_distance + 1)
    # Power pellets are good, but not that good
    power_pellets_feature = scared_time * 0.5
    game_score = currentGameState.getScore() * 0.6

    return remaining_food_feature + ghost_distance_feature + closest_food_feature + power_pellets_feature + game_score

