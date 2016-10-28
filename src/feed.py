import json
import math

def find_meal(cal, nbr_ingredients):
    meal_ingredients = []
    avg_cal = _compute_average_calories(cal, nbr_ingredients)
    available_ingredients = _sanitize_ingredients(_read_ingredients())
    while (nbr_ingredients > 0):
        if (nbr_ingredients > 1):
            meal_ingredients.append(available_ingredients[avg_cal])
            cal -= avg_cal
        else:
            meal_ingredients.append(available_ingredients[cal])
        nbr_ingredients -= 1
    return meal_ingredients

def _read_ingredients():
    """ Le fichier des ingredients /data/ingredients.json """
    ingredients_as_json = ""
    with open('../data/ingredients.json') as ingredients_file:
        for line in ingredients_file.readlines():
            ingredients_as_json += line

    ingredients = json.loads(ingredients_as_json)
    return ingredients

def _sanitize_ingredients(ingredients):
    ingredients_set = {}
    for ing in ingredients:
        cal_key = ing['CAL']
        ingredients_set[int(cal_key)] = ing['ITEM']

    return ingredients_set

def _compute_average_calories(calories, nbr_ingredients):
    avg = calories/nbr_ingredients
    return math.ceil(avg/10)*10
