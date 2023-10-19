from django.db import models


class Move(models.Model):
    name = models.CharField(max_length=50)
    power = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = "Move"
        verbose_name_plural = "Moves"

    def __str__(self) -> str:
        return self.name


class Pokemon(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()
    power = models.IntegerField(default=0, null=True, blank=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    type = models.CharField(max_length=50)
    moves = models.ManyToManyField(Move, related_name="pokemons")

    class Meta:
        verbose_name = "Pokemon"
        verbose_name_plural = "Pokemons"

    def __str__(self) -> str:
        return self.name
