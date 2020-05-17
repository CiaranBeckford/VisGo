class Agent():
    """Interface for a go-playing bot."""
    def select_move(self, game_state):
        raise NotImplementedError()
