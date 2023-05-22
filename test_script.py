import random
from final_project import Battle
from final_project import VictoryRoad

def test_battle_init():
    """
    Test case for initializing a Battle.

    Checks if the Battle is initialized correctly with the correct number of lives,
    and if the dictionary of type coverages are all correct.

    Returns:
        None

    Raises:
        AssertionError: If the assertions fail/ don't equal what is being tested.
    """
    lives = 3
    final_project = Battle(lives)

    types = {
        "Dark": ["Psychic"],
        "Psychic": ["Fighting"],
        "Fighting": ["Dark"],
    }
    assert final_project.types == types
    assert final_project.lives == lives

def test_battle():
    """
    Test case for the battle method in the Battle class.

    Tests different outcomes of battle scenarios and checks if the expected results are returned.

    Returns:
        None

    Raises:
        AssertionError: If the assertions fail/ don't equal what is being tested.
    """
    final_project = Battle()

    result = final_project.battle("Fighting", "Dark")
    assert result == "You win!"

    result = final_project.battle("Psychic", "Fighting")
    assert result == "Victory Road Trainer wins!"

    result = final_project.battle("Psychic", "Psychic")
    assert result in ["You win!", "Victory Road Trainer wins!"]

def test_victory_road_init():
    """
    Test case for initializing a Victory Road instance.

    Tests if the Victory Road instance is initialized correctly with the intital number of lives/
    Tests if the dictionary of rooms and the directions are set up right.

    Returns:
        None

    Raises:
        AssertionError: If the assertions fail/ don't equal what is being tested.
    """
    lives = 3
    final_project = VictoryRoad(lives)

    assert final_project.directions == ["north", "south", "east", "west"]
    rooms = {
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
    assert final_project.rooms == rooms
    assert final_project.lives == lives