from datetime import datetime
from time import time
import csv
from .units import Measure, MeasurementParser

class DataSeries():
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
        self.most_recent = None # Holds the latest recorded entry date
        self.entries = []
        self._i = 0 # Index of current iteration

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries) 

    def __iadd__(self, rhs):
        self.add_entry(rhs)
        return self

    def get_values(self, count):
        i = len(self.entries) - 1
        r = []
        while i >= 0 and len(r) < count:
            r.append(self.entries[i][1])
            i -= 1
        return r

    def add_entry(self, measurement, date=datetime.now()):
        m = Measure(measurement, self.unit)
        date = date.replace(hour=5, minute=0, second=0, microsecond=0)
        if len(self.entries) == 0 or self.entries[len(self.entries)-1][0] < date:
            self.entries.append((date, m))
        else: # Yeah, I could do a binary search to find where to put it, but this is Python so memory no longer matters, nothing does really
            i = len(self.entries)-1
            while i > -1 and self.entries[i][0] > date:
                i -= 1
            self.entries.insert(i+1,(date, m))

    def get_entry_on_date(self, date):
        date = date.replace(hour=5, minute=0, second=0, microsecond=0)
        j = len(self.entries)-1
        for i in range(j, -1, -1):
            if self.entries[i][0] == date:
                return self.entries[i][1]

    def get_most_recent_entry(self):
        if len(self.entries) == 0:
            return None
        return self.entries[len(self.entries)-1][1]

    def write_to_file(self, file_handle):
        for date,measure in self.entries:
            file_handle.write(str(date.timestamp()) + "," + str(measure.value) + "," + str(measure.unit) + "\n")

    @staticmethod
    def read_from_file(name, file_handle, unit):
        s = DataSeries(name, unit)
        reader = csv.reader(file_handle)
        for row in reader:
            d = datetime.fromtimestamp(float(row[0]))
            m = MeasurementParser.parse(row[1] + " " + row[2])
            s.add_entry(m, date=d)
        return s

