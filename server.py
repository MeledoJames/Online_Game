'''Making a server for a online multiplayer game in python'''
import socket
from _thread import *
import pickle
from game import Game

# Server address and port

server = "192.168.0.117"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Setting the ipv4 and tcp addresses

try:
    s.bind((server, port))  # Binding the socket to the server address
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server started")

connected = set()
games = {}  # Dictionary of the number of games
idCount = 0

def threaded_client(conn, p, gameID):  # We are going to make a threaded client
    global idCount
    conn.send(str.encode(str(p)))  # This is going to tell us which player we are

    reply = ""

    while True:

        try:
            data = conn.recv(4096).decode()  # Receive string data

            if gameID in games:  # Checking if the game still exists
                game = games[gameID]

                if not data:  # Checking if the game is ready or not
                    break
                else:

                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)  # If it is a move, sending the move to the client

                    conn.sendall(pickle.dumps(game))  # Constantly going to update the game

            else:
                break
        except:
            break

    print("Lost connection")

    try:
        del games[gameID]  # When a player disconnects it's going to delete the game
        print("Closing game", gameID)

    except:
        pass

    idCount -= 1
    conn.close()  # After deleting the game it's going to close the connection

while True:

    conn, addr = s.accept()  # Accepting the connection to the client
    print("Connected to ", addr)

    idCount += 1  # After connection, idcount will increase
    p = 0  # Player = 0
    gameID = (idCount - 1) // 2  # A game, will contain 2 players

    if idCount % 2 == 1:
        games[gameID] = Game(gameID)  # The key in the dictionary is a now a new game and now we can add players to it
        print("Creating a new game...")

    else:
        games[gameID].ready = True  # When both the players have joined the server is ready to start a new game
        p = 1  # Player = 1

    start_new_thread(threaded_client, (conn, p, gameID))  # Starting a new thread
