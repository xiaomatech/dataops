#!/usr/bin/env python

from resource_management.core.logger import Logger
from resource_management.core.source import Template
from atlas_api import AtlasRequestHandler
import json


class AtlasModelChanges:
    def __init__(self, atlas_url_list, username, password):
        self.atlas_request_handler = AtlasRequestHandler(atlas_url_list, username, password)

    def is_model_registered(self):
        api_endpoint = "/api/atlas/v2/types/structdef/name/dss_hive_column_profile_data"
        response_code, response_content = self.atlas_request_handler.handle_request(api_endpoint)
        if response_code == 200:
            return True
        else:
            return None

    def add_hive_profile_types(self):
        hive_profile_types_json = Template("hive_profiler_model.json").get_content()
        api_endpoint = "/api/atlas/v2/types/typedefs"
        Logger.info("Attempting to register Hive profile types with Atlas server")
        Logger.debug("Payload for the profiler model registration request => {0}".format(hive_profile_types_json))
        response_code, response_content = self.atlas_request_handler.handle_request(api_endpoint,
                                                                                    hive_profile_types_json)
        if response_code == 200:
            Logger.info("Profile types registered successfully")
            Logger.debug("Received content from Atlas server {0}".format(response_content))

        elif response_code is not None:
            Logger.error("Error during profile type registration. Http status code - {0}. {1}".
                         format(response_code, response_content))

        else:
            Logger.error("No Atlas URL able to process the request successfully")

    def get_entity_def(self, name):
        api_endpoint = "/api/atlas/v2/types/entitydef/name/{}".format(name)
        response_code, response_content = self.atlas_request_handler.handle_request(api_endpoint)
        if response_code == 200:
            Logger.debug("Received content from Atlas server {0}".format(response_content))

        elif response_code is not None:
            Logger.error("Error during retrieving entity definition. Http status code - {0}. {1}".
                         format(response_code, response_content))
        else:
            Logger.error("No Atlas URL able to process the request successfully")
        return response_content

    def update_hive_types(self):
        column_profiler_def = '{ "name": "profileData", "typeName": "dss_hive_column_profile_data","cardinality": "SINGLE","isIndexable": false,"isOptional": true,"isUnique": false}'
        table_profiler_def = '{"name":"profileData","typeName":"dss_hive_table_profile_data","cardinality":"SINGLE","isIndexable":false,"isOptional":true,"isUnique":false}'
        column_profiler_def_dict = json.loads(column_profiler_def)
        table_profiler_def_dict = json.loads(table_profiler_def)
        hive_column = json.loads(self.get_entity_def("hive_column"))
        hive_table = json.loads(self.get_entity_def("hive_table"))
        hive_column['attributeDefs'].append(column_profiler_def_dict)
        hive_table['attributeDefs'].append(table_profiler_def_dict)
        type_update = {'enumDefs': [], 'classificationDefs': [], 'entityDefs': [hive_column, hive_table],
                       'relationshipDefs': [], 'structDefs': []}
        type_update_request = json.dumps(type_update)
        api_endpoint = "/api/atlas/v2/types/typedefs"
        Logger.info("Attempting to update existing Hive types with profile attributes with Atlas server")
        Logger.debug("Payload for the Hive model update request => {0}".format(type_update_request))
        response_code, response_content = self.atlas_request_handler. \
            handle_request(api_endpoint, type_update_request, True)

        if response_code == 200:
            Logger.info("Hive types updated with profile attributes successfully")
            Logger.debug("Received content from Atlas server {0}".format(response_content))

        elif response_code is not None:
            Logger.error("Error while updating the hive_table and hive_column types with profile data "
                         "attribute. Http Status Code - {0}. {1}".format(response_code, response_content))

        else:
            Logger.error("No Atlas URL able to process the request successfully")
