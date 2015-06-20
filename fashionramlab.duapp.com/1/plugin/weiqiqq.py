#! /usr/bin/env python
# -*- coding: utf-8 -*-

import meta
from db import log

__author__ = '锦峰'

class WeiqiqqPlugin(object):
    __metaclass__ = meta.PluginMetaClass
    name = 'weiqiqq入口插件'

    def response_message(self, request):
        import traceback
        try:
            import urllib2
            from hashlib import sha1

            url = self.settings['url']
            token = self.settings['token']
            timestamp = request.arguments.get('timestamp')[0]
            nonce = request.arguments.get('nonce')[0]
            signature = sha1((''.join(
                sorted([token, timestamp, nonce])
            ))).hexdigest()
            signature_query_str = '&'.join([
                'timestamp=%s' % timestamp,
                'nonce=%s' % nonce,
                'signature=%s' % signature,
            ])

            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            request = urllib2.Request('%s%s%s' % (url, ('?' if '?' not in url else '&'), signature_query_str))
            # log('%s%s%s' % (url, ('?' if '?' not in url else '&'), signature_query_str))
            # log(self.request.body)
            response = opener.open(request, self.request.body)
            return log(response.read())
        except:
            log(traceback.format_exc())

