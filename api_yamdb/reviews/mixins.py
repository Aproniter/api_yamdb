from rest_framework import mixins, viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class ModelMixinSet(CreateModelMixin, ListModelMixin,
                    DestroyModelMixin, GenericViewSet):
    """Стоит дать более понятное имя для класса, какие методы он реализует"""
    pass



class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass
