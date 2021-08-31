import reactor_database as db


def retrieve(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up, accuracy_down,
             accuracy_left, accuracy_right, accuracy_all, attempts, worst_wrong_dir, worst_door_acc,
             worst_wrong_scenario, time_elapsed, command):

    if command == "retrieve":
        result = db.database(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up,
                             accuracy_down, accuracy_left, accuracy_right, accuracy_all, attempts, worst_wrong_dir,
                             worst_door_acc, worst_wrong_scenario, time_elapsed, command)
    else:
        return "invalid entry"

    for idx, item in enumerate(result):
        print(idx, result)
