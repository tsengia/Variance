from datetime import datetime, timedelta
from unittest import TestCase

from context import variance
from variance.units import *
from variance.series import DataSeries

class TestDataSeries(TestCase):
    def test_init(self):
        d = DataSeries("test1", LengthUnit.INCH)
        self.assertEqual(d.name, "test1")
        self.assertEqual(d.unit, LengthUnit.INCH)
        self.assertEqual(len(d.entries), 0)
        self.assertEqual(len(d), 0)

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
