import json
import os

class ConfigLoader:
    def __init__(self, default_config_file='default_config.json', user_config_file='user_config.json'):
        self.config = self.load_defaults(default_config_file)
        self.user_config_file = user_config_file

    def load_defaults(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def load_user_config(self):
        if os.path.exists(self.user_config_file):
            with open(self.user_config_file, 'r') as f:
                user_config = json.load(f)
            self.merge_configs(user_config)

    def merge_configs(self, user_config):
        for key, value in user_config.items():
            if isinstance(value, dict) and key in self.config:
                self.config[key].update(value)
            else:
                self.config[key] = value

    def get(self, key, default=None):
        return self.config.get(key, default)

if __name__ == '__main__':
    config_loader = ConfigLoader()
    config_loader.load_user_config()
    print(config_loader.get('api_key', 'default_api_key'))