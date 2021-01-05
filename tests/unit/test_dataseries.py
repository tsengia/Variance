from datetime import datetime, timedelta
import pathlib
from unittest import TestCase

import variance
from variance.core.units import *
from variance.core.series import DataSeries

class TestDataSeries(TestCase):
    def test_init(self):
        d = DataSeries("test1", LengthUnit.INCH)
        self.assertEqual(d.name, "test1")
        self.assertEqual(d.unit, LengthUnit.INCH)
        self.assertEqual(len(d.entries), 0)
        self.assertEqual(len(d), 0)
        self.assertEqual(d.get_most_recent_entry(), None)

    def test_three_entries(self):
        d = DataSeries("test2", LengthUnit.CENTIMETER)
        self.assertEqual(len(d), 0)
        d.add_entry(Inches(10), datetime.now() - timedelta(days=1))
        self.assertEqual(len(d), 1)
        self.assertEqual(d.get_most_recent_entry(), Inches(10))
        d.add_entry(Feet(1), datetime.now() - timedelta(days=2))
        self.assertEqual(len(d), 2)
        self.assertEqual(d.get_most_recent_entry(), Inches(10))
        d.add_entry(Yards(1))
        self.assertEqual(len(d), 3)
        self.assertEqual(d.get_most_recent_entry(), Yards(1))
        self.assertEqual(d.get_entry_on_date(datetime.now() - timedelta(days=2)), Feet(1))

    def test_values(self):
        d = DataSeries("testA", MassUnit.POUND)
        d.add_entry(Pounds(1), datetime.now() - timedelta(days=5))
        d.add_entry(Pounds(2), datetime.now() - timedelta(days=4))
        d.add_entry(Pounds(3), datetime.now() - timedelta(days=3))
        d.add_entry(Pounds(4), datetime.now() - timedelta(days=2))
        d.add_entry(Pounds(5), datetime.now() - timedelta(days=1))
        d += Pounds(6)
        next_i = Pounds(6)
        for i in d.get_values(10):
            self.assertEqual(i, next_i)
            next_i -= Pounds(1)
        self.assertEqual(next_i, Pounds(0))
        next_i = Pounds(6)
        k = d.get_values(3)
        self.assertEqual(len(k), 3)
        for i in k:
            self.assertEqual(i, next_i)
            next_i -= Pounds(1)
        self.assertEqual(next_i, Pounds(3))

    def test_iteration(self):
        d = DataSeries("test3", MassUnit.MILLIGRAM) 
        d.add_entry(Milligrams(1), datetime.now() - timedelta(days=5))
        d.add_entry(Milligrams(2), datetime.now() - timedelta(days=4))
        d.add_entry(Milligrams(3), datetime.now() - timedelta(days=3))
        d.add_entry(Milligrams(4), datetime.now() - timedelta(days=2))
        d.add_entry(Milligrams(5), datetime.now() - timedelta(days=1))
        d += Milligrams(6)
        next_i = Milligrams(1)
        for i in d:
            self.assertEqual(i[1], next_i)
            next_i += Milligrams(1)
        self.assertEqual(next_i, Milligrams(7))


    def test_write(self):
        d = DataSeries("test4", MassUnit.MILLIGRAM) 
        d.add_entry(Milligrams(1), datetime.now() - timedelta(days=5))
        d.add_entry(Milligrams(2), datetime.now() - timedelta(days=4))
        d.add_entry(Milligrams(3), datetime.now() - timedelta(days=3))
        d.add_entry(Milligrams(4), datetime.now() - timedelta(days=2))
        d.add_entry(Milligrams(5), datetime.now() - timedelta(days=1))
        with open("test-write-tmp-fileasdfghjkl12345.csv", "w") as f:
            d.write_to_file(f)
        with open("test-write-tmp-fileasdfghjkl12345.csv", "r") as f:
            k = DataSeries.read_from_file("test4", f, MassUnit.MILLIGRAM)
        pathlib.Path("test-write-tmp-fileasdfghjkl12345.csv").unlink()
        self.assertEqual(d.get_most_recent_entry(), k.get_most_recent_entry())
        self.assertEqual(len(d), len(k))
        self.assertEqual(d.get_values(10), k.get_values(10))
