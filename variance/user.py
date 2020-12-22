from time import time
from datetime import datetime
from enum import Enum
import pickle
import csv

from .config import *
from .series import DataSeries
from .body import Body, Sex

class UserList():
    def __iter__(self):
        return iter(self.users.keys())

    def __len__(self):
        return len(self.users)

    def remove_user(self, user):
        if isinstance(user, User):
            user = user.name
        del self.users[user]

    def add_user(self, user, path=None):
        if isinstance(user, User):
            user = user.name
        if path == None:
            path = USER_PATH / (user.lower().replace(" ", "-") + ".vusr")
        self.users[user] = Path(path)
        return self.users[user]

    def get_user_path(self, username):
        if isinstance(username, User):
            username = username.name
        return self.users[username]

    def change_user_path(self, user, path):
        if isinstance(user, User):
            user = user.name
        if user in self.users:
            self.users[user] = Path(path)

    def save(self):
        file_handle = open(self.file_path, "w")
        for u in self.users.keys():
            file_handle.write(u + "," + str(self.users[u]) + "\n")
        file_handle.close()

    def __init__(self, file_path):
        self.file_path = file_path
        self.users = {}
        if not file_path.is_file():
            self.file_path.touch()
        file_handle = open(file_path, "r")
        reader = csv.reader(file_handle) # The file is a CSV that goes name, filepath
        for row in reader:
            self.users[row[0]] = Path(row[1])
        file_handle.close()

class User():
    def __init__(self, name, sex, birthday):
        self.name = name
        self.birthday = birthday
        self.sex = sex 
        self.weight_tracker = DataSeries("weight", WEIGHT_TRACK_UNITS)
        self.height_tracker = DataSeries("height", HEIGHT_TRACK_UNITS)
        self.size_trackers = {}
        self.size_trackers["neck"] = DataSeries("neck-size", SIZE_TRACK_UNITS)
        self.size_trackers["waist"] = DataSeries("waist-size", SIZE_TRACK_UNITS)

    @property
    def height(self):
        return self.height_tracker.get_most_recent_entry()

    @property
    def weight(self):
        return self.weight_tracker.get_most_recent_entry()

    @property
    def age(self):
        return (datetime.now() - self.birthday).days // 365

    @staticmethod
    def load_from_file(file_handle):
        return pickle.load(file_handle)

    def save_to_file(self, file_handle):
        pickle.dump(self, file_handle)
