#!/usr/bin/python3
import unittest
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    def test_base_model(self):
        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89
        self.assertEqual(my_model.name, "My First Model")
        self.assertEqual(my_model.my_number, 89)
        self.assertEqual(str(my_model), "[BaseModel] ({}) {}".format(my_model.id, my_model.__dict__))
        initial_updated_at = my_model.updated_at
        my_model.save()
        self.assertNotEqual(my_model.updated_at, initial_updated_at)
        my_model_json = my_model.to_dict()
        self.assertEqual(my_model_json["name"], "My First Model")
        self.assertEqual(my_model_json["my_number"], 89)
        self.assertEqual(my_model_json["__class__"], "BaseModel")

if __name__ == "__main__":
    unittest.main()
