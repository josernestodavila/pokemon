from django.contrib import admin

from api.models import Move, Pokemon


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "power",
    )


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "height",
        "order",
        "power",
        "weight",
    )
    filter_horizontal = ("moves",)
