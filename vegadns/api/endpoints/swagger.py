import os
import sys
import json
import urlparse

from flask import Flask, request

from vegadns.api import endpoint
from vegadns.api.endpoints import AbstractEndpoint


@endpoint
class Swagger(AbstractEndpoint):
    auth_required = False
    route = '/swagger'

    def get(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        swagger_file = this_dir + "/../../../swagger/vegadns.swagger.json"

        with open(swagger_file) as template:
            contents = template.read()

        body = json.loads(contents)
        baseUrl = request.args.get('baseUrl', None)

        if baseUrl is not None:
            baseUrl = baseUrl.rstrip("/")
            parsed = urlparse.urlparse(baseUrl)
            body['host'] = parsed.netloc
            body['schemes'] = [parsed.scheme]
            body['securityDefinitions']['BearerToken']['tokenUrl'] = (
                baseUrl + "/1.0/token"
            )

        return body
