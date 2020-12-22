from pathlib import Path

from usda import UsdaClient
from units import *
from user import UserList, User, Sex
from cli_input import confirm_prompt, read_date, read_number, menu_select
from config import USDA_API_KEY, USER_PATH

new_user = False

def cls():
    print("\n" * 80)

# Verify that API key is set in config
if not USDA_API_KEY:
    print("Error: USDA_API_KEY not set in config.py!")
    exit(-1)
else:
    print("Using API key: " + USDA_API_KEY)

# Verify that the user data directory is present
if not USER_PATH:
    print("Error USER_PATH not set in config.py!")
    exit(-1)
if not USER_PATH.is_dir():
    new_user = True
    cls()
    print("Warning: Could not find USER_PATH " + str(USER_PATH) + "!")
    c = confirm_prompt("Create new directory? If first time, enter y [y/n]: ")
    if c:
        USER_PATH.mkdir()
        print("Created new directory " + str(USER_PATH))
    else:
        print("Exiting.")
        exit(-1)

user_list = UserList(USER_PATH / "users.csv")

if new_user:
    new_user = confirm_prompt("Are you a new user? [y/n]: ")

def create_new_user():
    cls()
    name = input("What is your name? ")
    s = menu_select(["Male","Female"], "What is your sex? ")
    if s == 0:
        s = Sex.MALE
    else:
        s = Sex.FEMALE
    birthday = read_date("What is your birthday? [yyyy, mm, dd] ")
    return User(name, s, birthday)

def select_user():
    cls()
    u = menu_select(["Create new user"] + list(user_list), "Select a user: ")
    if u == 0:
        u = create_new_user()
        user_list.add_user(u)
    else:
        u = User.load_from_file(open(user_list.get_user_path(list(user_list)[u - 1]), "rb"))
    return u

def change_user(current_user):
    current_user.save_to_file(open(user_list.get_user_path(current_user.name), "wb"))
    user_list.save()
    return select_user()

def view_tracker(tracker):
    cls()
    print("Tracker name: " + tracker.name)
    print("Entry count: " + str(len(tracker)))
    print("Latest measurement: " + str(tracker.get_most_recent_entry()))
    tracker.plot()
    a = menu_select(["Back to tracker menu", "Add entry"])
    if a == 1:
        d = read_date("Entry date [press enter for today]: ", today_default=True)
        m = read_number("Entry measurement (" + str(tracker.unit) + "): ")
        tracker.add_entry(Measure(m, tracker.unit))

def tracker_menu(user):
    cls()
    t = menu_select(["Back to main menu", "Weight", "Height", "Neck Size", "Waist Size"], "Select a tracker: ")
    if t == 1:
        view_tracker(user.weight_tracker)
    elif t == 2:
        view_tracker(user.height_tracker)
    elif t == 3:
        view_tracker(user.size_trackers["neck"])
    elif t == 4:
        view_tracker(user.size_trackers["waist"])

def main_menu(user):
    quit = False
    while not quit:
        cls()
        a = menu_select(["Change user", "View/Enter Tracker Data", "View/Edit Profile", "View/Edit Targets", "Meal Planning", "Workout Planning", "Exit"])
        if a == 0:
            user = change_user(user)
        elif a == 1:
            tracker_menu(user)

        if a == 6:
            quit = True
            user.save_to_file(open(user_list.get_user_path(user.name), "wb"))
            user_list.save()
            break

if new_user:
    u = create_new_user()
    user_list.add_user(u)
else:
    u = select_user()

main_menu(u)
