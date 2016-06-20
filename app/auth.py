from flask import url_for, current_app, redirect, request, jsonify
from rauth import OAuth2Service
import json


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.config = current_app.config['OAUTH_PROVIDERS'][provider_name]['conf']
        self.service = OAuth2Service(
            name=self.provider_name,
            client_id=self.config.get('consumer_key'),
            client_secret=self.config.get('consumer_secret'),
            authorize_url=self.config.get('authorize_url'),
            access_token_url=self.config.get('access_token_url'),
            base_url=self.config.get('base_url')
        )

    def get_callback_url(self):
        return url_for('users.callback', provider_name=self.provider_name, _external=True)

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope=self.config.get('request_token_params').get('scope'),
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return jsonify(request.args)
        data = {'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()}
        if 'decoder' in self.config:
            oauth_session = self.service.get_auth_session(data=data,
                                                          decoder=self.decoder)
        else:
            oauth_session = self.service.get_auth_session(data=data)
        return oauth_session.get('').json()

    def decoder(self, r):
        decoder_name = self.config.get('decoder')
        if decoder_name == 'bjson':
            return json.loads(r.decode())
        elif decoder_name == 'json':
            return json.loads(r)
        else:
            return None
