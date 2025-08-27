import json
from os import PathLike
import pathlib
from venv import create

from requests_toolbelt import sessions
from typing import Any
from .oath_information import OathInformation
from .question import Question
from .block import Block


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
            # purposefully empty
        }

        response = self.connection.get(endpoint, headers=headers)

        return response.json()['result']

    def get_survey(self, survey_id: str) -> dict[str, Any]:
        endpoint = f'/API/v3/survey-definitions/{survey_id}'
        return self._url_only_get(endpoint)

    def who_am_i(self) -> dict[str, Any]:
        endpoint = "/API/v3/whoami"

        return self._url_only_get(endpoint)

    def get_questions(self, survey_id: str) -> dict[str, Any]:
        endpoint = f'/API/v3/survey-definitions/{survey_id}/questions'
        return self._url_only_get(endpoint)

    def get_blocks(self, survey_id: str) -> list[dict[str, Any]]:
        endpoint = '/API/v3/survey-definitions/{survey_id}/blocks/{block_id}'
        headers = {
            # purposefully empty
        }
        survey = self.get_survey(survey_id)
        blocks = []
        for block_id in survey['Blocks']:
            block = self.connection.get(endpoint.format(survey_id=survey_id, block_id=block_id), headers=headers)
            block.raise_for_status()
            blocks.append(block.json()['result'])
        return blocks

    def get_flow(self, survey_id: str) -> dict[str, Any]:
        endpoint = f'/API/v3/survey-definitions/{survey_id}/flow'
        return self._url_only_get(endpoint)

    def get_survey_options(self, survey_id: str):
        endpoint = f'/API/v3/survey-definitions/{survey_id}/options'
        return self._url_only_get(endpoint)

    def download_all_survey_attributes(self, survey_id: str, dir_path: str,
                                       create_dir_if_missing: bool = False,
                                       create_parents: bool = False) -> None:
        """
        Downloads the survey and its questions, options, flow, and blocks to the specified directory
        :param survey_id: the survey's id
        :param dir_path: the path to the directory to download all the json files to
        :param create_dir_if_missing: create the directory if missing
        :param create_parents: if the directory is missing, should all missing directories along the path
        be created?
        :return:
        """
        dir_path = pathlib.Path(str(dir_path))
        if create_dir_if_missing and not dir_path.exists():
            dir_path.mkdir(parents=create_parents, exist_ok=True)

        locations_and_generators = {
            'survey.json': lambda: self.get_survey(survey_id),
            'questions.json': lambda: self.get_questions(survey_id),
            'survey_options.json': lambda: self.get_survey_options(survey_id),
            'flow.json': lambda: self.get_flow(survey_id),
            'blocks.json': lambda: self.get_blocks(survey_id)
        }
        for location, generator in locations_and_generators.items():
            with open(dir_path / location, 'w') as dest_file:
                json.dump(generator(), dest_file, indent=2)

    def _url_only_get(self, endpoint):
        headers = {
            # purposefully empty
        }
        response = self.connection.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()['result']
    
    def create_question(self, survey_id:str, question:Question) -> dict[str, Any]:
        question_id = question.get_ID()
        headers = {
            # purposefully empty
        }
        params = {
            "blockId": question._block_ID
        }
        endpoint = f'/API/v3/survey-definitions/{survey_id}/questions'
        response = self.connection.post(endpoint, json=question.generate_json(), headers=headers, params=params)
        print(response.text)
        return response.json()
    
    def create_block(self, survey_id:str, block:Block) -> dict[str, Any]:
        headers = {
            # purposefully empty
        }
        endpoint = f'/API/v3/survey-definitions/{survey_id}/blocks'
        response = self.connection.post(endpoint, json=block.generate_json(), headers=headers)
        print(response.text)
        return response.json()
