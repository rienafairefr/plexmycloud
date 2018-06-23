from flask_script import Manager

from plexcreatorapi.app import app

from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()

manager = Manager(app)

if __name__ == '__main__':
    manager.run()