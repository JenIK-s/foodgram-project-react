import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    with open(os.path.join(settings.DATA_ROOT, 'ingredients.json'), 'r') as file:
        data = json.load(file)
        for ingredient in data.items():
            Ingredient.objects.create(
                name=ingredient["name"],
                measurement_unit=ingredient[
                "measurement_unit"]
            )