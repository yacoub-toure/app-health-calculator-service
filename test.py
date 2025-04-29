import unittest
from health_utils import calculate_bmi, calculate_bmr
from app import app

class TestHealthUtils(unittest.TestCase):
    def test_calculate_bmi(self):
        self.assertAlmostEqual(calculate_bmi(1.75, 70), 22.86, places=2)
        self.assertAlmostEqual(calculate_bmi(1.60, 60), 23.44, places=2)
        with self.assertRaises(ValueError):
            calculate_bmi(0, 70)
        with self.assertRaises(ValueError):
            calculate_bmi(1.75, -10)

    def test_calculate_bmr_male(self):
        self.assertAlmostEqual(calculate_bmr(175, 70, 30, 'male'), 1695.67, places=2)
        with self.assertRaises(ValueError):
            calculate_bmr(175, 70, 0, 'male')
        with self.assertRaises(ValueError):
            calculate_bmr(175, -70, 30, 'male')

    def test_calculate_bmr_female(self):
        self.assertAlmostEqual(calculate_bmr(165, 60, 25, 'female'), 1405.33, places=2)
        with self.assertRaises(ValueError):
            calculate_bmr(165, 60, 25, 'other')

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_bmi_endpoint(self):
        response = self.app.post('/bmi', json={'height': 1.75, 'weight': 70})
        self.assertEqual(response.status_code, 200)
        self.assertIn('bmi', response.get_json())
        self.assertAlmostEqual(response.get_json()['bmi'], 22.86, places=2)

        response = self.app.post('/bmi', json={'height': 0, 'weight': 70})
        self.assertEqual(response.status_code, 400)

    def test_bmr_endpoint(self):
        response = self.app.post('/bmr', json={'height': 175, 'weight': 70, 'age': 30, 'gender': 'male'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('bmr', response.get_json())
        self.assertAlmostEqual(response.get_json()['bmr'], 1695.67, places=2)

        response = self.app.post('/bmr', json={'height': 165, 'weight': 60, 'age': 25, 'gender': 'female'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('bmr', response.get_json())
        self.assertAlmostEqual(response.get_json()['bmr'], 1405.33, places=2)

        response = self.app.post('/bmr', json={'height': 165, 'weight': 60, 'age': 25, 'gender': 'other'})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()