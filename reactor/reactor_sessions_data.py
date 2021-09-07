import reactor_database as db
from reactor_database import retrieve_entries
import datetime
from datetime import timedelta
from statistics import mode


# def retrieve(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up, accuracy_down,
#              accuracy_left, accuracy_right, accuracy_all, worst_wrong_dir, worst_door_acc,
#              worst_wrong_scenario, attempts, time_elapsed, command):
#
#     if command == "retrieve":
#         result = db.database(user_name, level, react_up, react_down, react_left, react_right, react_all, accuracy_up,
#                              accuracy_down, accuracy_left, accuracy_right, accuracy_all, worst_wrong_dir,
#                              worst_door_acc, worst_wrong_scenario, attempts, time_elapsed, command)
#     else:
#         return "invalid entry"

def retrieve(user_name):
    result = retrieve_entries(user_name)

    # test - to see what exists on 'result'
    # for idx, item in enumerate(result):
    #     print(idx, item)

    def data_sorter(data):

        directions = ['NA', 'up', 'down', 'left', 'right']

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
        assertion = []
        elapsed = []

        sessions = []
        for session in data:

            levels.append(int(session[2]))

            try:
                r_up.append(float(session[3]))
            except ValueError:
                r_up.append(0)
            try:
                r_down.append(float(session[4]))
            except ValueError:
                r_down.append(0)
            try:
                r_left.append(float(session[5]))
            except ValueError:
                r_left.append(0)
            try:
                r_right.append(float(session[6]))
            except ValueError:
                r_right.append(0)
            try:
                r_all.append(float(session[7]))
            except ValueError:
                r_all.append(0)
            try:
                r_fastest.append((session[8].split()[0], float(session[8].split()[-1])))
            except ValueError:
                r_fastest.append(0)
            try:
                r_slowest.append((session[9].split()[0], float(session[9].split()[-1])))
            except ValueError:
                r_slowest.append(0)
            try:
                p_up.append(float(session[10]))
            except ValueError:
                p_up.append(0)
            try:
                p_down.append(float(session[11]))
            except ValueError:
                p_down.append(0)
            try:
                p_left.append(float(session[12]))
            except ValueError:
                p_left.append(0)
            try:
                p_right.append(float(session[13]))
            except ValueError:
                p_right.append(0)
            try:
                p_all.append(float(session[14]))
            except ValueError:
                p_all.append(0)

            w_launch.append(directions.index(session[15].split()[0]))
            w_door.append(directions.index(session[16].split()[0]))

            try:
                if float(session[17].split()[-1]) > 100:
                    assertion.append(100)
                else:
                    assertion.append(float(session[17].split()[-1]))
            except ValueError:
                assertion.append(0)
            elapsed.append(int(session[18]))

        sessions.append(levels)
        sessions.append(r_up)
        sessions.append(r_down)
        sessions.append(r_left)
        sessions.append(r_right)
        sessions.append(r_all)
        sessions.append(r_fastest)
        sessions.append(r_slowest)
        sessions.append(p_up)
        sessions.append(p_down)
        sessions.append(p_left)
        sessions.append(p_right)
        sessions.append(p_all)
        sessions.append(w_launch)
        sessions.append(w_door)
        sessions.append(assertion)
        sessions.append(elapsed)

        return sessions

    def averager(category, data):

        if category not in [6, 7, 13, 14]:
            size = len(data)
            total = sum(data)
            return round(total / size, 2)

        elif category in [6, 7]:

            directions = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
            for item in data:
                directions[item[0]] += 1

            greatest = max({k for k, v in directions.items()})

            counts = []
            for item in data:
                if item[0] == greatest:
                    counts.append(item[-1])

            size = len(counts)
            total = sum(counts)
            return greatest, round(total / size, 2)

        else:
            return mode(data)

    def current_day(data):
        today_date = datetime.datetime.today().strftime("%d%m%y")

        today = []
        for entry in data:
            if entry[1][-6:] == today_date:
                today.append(entry)

        return data_sorter(today)

    def by_day(data):
        today = datetime.date.today()
        days_date = [(today - timedelta(days=n)).strftime("%d%m%y") for n in range(365)]

        # print(f"data: {data}")

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

        # print(f"all_days: {all_days}")
        # for day in all_days:
        #     print(f"day {day}")

        # blank_lists = [[] for _ in range(365 - len(all_days))]
        # for blank in blank_lists:
        #     all_days.append(blank)

        # print(f"\n\nby_day({len(all_days)}): {all_days}\n\n")
        # categories = [' 0 level', ' 1 up success reaction times average', ' 2 down success reaction times average',
        #               ' 3 left success reaction times average', ' 4 right success reaction times average',
        #               ' 5 total success reaction times average', ' 6 fastest direction success average',
        #               ' 7 slowest direction success average', ' 8 up shots percentage', ' 9 down shots percentage',
        #               '10 left shots percentage', '11 right shots percentage', '12 total shots percentage',
        #               '13 worst wrong launch direction', '14 worst mistook door', '15 assertion', '16 time elapsed', ]

        all_categories, inner = [], []
        category = 0
        for idx_category in range(17):
            for a_day in all_days:
                day_categories = data_sorter(a_day)
                inner.append(averager(idx_category, day_categories[idx_category]))
            all_categories.append(inner)
            inner = []

        return all_categories

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

        print(f"\n\nby_month({len(all_months)}): {all_months}\n\n")

        data_sorter(all_months)

    # print("today")
    # day = current_day(result)
    # print("dailny")
    daily = by_day(result)
    # print("weekly")
    # by_week(result)
    # print("monthly")
    # by_month(result)

    return daily






