import connexion
import logging
logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir='../spec', debug=True)
app.add_api('swagger.yaml')
app.run(port=8080)
