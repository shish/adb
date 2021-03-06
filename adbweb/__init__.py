from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid, authenticated_userid
from pyramid.security import has_permission

from sqlalchemy import engine_from_config

import locale
import logging

log = logging.getLogger(__name__)


from .models import (
    DBSession,
    Base,
    )


def configure_routes(config):
    config.add_static_view('static', 'static', cache_max_age=0)

    config.add_route('index', '/')

    config.add_route('users', '/user')
    config.add_route('user', '/user/{user_id}')

    config.add_route('decks', '/deck')
    config.add_route('deck', '/deck/{deck_id}')

    config.add_route('cards', '/card')
    config.add_route('card', '/card/{card_id}')

    config.add_route('sessions', '/session')
    config.add_route('session', '/session/{session_id}')

    config.scan("adbweb.views")


def configure_templates(config):
    pass


def configure_locale(config, settings):
    loc = 'en_GB.UTF-8'
    try:
        locale.setlocale(locale.LC_ALL, loc)
    except locale.Error:
        # locale doesn't work on windows?
        log.error("Error setting locale to %r", loc)


def configure_cache(config, settings):
    try:
        cache.fast.configure_from_config(settings, "cache.fast.")
        cache.slow.configure_from_config(settings, "cache.slow.")
    except Exception:
        pass


def configure_auth(config):
    def principals(username, request):
        u = User.by_username(username)
        return ["u:"+u.username, ]#"g:"+u.category]
    config.set_authentication_policy(AuthTktAuthenticationPolicy('tuttuuttuttututu?', callback=principals, hashalg='sha512'))
    config.set_authorization_policy(ACLAuthorizationPolicy())


def configure_user(config):
    def user(request):
        from adbweb.models import User
        un = authenticated_userid(request)
        u = User.by_username(un)
        if not u:
            u = User.by_username("shish")
        if not u:
            raise Exception("Anonymous is missing")
        u.ip = "127.0.0.9"  # request.headers["REMOTE_ADDR"]
        return u
    config.add_request_method(user, property=True, reify=True)


def main(global_config, **settings):  # pragma: no cover
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    configure_routes(config)
    configure_templates(config)
    configure_locale(config, settings)
    configure_cache(config, settings)
    configure_auth(config)
    configure_user(config)

    return config.make_wsgi_app()
