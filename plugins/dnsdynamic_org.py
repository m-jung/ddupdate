"""
ddupdate plugin updating data on dnsdynamic.org.

See: ddupdate(8)
See: https://www.dnsdynamic.org/api.php

"""

from ddupdate.ddplugin import ServicePlugin, ServiceError
from ddupdate.ddplugin import http_basic_auth_setup, get_response


class DynamicDnsPlugin(ServicePlugin):
    """
    Update a dns entry on dnsdynamic.org.

    Does not support setting arbitrary ip address (despite documentation)
    The ip-disabled plugin should be used, and the address set is as seen
    from dns-dynamic.org.

    netrc: Use a line like
        machine www.dnsdynamic.org login <username>  password <password>

    Options:
        none
    """

    _name = 'dnsdynamic.org'
    _oneliner = 'Updates on http://dnsdynamic.org/'
    _url = 'https://www.dnsdynamic.org/api?hostname={0}'

    def register(self, log, hostname, ip, options):
        """Implement ServicePlugin.register."""
        url = self._url.format(hostname)
        http_basic_auth_setup(url, 'www.dnsdynamic.org')
        html = get_response(log, url, self._socket_to)
        if html.split()[0] not in ['nochg', 'good']:
            raise ServiceError("Bad update reply: " + html)