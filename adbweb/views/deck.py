from .meta import *
import logging

log = logging.getLogger(__name__)


@view_config(request_method="GET", route_name="decks", renderer="json")
def deck_list(request):
    decks = DBSession.query(Deck).all()
    return decks


@view_config(request_method="GET", route_name="deck", renderer="json")
def deck_read(request):
    try:
        deck = DBSession.query(Deck).filter(Deck.deck_id==request.matchdict["deck_id"]).one()
        return deck
    except (NoResultFound, ValueError):
        raise NotFound()
    except Exception:
        log.exception("Moo")
        raise


@view_config(request_method="POST", route_name="decks", renderer="json")
def deck_create(request):
    deck = Deck(
        title=request.json_body["title"]
    )
    DBSession.add(deck)
    DBSession.flush()
    log.info("Added deck %(deck_id)d", {"deck_id": deck.deck_id})
    return TTResponse(status="ok", deck_id=deck.deck_id)


@view_config(request_method="DELETE", route_name="deck", renderer="json")
def deck_delete(request):
    try:
        deck_id = int(request.matchdict["deck_id"])
        deck = DBSession.query(Deck).filter(Deck.deck_id==deck_id).one()
        DBSession.delete(deck)
        log.info("Deleted deck %(deck_id)d", {"deck_id": deck.deck_id})
        return TTResponse(status="ok")
    except (NoResultFound, ValueError):
        raise NotFound()
