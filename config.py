"""app configuration"""
import configparser


def load_config():
    """Method load_config"""
    configuration = configparser.ConfigParser()
    configuration.read(".config")
    return configuration


config = load_config()
