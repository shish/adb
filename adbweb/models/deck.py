from .meta import *


class Card(Base):
    __tablename__ = "card"
    card_id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    title_jp = Column(Unicode, nullable=False)
    title_en = Column(Unicode, nullable=True)
    #description = Column(Unicode, nullable=False, default=u"")

    def __json__(self, request):
        d = {
            "card_id": self.card_id,
            "code": self.code,
            "title": self.title_en or self.title_jp,
            "title_en": self.title_en,
            "title_jp": self.title_jp,
        }
        return d


class Deck(Base):
    __tablename__ = "deck"
    deck_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    type = Column(Unicode, nullable=False, default=u"user")
    title = Column(Unicode, nullable=False)

    def __json__(self, request):
        d = {
            "deck_id": self.deck_id,
            "title": self.title,
            "type": self.type,
        }
        if "deck_id" in request.matchdict:
            d.update({
                "cards": self.cards,
            })
        return d


class Link(Base):
    __tablename__ = "link"
    deck_id = Column(Integer, ForeignKey("deck.deck_id"), primary_key=True)
    number = Column(Integer, nullable=False)
    card_id = Column(Integer, ForeignKey("card.card_id"), primary_key=True)

    deck = relationship(Deck, backref=backref("cards", cascade="all, delete-orphan"))
    card = relationship(Card, backref=backref("decks", cascade="all, delete-orphan"))

    def __json__(self, request):
        d = {
            "number": self.number,
            "card": self.card,
        }
        return d
