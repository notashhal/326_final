import random
import os
import re
from scipy import stats
import sqlite3
import requests

def intro():
    """
    Prints an introduction to the game called Victory Road. Gives a general overview of what the traveler (player) should expect.

    The function requests from the "https://randomuser.me/api/" API to recieve a random user's data,
    which in this case is their first name. The name is then used to emulate someone actually telling you this intro. It is a 
    different person every time you start a new game.

    Introduction Information:
    - Welcomes the player to the game called Victory Road.
    - Introduces the speaker with their first name, also making sure to be capitalized.
    - Explains the goal of the game
    - Uses three types: Dark, Psychic, and Fighting.
    - Describes the type triangle, where Dark is super-effective on Psychic, Psychic is super-effective on Fighting,
      and Fighting is super-effective on Dark.
    - Player will encounter trainers, find items, and participate in Python Trivia challenges.

    No parameters for this function.
    """

    response = requests.get("https://randomuser.me/api/")
    data = response.json()
    intro_name = data["results"][0]["name"]["first"].capitalize()

    print("Hello! Welcome to Victory Road!")
    print(f"My name is, {intro_name}, and let me tell you about what you should expect from this game!")
    print("Your goal is to get through the maze with your 3 types: Dark, Psychic, and Fighting.")
    print("They're set up as a type triangle.")
    print("That means Dark is super-effective on Psychic, Psychic is super-effective on Fighting, and Fighting is super-effective on Dark.")
    print("You will end up fighting trainers, finding items, and answering fun Python Trivia! Are you Ready?")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

type_regex = re.compile(r"^(Dark|Psychic|Fighting)$")

class Battle:
    """
    Class of a battle between the traveler (player) and a trainer in Victory Road.

    Attributes:
    - types: A dictionary of each type and its super-effective counterpart.
    - lives: The number of lives the traveler (player) has.

    Methods:
    - battle(player_type, trainer_type): Figures out who wins depending on the typing.
    - start_battle(): Starts an actual battle between the traveler (player) and a randomly chosen trainer type.
    """

    def __init__(self, lives):
        self.types = {
            "Dark": ["Psychic"],
            "Psychic": ["Fighting"],
            "Fighting": ["Dark"],
        }
        self.lives = lives

    def battle(self, player_type, trainer_type):
        """
        Figures out who wins depending on the typing.

        Parameters:
        - player_type (str): The 3 player types (Dark, Psychic, or Fighting).
        - trainer_type (str): The type of the trainer.

        Returns:
        - str: The outcome of the battle. Possible outcomes:
            - "You win!": If the traveler (player) wins.
            - "Victory Road Trainer wins!": If the trainer wins the battle.
        
        The method uses stats.bernoulli.rvs to determine the winner based on type advantages and a
        player's and trainer's chosen types, Type Advantage = 70% of winning, Neutral = 50%, Type Weakness = 30%.

        If the traveler (player) loses, they lose a life.
        """
        if player_type in self.types and trainer_type in self.types[player_type]:
            if stats.bernoulli.rvs(0.7):
                return "You win!"
            else:
                return "Victory Road Trainer wins!"
        elif player_type == trainer_type:
            if stats.bernoulli.rvs(0.5):
                return "You win!"
            else:
                return "Victory Road Trainer wins!"
        elif trainer_type in self.types and player_type in self.types[trainer_type]:
            return "Victory Road Trainer wins!"
        else:
            if stats.bernoulli.rvs(0.3):
                return "You win!"
            else:
                self.lives -= 1
                return "Victory Road Trainer wins!"

    def start_battle(self):
        """
        Starts an actual battle between the traveler (player) and a randomly chosen trainer type.

        The method randomly chooses a trainer type, asks the traveler (player) to choose a type,
        and continues the battle until the player loses a life or wins the battle.

        Battle Rules:
        If the traveler (player) wins, they can continue.
        If the trainer wins, the traveler (player) loses a life, but can still continue.
        If the trainer wins, and the traveler (player) has no lives left, the game is then over.
        """
        trainer_type = random.choice(list(self.types.keys()))
        print("Victory Road Trainer has a", trainer_type, "type!")
        print("Lives remaining:", self.lives)

        while self.lives > 0:
            player_type = input("Choose your type (Dark, Psychic, or Fighting): ")

            while not type_regex.match(player_type):
                print("Invalid type! Please choose Dark, Psychic, or Fighting.")
                player_type = input("Choose your type (Dark, Psychic, or Fighting): ")

            outcome = self.battle(player_type, trainer_type)
            print("You chose type:", player_type)
            print("Victory Road Trainer chose:", trainer_type)
            print(outcome)

            if outcome == "Victory Road Trainer wins!":
                self.lives -= 1
                print("You have", self.lives, "lives left.")
                break
            elif outcome == "You win!":
                print("You have", self.lives, "lives left.")
                break

        if self.lives <= 0:
            print("Game over! You lost all your lives.")

