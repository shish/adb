from .meta import *
import logging

log = logging.getLogger(__name__)


@view_config(request_method="GET", route_name="cards", renderer="json")
def card_list(request):
    cards = DBSession.query(Card).all()
    return cards


@view_config(request_method="GET", route_name="card", renderer="json")
def card_read(request):
    try:
        card = DBSession.query(Card).get(request.matchdict["card_id"])
        return card
    except (NoResultFound, ValueError):
        raise NotFound()


@view_config(request_method="POST", route_name="cards", renderer="json")
def card_create(request):
    card = Card(
        user_id=request.user.user_id,
        code=request.json_body["code"],
        title=request.json_body["title"],
    )
    DBSession.add(card)
    DBSession.flush()
    log.info("Added card %(card_id)d", {"card_id": card.card_id})
    return TTResponse(status="ok", card_id=card.card_id)


@view_config(request_method="DELETE", route_name="card", renderer="json")
def card_delete(request):
    try:
        card_id = int(request.matchdict["card_id"])
        card = DBSession.query(Card).get(card_id)
        DBSession.delete(card)
        log.info("Deleted card %(card_id)d", {"card_id": card.card_id})
        return TTResponse(status="ok")
    except (NoResultFound, ValueError):
        raise NotFound()
