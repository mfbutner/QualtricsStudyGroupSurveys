from requests_toolbelt import sessions
from typing import Any
from .oath_information import OathInformation


class QualtricsConnection:
    def __init__(self, data_center: str,
                 credentials: str | OathInformation):
        """
        Create a connection to the Qualtrics API servers
        :param data_center: url to the datacenter, ex: https://iad1.qualtrics.com/
        :param credentials: if a string, it should be the api token otherwise the oath credentials need to be supplied
        """

        # these are the headers that all Qualtrics APIS have in common
        common_headers = {"Accept": "application/json"}

        # TODO check data_center is properly formatted
        if not data_center.endswith('/'):
            data_center += '/'
        self.connection = sessions.BaseUrlSession(base_url=data_center)

        match credentials:
            case OathInformation():
                # TODO: check into https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html for easier oauth handling
                self.oath_info = credentials  # this needs to be kept around in case the oauth token expires
                oath_token_request = self.connection.post('/oauth2/token',
                                                          data={'grant_type': 'client_credentials',
                                                                'scope': self.oath_info.scope
                                                                },
                                                          auth=(self.oath_info.client_id, self.oath_info.client_secret))
                oath_token_request.raise_for_status()
                values = oath_token_request.json()
                access_token = values['access_token']
                common_headers['Authorization'] = f'Bearer {access_token}'
            case str():
                common_headers['X-API-TOKEN'] = credentials
                self.oath_info = None
            case wrong_type:
                 raise TypeError(f'credentials must be one of str | OathInformation but {type(wrong_type)} was entered')

        self.connection.headers.update(common_headers)

    def list_surveys(self) -> dict[str, Any]:
        endpoint = "/API/v3/surveys"

        headers = {

        }

        response = self.connection.get(endpoint, headers=headers)

        return response.json()['result']

    def get_survey(self, survey_id: str) -> dict[str, Any]:
        endpoint = f'/API/v3/surveys/{survey_id}'
        headers = {
        }

        response = self.connection.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()['result']

    def who_am_i(self) -> dict[str, Any]:
        endpoint = "/API/v3/whoami"

        headers = {

        }

        response = self.connection.get(endpoint, headers=headers)

        return response.json()['result']
