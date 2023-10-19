import strawberry

from .models import Move, Pokemon
from .types import MoveType, PokemonType
from .mutations import Mutation


@strawberry.type
class Query:
    @strawberry.field
    def pokemons(self) -> list[PokemonType]:
        return Pokemon.objects.all()

    @strawberry.field
    def moves(self) -> list[MoveType]:
        return Move.objects.all()


schema = strawberry.Schema(query=Query, mutation=Mutation)
