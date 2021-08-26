import sqlite3
import datetime


def database(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up, accuracy_down,
             accuracy_left, accuracy_right, accuracy_all, attempts, worst_wrong_dir, worst_door_acc,
             worst_wrong_scenario, command):
    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS entries " \
                   "(user_name TEXT, " \
                   "timestamp TEXT, " \
                   "level TEXT, " \
                   "reaction_avg_up TEXT, " \
                   "reaction_avg_down TEXT, " \
                   "reaction_avg_left TEXT, " \
                   "reaction_avg_right TEXT, " \
                   "reaction_avg_all TEXT, " \
                   "accuracy_up TEXT, " \
                   "accuracy_down TEXT, " \
                   "accuracy_left TEXT, " \
                   "accuracy_right TEXT, " \
                   "accuracy_all TEXT, " \
                   "attempts TEXT, " \
                   "worst_wrong_direction TEXT, " \
                   "worst_door_accuracy TEXT, " \
                   "worst_wrong_scenario TEXT)"

    CREATE_ENTRY = "INSERT INTO entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    RETRIEVE_ENTRIES = "SELECT * FROM entries WHERE user_name = (?) ORDER BY rowid DESC"

    def timestamp():
        return datetime.datetime.today().strftime("%S%M%H%d%m%y")

    def create_tables():
        with sqlite3.connect("reactor_data.db") as connection:
            connection.execute(CREATE_TABLE)

    def create_entry(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up,
                     accuracy_down, accuracy_left, accuracy_right, accuracy_all, attempts, worst_wrong_dir,
                     worst_door_acc, worst_wrong_scenario):
        with sqlite3.connect("reactor_data.db") as connection:
            connection.execute(CREATE_ENTRY, (
                user_name, timestamp(), level, react_up, react_down, react_left, react_right, react_all, accuracy_up,
                accuracy_down, accuracy_left, accuracy_right, accuracy_all, attempts, worst_wrong_dir, worst_door_acc,
                worst_wrong_scenario))

    def retrieve_entries(user_name):
        with sqlite3.connect("reactor_data.db") as connection:
            cursor = connection.cursor()
            cursor.execute(RETRIEVE_ENTRIES, user_name)
            return cursor.fetchall()

    create_tables()
    if command == "entry":
        create_entry(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up,
                     accuracy_down, accuracy_left, accuracy_right, accuracy_all, attempts, worst_wrong_dir,
                     worst_door_acc, worst_wrong_scenario)
    elif command == "retrieve":
        return retrieve_entries(user_name)


# test data

# user_name = "benny"
# level = 26
# react_up = 300.0
# react_down = 310.1
# react_left = 315.5
# react_right = 399.99
# react_all = 350
# accuracy_up = 80
# accuracy_down = 70
# accuracy_left = 60
# accuracy_right = 58
# accuracy_all = 65
# attempts = 90
# worst_wrong_dir = "right"
# worst_door_acc = "down"
# worst_wrong_scenario = "shot down door left"
#
# database(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up, accuracy_down,
#     accuracy_left, accuracy_right, accuracy_all, attempts, worst_wrong_dir, worst_door_acc, worst_wrong_scenario)

"""
'Minicon' project using conway's game of life
color fading using pygame
was introduced to Haskell
learned about Merge sort
started new github: thejourneyville
'Dissolving Octagons' project
learned about Closest Points algorithm in O(n log n)
learned about Shortest Path using BFS
WIP game: Reactor (measures/records/analyzes reaction speed)
'


"""