class TrainerBossBattle(Battle):
    """
    The boss battle between the traveler (player) and the Victory Road Boss Trainer.

    The class inherits the 'Battle class' and overrides the 'start_battle()' method.

    Method Override:
    - start_battle(): Starts a boss battle against the Victory Road Boss Trainer.
    """
    def start_battle(self):
        """
        Starts a battle sequence against the boss trainer in the Victory Road game.

        The method randomizes the available trainer types and starts a battle with the boss trainer.
        The battle doesn't stop until the player wins three times or runs out of lives.

        Battle:
        - The method asks the traveler (player) to choose their type (Dark, Psychic, or Fighting).
        - If the chosen type is invalid, the method displays an error message and asks the player again.
        - The battle's winner is determined by the 'battle' method from the 'Battle' class.
        - The types chosen, lives, and the battle outcome are also printed..

        If the traveler (player) wins three battles, the method shows a victory message.
        If the player runs out of lives/loses the battle, the method displays a game over message.

        No parameters are required for this method.
        """
        
        trainer_types = list(self.types.keys())
        random.shuffle(trainer_types)

        player_wins = 0

        while player_wins < 3 and self.lives > 0:
            trainer_type = trainer_types[player_wins % len(trainer_types)]
            print("Victory Road Boss Trainer has a", trainer_type, "type!")
            print("Lives remaining:", self.lives)

            player_type = input("Choose your type (Dark, Psychic, or Fighting): ")

            while not type_regex.match(player_type):
                print("Invalid type! Please choose Dark, Psychic, or Fighting.")
                player_type = input("Choose your type (Dark, Psychic, or Fighting): ")

            outcome = self.battle(player_type, trainer_type)
            print("You chose type:", player_type)
            print("Victory Road Boss Trainer chose:", trainer_type)

            print("")

            print(outcome)

            if outcome == "Victory Road Trainer wins!":
                self.lives -= 1
                print("Try Again! Lives remaining:", self.lives)
            elif outcome == "You win!":
                player_wins += 1

            print("")

            if player_wins == 3:
                print("Congratulations! You defeated the Boss Trainer!")
                break

        if self.lives <= 0:
            print("Game over! You ran out of lives.")

