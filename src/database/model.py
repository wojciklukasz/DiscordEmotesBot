from pony import orm
from datetime import datetime

db = orm.Database()


class Emote(db.Entity):
    name = orm.Required(str, unique=True)
    guild_id = orm.Required(str)
    uses = orm.Required(int)
    last_used = orm.Required(datetime)


@orm.db_session
def add_emote(emote, server):
    print(f'Adding new emote: {emote} in server {server} ID: {server.id}')
    e = Emote(name=emote, guild_id=str(server.id), uses=1, last_used=datetime.now())
    return e


@orm.db_session
def increase_count(emote, server):
    e = Emote.get(name=emote, guild_id=str(server.id))
    if e is None:
        add_emote(emote, server)
        return

    print(f'Increasing uses of {emote}')
    e.uses += 1


@orm.db_session
def get_count(emote, server):
    e = Emote.get(name=emote, guild_id=str(server.id))
    if e is None:
        return 0

    return e.uses


def connect():
    db.bind(provider='sqlite', filename='db.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
