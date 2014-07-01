from pyramid import testing

from adbweb.tests import AdbWebTest
from adbweb import (
    configure_routes,
    configure_templates,
    configure_locale,
    configure_cache,
    configure_auth,
    configure_user,
)


class TestMain(AdbWebTest):
    def test_configure_routes(self):
        configure_routes(self.config)

    def test_configure_templates(self):
        configure_templates(self.config)

    def test_configure_locale(self):
        configure_locale(self.config, {})

    def test_configure_cache(self):
        configure_cache(self.config, {})

#    def test_configure_auth(self):
#        configure_auth(self.config)

    def test_configure_user(self):
        configure_user(self.config)
