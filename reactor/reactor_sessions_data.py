import reactor_database as db
import datetime
from datetime import timedelta


def retrieve(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up, accuracy_down,
             accuracy_left, accuracy_right, accuracy_all, worst_wrong_dir, worst_door_acc,
             worst_wrong_scenario, attempts, time_elapsed, command):

    if command == "retrieve":
        result = db.database(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up,
                             accuracy_down, accuracy_left, accuracy_right, accuracy_all, worst_wrong_dir,
                             worst_door_acc, worst_wrong_scenario, attempts, time_elapsed, command)
    else:
        return "invalid entry"

    # test - to see what exists on 'result'
    # for idx, item in enumerate(result):
    #     print(idx, item)

    def data_sorter(data):
        levels = []
        r_up = []
        r_down = []
        r_left = []
        r_right = []
        r_all = []
        r_fastest = []
        r_slowest = []
        p_up = []
        p_down = []
        p_left = []
        p_right = []
        p_all = []
        w_launch = []
        w_door = []
        w_scene = []
        assertion = []
        elapsed = []

        directions = ['NA', 'up', 'down', 'left', 'right']

        for entry in data:

            check_directions = [entry[3], entry[4], entry[5], entry[6]]
            reaction_directions = []
            for item in check_directions:
                try:
                    reaction_directions.append(float(item))
                except ValueError:
                    continue

            levels.append(int(entry[2]))

            try:
                r_up.append(float(entry[3]))
            except ValueError:
                r_up.append(0)
            try:
                r_down.append(float(entry[4]))
            except ValueError:
                r_down.append(0)
            try:
                r_left.append(float(entry[5]))
            except ValueError:
                r_left.append(0)
            try:
                r_right.append(float(entry[6]))
            except ValueError:
                r_right.append(0)
            try:
                r_all.append(float(entry[7]))
            except ValueError:
                r_all.append(0)
            if reaction_directions:
                r_fastest.append(min(reaction_directions))
                r_slowest.append(max(reaction_directions))
            else:
                r_fastest.append(0)
                r_slowest.append(0)
            try:
                p_up.append(float(entry[8]))
            except ValueError:
                p_up.append(0)
            try:
                p_down.append(float(entry[9]))
            except ValueError:
                p_down.append(0)
            try:
                p_left.append(float(entry[10]))
            except ValueError:
                p_left.append(0)
            try:
                p_right.append(float(entry[11]))
            except ValueError:
                p_right.append(0)
            try:
                p_all.append(float(entry[12]))
            except ValueError:
                p_all.append(0)
            w_launch.append(directions.index(entry[13].split()[0]))
            w_door.append(directions.index(entry[14].split()[0]))
            if entry[15] != "None":
                w_scene.append(entry[15])
            else:
                w_scene.append(0)
            try:
                assertion.append(float(entry[16].split()[-1]))
            except ValueError:
                assertion.append(0)
            elapsed.append(int(entry[17]))

        s = [levels,
             r_up,
             r_down,
             r_left,
             r_right,
             r_all,
             r_fastest,
             r_slowest,
             p_up,
             p_down,
             p_left,
             p_right,
             p_all,
             w_launch,
             w_door,
             w_scene,
             assertion,
             elapsed]

        print()
        for item in s:
            print(item)





    def current_day(data):
        today_date = datetime.datetime.today().strftime("%d%m%y")

        day = []
        for entry in data:
            if entry[1][-6:] == today_date:
                day.append(entry)

        # print(f"today ({len(day)}): {day}")

        data_sorter(day)

    def by_day(data):
        today = datetime.date.today()
        days_date = [(today - timedelta(days=n)).strftime("%d%m%y") for n in range(365)]

        day = 0
        all_days, inner = [], []
        for entry in data:
            while day <= 364:
                if entry[1][-6:] == days_date[day]:
                    inner.append(entry)
                    break
                else:
                    day += 1
                    all_days.append(inner)
                    inner = []
                all_days.append(inner)

        blank_lists = [[] for _ in range(365 - len(all_days))]
        for blank in blank_lists:
            all_days.append(blank)

        print(f"\n\nby_day({len(all_days)}): {all_days}\n\n")

        data_sorter(all_days)

    def by_week(data):
        today = datetime.date.today()

        all_weeks_date, inner = [], []
        inner.append(datetime.datetime.today().strftime("%d%m%y"))
        for n in range(1, 365):
            if n % 7 == 0:
                inner.append((today - timedelta(days=n)).strftime("%d%m%y"))
                all_weeks_date.append(inner)
                inner = []
            else:
                inner.append((today - timedelta(days=n)).strftime("%d%m%y"))

        # print(f"\n\nall_weeks top: {all_weeks_date}")

        # NOTE: adds all entries to their corresponding week list:
        # [container[week 0(entry0)(entry1)][week 1(entry0)(entry1)]...]
        all_weeks, inner = [], []
        week = 0
        for entry in data:
            while week < 52:
                if entry[1][-6:] in all_weeks_date[week]:
                    inner.append(entry)
                    break
                else:
                    week += 1
                    if inner:
                        all_weeks.append(inner)
                    inner = []
        all_weeks.append(inner)

        # adds remaining blank lists to fill 52 weeks of 'all_weeks'
        blank_lists = [[] for _ in range(52 - len(all_weeks))]
        for blank in blank_lists:
            all_weeks.append(blank)

        print(f"\n\nby_week({len(all_weeks)}): {all_weeks}\n\n")

        data_sorter(all_weeks)

    # NOTE need to figure out how to store monthly data starting from this month and that there's no overlap
    def by_month(data):
        today = datetime.date.today()
        current_month = int(today.strftime("%m"))
        days = [(today - timedelta(days=n)).strftime("%d%m%y") for n in range(365)]

        jan, feb, mar, apr, may, jun, jul, aug, sep, ocT, nov, dec = [], [], [], [], [], [], [], [], [], [], [], []
        for item in days:
            if item[-4:-2] == "01":
                jan.append(item[-4:-2])
            elif item[-4:-2] == "02":
                feb.append(item[-4:-2])
            elif item[-4:-2] == "03":
                mar.append(item[-4:-2])
            elif item[-4:-2] == "04":
                apr.append(item[-4:-2])
            elif item[-4:-2] == "05":
                may.append(item[-4:-2])
            elif item[-4:-2] == "06":
                jun.append(item[-4:-2])
            elif item[-4:-2] == "07":
                jul.append(item[-4:-2])
            elif item[-4:-2] == "08":
                aug.append(item[-4:-2])
            elif item[-4:-2] == "09":
                sep.append(item[-4:-2])
            elif item[-4:-2] == "10":
                ocT.append(item[-4:-2])
            elif item[-4:-2] == "11":
                nov.append(item[-4:-2])
            elif item[-4:-2] == "12":
                dec.append(item[-4:-2])

        all_months_date = []
        for month in [jan, feb, mar, apr, may, jun, jul, aug, sep, ocT, nov, dec]:
            all_months_date.append(month)

        all_months, inner = [], []
        month_idx = current_month - 1
        for entry_idx in range(len(data)):
            while len(all_months) <= 12:
                if data[entry_idx][1][-4:-2] in all_months_date[month_idx]:
                    inner.append(data[entry_idx])
                    break
                else:
                    month_idx = (month_idx - 1) % 12
                    all_months.append(inner)
                    inner = []
        all_months.append(inner)

        blank_lists = [[] for _ in range(12 - len(all_months))]
        for blank in blank_lists:
            all_months.append(blank)

        data_sorter(all_months)

        print(f"\n\nby_month({len(all_months)}): {all_months}\n\n")

    current_day(result)
    # by_day(result)
    # by_week(result)
    # by_month(result)






