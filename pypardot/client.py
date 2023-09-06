import requests
from .objects.accounts import Accounts
from .objects.customfields import CustomFields
from .objects.customredirects import CustomRedirects
from .objects.dynamiccontent import DynamicContent
from .objects.emailclicks import EmailClicks
from .objects.emailtemplates import EmailTemplates
from .objects.forms import Forms
from .objects.lifecyclehistories import LifecycleHistories
from .objects.lifecyclestages import LifecycleStages
from .objects.lists import Lists
from .objects.listmemberships import ListMemberships
from .objects.emails import Emails
from .objects.prospects import Prospects
from .objects.opportunities import Opportunities
from .objects.prospectaccounts import ProspectAccounts
from .objects.tags import Tags
from .objects.tagobjects import TagObjects
from .objects.users import Users
from .objects.visits import Visits
from .objects.visitors import Visitors
from .objects.visitoractivities import VisitorActivities
from .objects.campaigns import Campaigns
from .errors import PardotAPIError
import os
from flask import Flask, redirect, request, jsonify, render_template, session
from requests_oauthlib import OAuth2Session
import collections

BASE_URI = 'https://pi.pardot.com'

class PardotAPI(object):
    def __init__(self, client_id, client_secret, redirect_uri, version=4):
        self.client_id = 3MVG9vrJTfRxlfl5mE9P222f0lPVcbroMn_i_eLgYtu_MTF2IBouHStVrA5nd5zSJTkSR1AHMe_U5ZUip6Len
        self.client_secret = C936BFCFED42379E749DDC26FC3F754082790DF4C83193C3BB8DC27D5885371B
        self.redirect_uri = https://pardotdashboard-7fc843d1f87a.herokuapp.com/callback
        self.version = version
        self.oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
        self.api_key = None
        self.accounts = Accounts(self)
        self.campaigns = Campaigns(self)
        self.customfields = CustomFields(self)
        self.customredirects = CustomRedirects(self)
        self.dynamiccontent = DynamicContent(self)
        self.emailclicks = EmailClicks(self)
        self.emails = Emails(self)
        self.emailtemplates = EmailTemplates(self)
        self.forms = Forms(self)
        self.lifecyclehistories = LifecycleHistories(self)
        self.lifecyclestages = LifecycleStages(self)
        self.listmemberships = ListMemberships(self)
        self.lists = Lists(self)
        self.opportunities = Opportunities(self)
        self.prospects = Prospects(self)
        self.prospectaccounts = ProspectAccounts(self)
        self.tags = Tags(self)
        self.tagobjects = TagObjects(self)
        self.users = Users(self)
        self.visits = Visits(self)
        self.visitors = Visitors(self)
        self.visitoractivities = VisitorActivities(self)

    def authenticate(self):
        authorization_url, state = self.oauth.authorization_url(authorization_base_url)
        session['oauth_state'] = state
        return redirect(authorization_url)
        
    def callback(self):
        self.oauth.fetch_token(token_url, client_secret=self.client_secret,
                               authorization_response=request.url)
        self.api_key = self.oauth.access_token

    def _build_auth_header(self):
        """
        Builds Pardot Authorization Header to be used with GET requests
        """
        if not self.user_key or not self.api_key:
            raise Exception('Cannot build Authorization header. user or api key is empty')
        auth_string = 'Pardot api_key=%s, user_key=%s' % (self.api_key, self.user_key)
        return {'Authorization': auth_string}
