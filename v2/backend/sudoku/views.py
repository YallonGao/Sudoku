from django.shortcuts import render
from rest_framework import viewsets
from .models import Sudoku
from .serializers import SudokuSerializer


class StepViewSet(viewsets.ModelViewSet):
    queryset = Sudoku.objects.all().order_by('step')
    serializer_class = SudokuSerializer


def clear_all():
    pass


def add_data():
    pass
