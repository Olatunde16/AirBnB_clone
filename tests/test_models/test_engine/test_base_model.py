#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModelInstantiation(unittest.TestCase):
    """Test cases for BaseModel instantiation."""

    def test_instantiation(self):
        """Test instantiation of BaseModel."""
        bm = BaseModel()
        self.assertIsInstance(bm, BaseModel)
        self.assertIsInstance(bm.id, str)
        self.assertIsInstance(bm.created_at, datetime)
        self.assertIsInstance(bm.updated_at, datetime)

    def test_custom_attributes(self):
        """Test instantiation of BaseModel with custom attributes."""
        custom_attrs = {"name": "Test", "value": 123}
        bm = BaseModel(**custom_attrs)
        for attr, value in custom_attrs.items():
            self.assertIn(attr, bm.__dict__)
            self.assertEqual(getattr(bm, attr), value)

    # Add other instantiation test methods...


class TestBaseModelSave(unittest.TestCase):
    """Test cases for BaseModel save method."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save_updates_updated_at(self):
        """Test if save method updates the updated_at attribute."""
        bm = BaseModel()
        initial_updated_at = bm.updated_at
        bm.save()
        self.assertGreater(bm.updated_at, initial_updated_at)

    # Add other save test methods...


class TestBaseModelToDict(unittest.TestCase):
    """Test cases for BaseModel to_dict method."""

    def test_to_dict_contains_correct_keys(self):
        """Test if to_dict method contains correct keys."""
        bm = BaseModel()
        keys = bm.to_dict().keys()
        self.assertSetEqual(set(keys), {"id", "created_at", "updated_at", "__class__"})

    # Add other to_dict test methods...


if __name__ == "__main__":
    unittest.main()
