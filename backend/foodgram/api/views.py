from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework import filters, mixins

from recipes import models
from api import serializers
from .filters import RecipeFilter
from django.db.models import Sum


class TagView(mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              viewsets.GenericViewSet):
    permission_classes = (AllowAny, )
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class IngredientsView(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = models.Ingredient.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.IngredientSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["^name", ]
    pagination_class = None


class RecipeView(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    permissions = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filter_class = RecipeFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST" or method == "PATCH":
            return serializers.CreateRecipeSerializer
        return serializers.ShowRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class FavoriteView(APIView):
    permissions = [IsAuthenticatedOrReadOnly, ]

    @action(
        methods=[
            "post",
        ],
        detail=True,
    )
    def post(self, request, recipe_id):
        user = request.user
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }
        if models.Favorite.objects.filter(
            user=user, recipe__id=recipe_id
        ).exists():
            return Response(
                {"Ошибка": "рецепт уже есть в избранном"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = serializers.FavoriteSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=[
            "DELETE",
        ],
        detail=True,
    )
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(models.Recipe, id=recipe_id)
        if not models.Favorite.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        models.Favorite.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = None

    @action(
        methods=[
            "post"
        ],
        detail=True,
    )
    def post(self, request, recipe_id):
        user = request.user
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }
        if models.ShoppingCart.objects.filter(
                user=user, recipe__id=recipe_id
        ).exists():
            return Response(
                {"Ошибка": "Уже есть в корзине"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = serializers.ShoppingCartSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        method=[
            "delete",
        ],
        detail=True,
    )
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(models.Recipe, id=recipe_id)
        if not models.ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        models.ShoppingCart.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def download_shopping_cart(request):
    """
    Формирует txt файл со списком
    покупок ингредиентов из ShoppingCart
    """
    ingredients = (
        models.IngredientInRecipe.objects
        .filter(recipe__shopping_cart__user=request.user)
        .values('ingredient')
        .annotate(total_amount=Sum('amount'))
        .values_list(
            'ingredient__name', 'total_amount',
            'ingredient__measurement_unit'
        )
    )
    wishlist = []
    [wishlist.append(
        '{} - {} {}.'.format(*ingredient)) for ingredient in ingredients]
    txtfile = HttpResponse(
        'Cписок покупок:\n' + '\n'.join(wishlist),
        content_type='text/plain'
    )
    txtfile['Content-Disposition'] = ('attachment; filename=Shoping list')
    return txtfile
