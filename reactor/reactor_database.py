import sqlite3
import datetime


def database(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up, accuracy_down,
             accuracy_left, accuracy_right, accuracy_all, worst_wrong_dir, worst_door_acc,
             attempts, time_elapsed, command):

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
                   "worst_wrong_direction TEXT, " \
                   "worst_door_accuracy TEXT, " \
                   "attempts TEXT, " \
                   "time_elapsed TEXT)"

    CREATE_ENTRY = "INSERT INTO entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    def timestamp():
        return datetime.datetime.today().strftime("%d%m%y")

    def create_tables():
        with sqlite3.connect("reactor_data.db") as connection:
            connection.execute(CREATE_TABLE)

    def create_entry(name, lev, r_up, r_down, r_left, r_right, r_all, acc_up,
                     acc_down, acc_left, acc_right, acc_all, wrst_wrong_dir,
                     wrst_door_acc, assertion, tme_elapsed):

        with sqlite3.connect("reactor_data.db") as connection:
            connection.execute(CREATE_ENTRY, (
                name, timestamp(), lev, r_up, r_down, r_left, r_right, r_all, acc_up,
                acc_down, acc_left, acc_right, acc_all, wrst_wrong_dir, wrst_door_acc,
                assertion, tme_elapsed))

    create_tables()
    if command == "entry":
        create_entry(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up,
                     accuracy_down, accuracy_left, accuracy_right, accuracy_all, worst_wrong_dir,
                     worst_door_acc, attempts, time_elapsed)


def retrieve_entries(name):

    RETRIEVE_ENTRIES = "SELECT * FROM entries WHERE user_name = (?) ORDER BY rowid DESC"

    with sqlite3.connect("reactor_data.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_ENTRIES, (name,))
        return cursor.fetchall()



