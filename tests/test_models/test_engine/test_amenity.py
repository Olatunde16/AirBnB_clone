#!/usr/bin/python3
import os
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Unittests for the Amenity class."""

    @classmethod
    def setUpClass(cls):
        cls.am = Amenity()

    @classmethod
    def tearDownClass(cls):
        del cls.am

    def test_instantiation(self):
        self.assertIsInstance(self.am, Amenity)
        self.assertIn(self.am, models.storage.all().values())
        self.assertIsInstance(self.am.id, str)
        self.assertIsInstance(self.am.created_at, datetime)
        self.assertIsInstance(self.am.updated_at, datetime)
        self.assertEqual("", Amenity.name)
        self.assertNotIn("name", self.am.__dict__)

    def test_two_amenities(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)
        self.assertLess(am1.created_at, am2.created_at)
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity(id="123456", created_at=dt, updated_at=dt)
        self.assertIn("[Amenity] (123456)", str(am))
        self.assertIn("'id': '123456'", str(am))
        self.assertIn("'created_at': " + dt_repr, str(am))
        self.assertIn("'updated_at': " + dt_repr, str(am))

    def test_save_method(self):
        first_updated_at = self.am.updated_at
        sleep(0.05)
        self.am.save()
        self.assertLess(first_updated_at, self.am.updated_at)

    def test_save_updates_file(self):
        amid = "Amenity." + self.am.id
        self.am.save()
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())

    def test_to_dict_method(self):
        dt = datetime.today()
        self.am.id = "123456"
        self.am.created_at = self.am.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.am.to_dict(), tdict)


if __name__ == "__main__":
    unittest.main()
