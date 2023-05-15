from rest_framework import serializers
from .models import Sudoku


class SudokuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sudoku
        fields = "__all__"
