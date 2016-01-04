#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import base64
import uuid
import random
import hashlib
import json

if sys.version_info > (3, 0):
    from urllib.request import build_opener, HTTPCookieProcessor, Request
    from http.cookiejar import CookieJar, Cookie
    from urllib.error import HTTPError
else:
    from urllib2 import build_opener, HTTPCookieProcessor, Request, HTTPError
    from cookielib import CookieJar, Cookie

SWEDBANK = "swedbank"
SPARBANKEN = "sparbanken"
SWEDBANK_UNG = "swedbank_ung"
SPARBANKEN_UNG = "sparbanken_ung"
SWEDBANK_FORETAG = "swedbank_foretag"
SPARBANKEN_FORETAG = "sparbanken_foretag"


class Swedbank(object):
    BANKS = {
        SWEDBANK: {
            "id": "HithYAGrzi8fu73j",
            "u-a": "SwedbankMOBPrivateIOS/3.9.0_(iOS;_8.0.2)_Apple/iPhone5,2"
        },
        SPARBANKEN: {
            "id": "9iZSu74jfDFaTdPd",
            "u-a": "SavingbankMOBPrivateIOS/3.9.0_(iOS;_8.0.2)_Apple/iPhone5,2"
        },
        SWEDBANK_UNG: {
            "id": "IV4Wrt2VZtyYjfpW",
            "u-a": "SwedbankMOBYouthIOS/1.6.0_(iOS;_8.0.2)_Apple/iPhone5,2"
        },
        SPARBANKEN_UNG: {
            "id": "BrGkZQR89rEbFwnj",
            "u-a": "SavingbankMOBYouthIOS/1.6.0_(iOS;_8.0.2)_Apple/iPhone5,2"
        },
        SWEDBANK_FORETAG: {
            "id": "v0RVbFGKMXz7U4Eb",
            "u-a": "SwedbankMOBCorporateIOS/1.5.0_(iOS;_8.0.2)_Apple/iPhone5,2"
        },
        SPARBANKEN_FORETAG: {
            "id": "JPf1VxiskNdFSclr",
            "u-a": "SavingbankMOBCorporateIOS/1.5.0_(iOS;_8.0.2)_Apple/iPhone5,2"
        }
    }

    def __init__(self):
        """ Set default stuff """
        self.data = ""
        self.pch = None
        self.authkey = None
        self.cj = CookieJar()
        self.profile = None
        self.account = None
        self.useragent = None
        self.bankid = None

    def get_authkey(self):
        if self.authkey is None:
            data = "%s:%s" % (self.bankid, uuid.uuid4())
            self.authkey = base64.b64encode(data.encode("utf-8")).decode(
                    "utf-8")
        return self.authkey

    def get_dsid(self):
        data = "%s%s" % (random.randint(0, 99999), random.randint(0, 99999))
        hashvalue = hashlib.sha1(data.encode("utf-8")).hexdigest()[:8]
        dsid = "%s%s" % (hashvalue[:4], hashvalue[4:].upper())
        random.shuffle(list(dsid))
        return ''.join(dsid)

    def request(self, url, post=None, method="GET"):
        """ Make the request"""
        dsid = self.get_dsid()
        baseurl = "https://auth.api.swedbank.se/TDE_DAP_Portal_REST_WEB/api/v1/%s?dsid=%s" % (
            url, dsid)

        if self.pch is None:
            self.pch = build_opener(HTTPCookieProcessor(self.cj))

        if post:
            post = bytearray(post, "utf-8")
            request = Request(baseurl, data=post)
            request.add_header("Content-Type", "application/json")
        else:
            request = Request(baseurl)

        request.add_header("User-Agent", self.useragent)
        request.add_header("Authorization", self.get_authkey())
        request.add_header("Accept", "*/*")
        request.add_header("Accept-Language", "sv-se")
        request.add_header("Connection", "keep-alive")
        request.add_header("Proxy-Connection", "keep-alive")
        self.cj.set_cookie(
                Cookie(version=0, name='dsid', value=dsid, port=None,
                       port_specified=False, domain='.api.swedbank.se',
                       domain_specified=False, domain_initial_dot=False,
                       path='/',
                       path_specified=True, secure=False, expires=None,
                       discard=True, comment=None, comment_url=None,
                       rest={'HttpsOnly': None}, rfc2109=False))
        request.get_method = lambda: method
        tmp = self.pch.open(request)
        self.data = tmp.read().decode("utf8")

    def login(self, user, passwd, bank):
        """ Login """
        if bank not in self.BANKS:
            print("Can't find that bank.")
            return False
        self.useragent = self.BANKS[bank]["u-a"]
        self.bankid = self.BANKS[bank]["id"]
        login = json.dumps(
                {"userId": user, "password": passwd, "useEasyLogin": False,
                 "generateEasyLoginId": False})
        try:
            self.request("identification/personalcode", post=login,
                         method="POST")
        except HTTPError as e:
            error = json.loads(e.read().decode("utf8"))
            print(error["errorMessages"]["fields"][0]["message"])
            return False
        try:
            self.request("profile/")
        except HTTPError as e:
            error = json.loads(e.read().decode("utf8"))
            print(error["errorMessages"]["general"][0]["message"])
            return False

        profile = json.loads(self.getdata())
        if len(profile["banks"]) == 0:
            print("Using wrong bank? Can't find any bank info.")
            return False
        try:
            self.profile = profile["banks"][0]["privateProfile"]["id"]
        except KeyError:
            self.profile = profile['banks'][0]['corporateProfiles'][0]["id"]
        try:
            self.request("profile/%s" % self.profile, method="POST")
        except HTTPError as e:
            error = json.loads(e.read().decode("utf8"))
            print(error["errorMessages"]["general"][0]["message"])
            return False

        return True

    def accounts(self):
        """ Accounts """
        try:
            self.request("engagement/overview")
        except HTTPError as e:
            error = json.loads(e.read().decode("utf8"))
            print(error["errorMessages"]["general"][0]["message"])
            return
        overview = json.loads(self.getdata())
        overviewl = reversed(list(overview))
        for i in overviewl:
            if len(overview[i]) > 0:
                for n in overview[i]:
                    if self.account is None and "id" in n:
                        self.account = n["id"]
                    if n.get('balance'):
                        print("%s: %s" % (n["name"], n["balance"]))
                    elif n.get('availableAmount', None):
                        print("%s: %s" % (n["name"], n["availableAmount"]))

                    else:
                        print(n)

    def history(self):
        """ History """
        print("Transactions:")
        try:
            self.request("engagement/transactions/%s" % self.account)
        except HTTPError as e:
            error = json.loads(e.read().decode("utf8"))
            print(error["errorMessages"]["general"][0]["message"])
            return

        transactions = json.loads(self.getdata())["transactions"]
        for i in transactions:
            print("%s %s %s" % (i["date"], i["description"], i["amount"]))

    @staticmethod
    def banks():
        ret = ""
        for i in sorted(Swedbank.BANKS.keys()):
            if i == "swedbank":
                ret += "\n%s (default)" % i
            else:
                ret += "\n%s" % i
        return ret

    def getdata(self):
        """ Get the response data """
        return self.data
