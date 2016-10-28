import unittest
import feed

class TestFeed(unittest.TestCase):

    def test_read_ingredients(self):
        ingredients = feed._read_ingredients()
        self.assertTrue(isinstance(ingredients, list))
        self.assertTrue(isinstance(ingredients[0], dict))
        self.assertEqual(len(ingredients), 471)

    def test_sanitize_ingredients(self):
        ing1 = {'CAL': 500, 'ITEM': "Foo"}
        ing2 = {'CAL': 700, 'ITEM': "Bar"}
        ing3 = {'CAL': 500, 'ITEM': "Baz"}
        ingredients_no_duplicate = [ing1, ing2]
        ingredients_duplicate = [ing1, ing2, ing3]

        set_no_duplicate = feed._sanitize_ingredients(ingredients_no_duplicate)
        set_duplicate = feed._sanitize_ingredients(ingredients_duplicate)
        self.assertEqual(len(set_no_duplicate), 2)
        self.assertEqual(len(set_duplicate), 2)
        self.assertNotEqual(set_no_duplicate, set_duplicate)

    def test_compute_average_calories(self):
        self.assertEqual(feed._compute_average_calories(2770, 3), 930)
        self.assertNotEqual(feed._compute_average_calories(330, 3), 115)
