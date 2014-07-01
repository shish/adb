import os
from glob import glob
import sys
import transaction
import random
import requests
from bs4 import BeautifulSoup
import requests_cache
from collections import defaultdict
import os
requests_cache.install_cache(os.path.expanduser('~/.cache/adbweb'))

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    User,
    Deck, Link, Card,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)#, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    add_stub_data()


def add_stub_data():
    with transaction.manager:
        user = User(username="shish", email="webmaster@shishnet.org")
        user.set_password("test")
        DBSession.add(user)

        user = User(username="test", email="example@example.com")
        user.set_password("test")
        DBSession.add(user)

        fetch_serieses()
        fetch_trial()
        fetch_example()
        fetch_user()


def fetch_serieses():
    page = requests.get("http://littleakiba.com/tcg/weiss-schwarz/").content
    soup = BeautifulSoup(page)

    fetch_series(46)
#    for link in soup.find_all('a'):
#        if 'series_id' in link["href"]:
#            series_id = int(link["href"].split("=")[1])
#            fetch_series(series_id)


def fetch_series(series_id):
    page = requests.get("http://littleakiba.com/tcg/weiss-schwarz/card.php?series_id=%d" % series_id).content
    soup = BeautifulSoup(page)

    deck_title = soup.h2.contents[0]
    print "Fetching deck %d:%r" % (series_id, deck_title)
    d = Deck(
        type="series",
        title=deck_title,
    )
    DBSession.add(d)

    for link in soup.find_all('a'):
        if 'card_id' in link["href"]:
            card_id = int(link["href"].split("=")[1])
            c = fetch_card(card_id)
            DBSession.add(Link(deck=d, card=c, number=1))

    DBSession.flush()


def fetch_card(card_id):
    page = requests.get("http://littleakiba.com/tcg/weiss-schwarz/card.php?card_id=%d" % card_id).content
    soup = BeautifulSoup(page)

    card_code = soup.find_all('small')[0].contents[0].split(' ')[0]
    mixed_title = soup.find("h4").prettify()
    card_name_jp, br, card_name_en = mixed_title.partition("<br/>")
    card_name_jp = BeautifulSoup(card_name_jp).text.strip()
    card_name_en = BeautifulSoup(card_name_en).text.strip() or None

    print "Fetching card %d:%r (%r / %r)" % (card_id, card_code, card_name_en, card_name_jp)

    c = Card(
        title_jp=card_name_jp,
        title_en=card_name_en,
        code=card_code,
    )
    DBSession.add(c)
    return c


def get_card(code):
    return DBSession.query(Card).filter(Card.code == code.upper()).first()


def fetch_trial():
    for filename in glob("data/trial-*"):
        d = Deck(
            title=filename.replace("data/trial-", "").replace(".txt", ""),
            type="trial",
        )
        DBSession.add(d)
        for line in file(filename):
            code, number = line.strip().split(": ")
            c = get_card(code)
            d.cards.append(Link(deck=d, card=c, number=int(number)))
        DBSession.flush()


def fetch_example():
    for filename in glob("data/ex-*"):
        d = Deck(
            title=filename.replace("data/ex-", "").replace(".txt", "").replace("-", " "),
            type="example",
        )
        DBSession.add(d)
        for line in file(filename):
            code, number, name = line.strip().split(": ")
            c = get_card(code.replace("e", ""))
            d.cards.append(Link(deck=d, card=c, number=int(number)))
        DBSession.flush()


def fetch_user():
    for filename in glob("data/user-*"):
        d = Deck(
            title=filename.replace("data/user-", "").replace(".txt", "") + "'s Cards",
            type="user",
        )
        DBSession.add(d)
        for line in file(filename):
            code, number = line.strip().split(": ")
            c = get_card(code.replace("e", ""))
            d.cards.append(Link(deck=d, card=c, number=int(number)))
        DBSession.flush()


def stub_cards():
    d = Deck(title=u"Test Deck")
    DBSession.add(d)

    for n in range(0, 100):
        #print "Adding %d" % n
        c = Card(
            title=u"Test Card %d" % n,
            code="TC/%03d" % n,
        )
        DBSession.add(c)

        l = Link(
            deck=d,
            card=c,
            number=random.randint(1, 4)
        )
        DBSession.add(l)