class VictoryRoad:
    """
    This class is for the Victory Road game.

    The class starts the game, creates dictionary of rooms that can be interacted with, battle the trainers, answer trivia questions,
    find health points, and even save and load game progress.

    Attributes:
    - directions: A list of directions (north, south, east, west) for movement.
    - rooms: A dictionary representing the game rooms in Victory Road.
    - lives: An integer which is the number of lives the traveler (player) has.
    - conn: Connects to the SQLite database.

    Methods:
    - __init__(self, initial_lives): Initializes the Victory Road game.
    - create_table(self): Creates the SQLite table to store game progress.
    - traveler_save(self): Saves the travelers (players) lives to the database.
    - traveler_load(self): Loads the travelers (players) lives from the database.
    - play(self): Plays the game and starts the travelers (players) movement, battles, trivia questions, and game completion.
    - start(self): Starts the Victory Road game.
    """
    def __init__(self, initial_lives):
        """
        Initializes the Victory Road game.

        Parameters:
        - initial_lives: An integer which is the initial number of lives for the traveler (player).
        """
        self.directions = ["north", "south", "east", "west"]
        self.rooms = {
            "Entrance": {"north": "Mid"},

            "Mid": {"north": "Trainer1", "south": "Entrance", "east": "PathE", "west": "PathW"},

            "PathW": {"north": "LifePoint", "south": "Trainer2", "east": "Mid"},

            "PathE": {"east": "DeadEnd", "south": "Trivia1", "west": "Mid"},

            "Trainer1": {"east": "Trainer3", "south": "Mid"},

            "Trainer2": {"north": "PathW"},

            "Trainer3": {"north": "Trivia2", "west": "Trainer1"},

            "DeadEnd": {"west": "PathE"},

            "Trivia1": {"north": "PathE"},

            "Trivia2": {"north": "TrainerBoss", "south": "Trainer3"},

            "LifePoint": {"south": "PathW"},

            "TrainerBoss": {"north": "BossExit"},

            "BossExit": {}
        }
        self.lives = initial_lives
        self.conn = sqlite3.connect("victory_road.db")
        self.create_table()

    def create_table(self):
        """
        Creates the SQLite table to store game progress.

        Creates a table named traveler in the database to store the progress.
        The table has three columns: id, name, and lives.
        """
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS traveler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                lives INTEGER NOT NULL
            )
            """
        )

        self.conn.commit()
        cursor.close()

    def traveler_save(self):
        """
        Saves the lives to the database.

        It inserts/updates the lives in the traveler table of the database.
        The name is set to 'Traveler1'.
        """
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO traveler (name, lives)
            VALUES (?, ?)
            ON CONFLICT (id)
            DO UPDATE SET lives = excluded.lives
            """,
            ("Traveler1", self.lives),
        )

        self.conn.commit()
        cursor.close()

    def traveler_load(self):
        """
        Loads the lives from the database.

        Retrieves the lives from the traveler table of the database.
        The name is set to 'Traveler1'.
        """
        cursor = self.conn.cursor()

        cursor.execute("SELECT lives FROM traveler WHERE name = ?", ("Traveler1",))
        result = cursor.fetchone()

        if result is not None:
            self.lives = result[0]
            print("Lives:", self.lives)

        cursor.close()

    def play(self):
        """
        Plays the game and starts the travelers (players) movement, battles, trivia questions, and game completion.

        Starts the Victory Road game and controls the main game loop.
        It asks for movement direction, updates the room position, starts battles with trainers, gives extra health, and asks trivia.
        The game doesn't stop until you either run out of lives or defeat the Trainer Boss and leave 'BossExit'.
        """
        room_pos = "Entrance"
        print("You're now entering Victory Road. Good Luck!\n")

        self.traveler_load()

        while room_pos != "BossExit" and self.lives > 0:
            print("You are in", room_pos + ".")
            print("You can go:", ", ".join(self.rooms[room_pos].keys()))

            direction = input("Where to, traveler? ")
            direction = direction.lower()

            if direction in self.rooms[room_pos]:
                room_pos = self.rooms[room_pos][direction]

                if room_pos.startswith("Trainer"):
                    if room_pos == "TrainerBoss":
                        battle = TrainerBossBattle(self.lives)
                    else:
                        battle = Battle(self.lives)

                    battle.start_battle()
                    self.lives = battle.lives

                if room_pos == "LifePoint":
                    self.lives += 1
                    print("+1 to your Health!", self.lives)

                if room_pos == "Trivia2":
                    print("Fill in the Blank: With web scraping, you rely on consistent formatting on a web page (or site) and write code to ___ the data you want.")
                    t2_answer = input("Your Answer is: ")
                    if t2_answer.lower == "extract":
                        self.lives += 1
                        print("+1 to your Health!", self.lives)
                    else:
                        print("Wrong! The correct answer is: extract")

                if room_pos == "Trivia1":
                    print("What is Hyper Text Markup Language commonly known as?")
                    t1_answer = input("Your Answer is: ")
                    if t1_answer.lower == "html":
                        self.lives += 1
                        print("+1 to your Health!", self.lives)
                    else:
                        print("Wrong! The correct answer is: HTML")
                    

            else:
                print("You can't go that way!\n")

        if room_pos == "BossExit":
            print("Congrats! You have defeated the Boss. You have successfully completed Victory Road!")
        
        self.traveler_save()

    def start(self):
        """
        Starts the Victory Road game.

        Starts the Victory Road game by calling all the methods.
        It clears the screen, shows the game introduction, and then starts with the 'play' method.
        If any error occurs during the game, it displays an error message, like the Try-Except.
        Finally, it closes the database connection.
        """
        try:
            clear()
            intro()
            self.play()
        except Exception as e:
            print("Game could not start, an error has occurred:", str(e))
        finally:
            self.conn.close()

VictoryRoad(3).start()
