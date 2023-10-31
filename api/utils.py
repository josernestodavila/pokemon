from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from .models import Move, Pokemon


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


async def fetch(session, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()


async def get_or_create_pokemon(session, url: str) -> Pokemon:
    if url in cache:
        pokemon_id = cache.get(url)
        pokemon = await Pokemon.objects.filter(pk=pokemon_id).afirst()
    else:
        response = await fetch(session, url)
        pokemon_info = {
            "name": response["name"],
            "order": response["order"],
            "height": response["height"],
            "weight": response["weight"],
            "type": [pokemon_type["type"]["name"] for pokemon_type in response["types"]],
        }

        pokemon = await Pokemon.objects.filter(**pokemon_info).afirst()
        if not pokemon:
            pokemon = await Pokemon.objects.acreate(**pokemon_info)

        cache.set(url, pokemon.id, timeout=CACHE_TTL)

    return pokemon


async def get_or_create_move(session, url: str) -> Move:
    if url in cache:
        move_id = cache.get(url)
        move = await Move.objects.filter(id=move_id).afirst()
    else:
        response = await fetch(session, url)

        move_info = {
            "name": response["name"],
            "power": response["power"],
        }

        move = await Move.objects.filter(**move_info).afirst()
        if not move:
            move = await Move.objects.acreate(**move_info)

        cache.set(url, move.id)

    return move
