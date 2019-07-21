import pickle
from flask import Flask, Blueprint, request, jsonify
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import summarization

load_dotenv()

MODEL_BUCKET = os.environ.get('MODEL_BUCKET', 'breef-models')
MODEL = None

app = Flask(__name__)

api = Blueprint('api', __name__, template_folder='templates')

@app.before_first_request
def _load_model():
  global MODEL

  MODEL = summarization.load_models()

@api.route('/shorten', methods=['GET', 'POST'])
def shorten():
  content = {}
  try:
    strContent = request.args.get('content', type = str)
    if strContent == None:
      content = request.get_json()['content']
    else:
      content = [strContent]
  except Exception:
    return jsonify(status_code='400', msg='Bad Request'), 400

  try:
    summaries = summarization.summarize(content, model=MODEL)

    return jsonify(summaries=summaries)
  except Exception as e:
    app.logger.error(e)
    return jsonify(status_code='500', msg='Interval Server Error'), 500

@app.errorhandler(500)
def server_error(e):
    app.logger.error('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
  # Downloads models locally
  summarization.download_models(MODEL_BUCKET)

  # initialize the log handler
  formatter = logging.Formatter(
      "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
  file_handler = RotatingFileHandler(os.environ.get('LOG_FILENAME', 'app.log'), maxBytes=10000000, backupCount=5)
  file_handler.setLevel(logging.DEBUG)
  file_handler.setFormatter(formatter)
  app.logger.addHandler(file_handler) 

  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)
  app.logger.addHandler(console_handler)

  app.run(debug=True, port=5900, host='0.0.0.0', use_reloader=False)