'''Making a online multiplayer game in python'''
class Game:
    def __init__(self, id):
        self.p1went = False  # This is going to be seeing whether p1 or p2 has made a move or not
        self.p2went = False
        self.ready = False  # This will see if the players are ready or not
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]  # Count the number of wins
        self.ties = 0  # Count the number of ties

    def get_player_move(self, p):  # This will tell us which move either players has made
        return self.moves[p]

    def play(self, player, move):

        self.moves[player] = move  # If the player makes a move pwnet will be set to True
        if player == 0:
            self.p1went = True
        else:
            self.p2went = True

    def connected(self):  # This will return whether both players are ready or not
        return self.ready

    def bothWent(self):  # This will return us whether both players have made a move or not
        return self.p1went and self.p2went

    def winner(self):

        p1 = self.moves[0].upper()[0]  # This will give the first letter of the move that is R, P or S
        p2 = self.moves[1].upper()[0]

        winner = -1  # winner will be -1 if there is a tie

        if p1 == "R" and p2 == "S":  # All the possible combinations for winning
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):  # Reset the game
        self.p1went = False
        self.p2went = False
