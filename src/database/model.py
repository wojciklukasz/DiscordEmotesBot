from pony import orm
from datetime import datetime


db = orm.Database()


class Emote(db.Entity):
    name = orm.Required(str, unique=True)
    guild_id = orm.Required(str)
    uses_emote = orm.Required(int)
    uses_reaction = orm.Required(int)
    last_used = orm.Required(datetime)


@orm.db_session
def add_emote(emote, server):
    print(f'Adding new emote: {emote} in server {server} ID: {server.id}')
    e = Emote(name=emote, guild_id=str(server.id), uses_emote=0, uses_reaction=0, last_used=datetime.now())
    return e


@orm.db_session
def increase_count_emote(emote, server):
    e = Emote.get(name=emote, guild_id=str(server.id))
    if e is None:
        e = add_emote(emote, server)

    print(f'Increasing uses as emote of {emote} in server {server} ID: {server.id}')
    e.uses_emote += 1


@orm.db_session
def increase_count_reaction(emote, server):
    e = Emote.get(name=emote, guild_id=str(server.id))
    if e is None:
        e = add_emote(emote, server)

    print(f'Increasing uses as reaction of {emote} in server {server} ID: {server.id}')
    e.uses_reaction += 1


@orm.db_session
def get_count_emote(emote, server):
    e = Emote.get(name=emote, guild_id=str(server.id))
    if e is None:
        return 0

    return e.uses_emote


@orm.db_session
def get_count_reaction(emote, server):
    e = Emote.get(name=emote, guild_id=str(server.id))
    if e is None:
        return 0

    return e.uses_reaction


@orm.db_session
def delete_emote(emote, server):
    e = Emote.get(name=emote, guild_id=str(server.id))
    if e is None:
        print(f'Trying to delete an emote which is not in a database! Please use historical data.')
    e.delete()
    print(f'Deleted {emote} from server {server} ID: {server.id}')


@orm.db_session
def decrease_count_emote(emote, server):
    e = Emote.get(name=emote, guild_id=str(server.id))

    print(f'Decreasing uses as emote of {emote} in server {server} ID: {server.id}')
    e.uses_emote -= 1

    if e.uses_emote == 0 and e.uses_reaction == 0:
        delete_emote(emote, server)


@orm.db_session
def decrease_count_reaction(emote, server):
    e = Emote.get(name=emote, guild_id=str(server.id))

    print(f'Decreasing uses as emote of {emote} in server {server} ID: {server.id}')
    e.uses_reaction -= 1

    if e.uses_emote == 0 and e.uses_reaction == 0:
        delete_emote(emote, server)


def connect():
    db.bind(provider='sqlite', filename='db.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
