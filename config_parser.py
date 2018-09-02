import json

CONFIG_FILE="config.json"

def readConfig():
    config = {}
    try:
        with open(CONFIG_FILE) as config_file:
            config = json.loads(config_file.read())
    except Exception as e:
        print "Error while reading config file"
        raise e
    return config
