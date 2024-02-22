#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from includes import *

class UserConfig(object):
    def __init__(self, logger):
        super()
        if logger is not None:
            self.logger = logger
        else:
            self.logger = setup_custom_logger("UserConfig")

        # Local API Related 
        self.url: str = ""
        self.email: str = ""
        self.password: str = ""
        self.token: str = ""
        
        self.param_realdata_id: int = 0

    def getLocalAPIInfo(self):
        config = configparser.ConfigParser()
        try:
            config.read('./setting.ini')

            # Local API Related 
            self.url = config["NETWORK_SETTING"].get("url")
            self.email = config["AUTHENTICATION"].get("email")
            self.password = config["AUTHENTICATION"].get("password")
            self.token = config["AUTHENTICATION"].get("token")
            
            self.param_realdata_id = config["PARAMETER"].get("param_realdata_id")

            self.is_read = True
        except Exception as e:
            print('\x1b[31;20mException: ', str(e), '\x1b[0m')
            traceback.print_exc()
            self.is_read = False

        return self.is_read

    def __str__(self) -> str:
        obj_dict = self.__dict__.copy()
        obj_dict.pop('logger', None)  # 删除logger属性
        json_data = json.dumps(obj_dict)
        return json_data
