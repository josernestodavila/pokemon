import strawberry
from .models import Pokemon
from .types import PokemonType


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_pokemon(self, name: str, order: int, power: int, height: int, weight: int, type: str) -> PokemonType:
        pokemon = Pokemon(name=name, order=order, power=power, height=height, weight=weight, type=type)
        pokemon.save()

        return pokemon
