from recipes.models import Ingredient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        with open("/app/foodgram/data/ingredients.csv") as f:
            for line in f:
                ing = line.split(',')
                Ingredient.objects.get_or_create(
                    name=ing[0],
                    measurement_unit=ing[1])
