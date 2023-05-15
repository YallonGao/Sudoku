from django.db import models


class Sudoku(models.Model):
    title = models.CharField(max_length=100)
    step = models.CharField(max_length=4)
    grids = models.CharField(max_length=729)

    objects = models.Manager()

    class Meta:
        db_table = 'd_sudoku'
