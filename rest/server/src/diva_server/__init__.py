import logging
# Python 3.7 does not have importlib.metadata, so need to install importlib_metadata
from importlib_metadata import version

import connexion


def health_check():
    return {
        "status_code": 0,
        "detail": "Server is working",
        "version": version(__name__)
    }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = connexion.App(__name__, specification_dir='../spec', debug=True)
    app.add_api('swagger.yaml')
    app.run(port=8080)
