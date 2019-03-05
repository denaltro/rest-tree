import yaml
import pathlib
import base64


class Config:
    def __init__(self):
        _config_file = self._read_config()

        mongo = _config_file['mongo']
        self.mongo_host = mongo['host']
        self.mongo_port = mongo['port']
        self.mongo_database = mongo['database']
        self.mongo_collection = mongo['collection']

        api = _config_file['api']
        self.api_host = api['host']
        self.api_port = api['port']

        auth = _config_file['auth']
        self.auth_user = auth['user']
        self.auth_password = auth['password']
        user_pass = base64.b64encode('{}:{}'.format(
            self.auth_user, self.auth_password).encode('utf-8'))
        self.basic_auth = 'Basic {}'.format(user_pass.decode('utf-8'))
        print(self.basic_auth)

    def _read_config(self):
        file_path = (
            '{}/../config/config.yml'.format(pathlib.Path(__file__).parent))
        try:
            with open(file_path, 'r', encoding='utf8') as file:
                return yaml.load(file)
        except Exception as e:
            raise Exception('Could not load config file: {}'.format(e))


config = Config()

__all__ = ['config']
