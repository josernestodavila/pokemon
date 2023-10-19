import strawberry


@strawberry.type
class PokemonType:
    name: str
    order: int
    power: int = 0
    height: int
    weight: int
    type: str


@strawberry.type
class MoveType:
    name: str
    power: int | None = 0
