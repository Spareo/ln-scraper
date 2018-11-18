import ruamel.yaml as yaml

class SettingsParser:
    def __init__(self):
        pass

    def get_settings(self, settings_file):
        with open(settings_file, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                settings = {}
                settings['criteria'] = data['criteria']
                settings['pageguid'] = data['pageguid']
                return settings
            except yaml.YAMLError as exc:
                print(exc)