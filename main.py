from flask import Flask, Blueprint, request, jsonify
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from summarization import summarize, download_models

load_dotenv()

app = Flask(__name__)

api = Blueprint('api', __name__, template_folder='templates')

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
    summaries = summarize(content)

    return jsonify(summaries=summaries)
  except Exception as e:
    app.logger.error(e)
    return jsonify(status_code='500', msg='Interval Server Error'), 500

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
  # Loads models into memory
  download_models()

  # initialize the log handler
  logHandler = RotatingFileHandler(
    os.environ.get('ERRORS_LOG_PATH', 'errors.log'), 
    maxBytes=1000, backupCount=1)
  logHandler.setLevel(logging.INFO)
  app.logger.setLevel(logging.INFO)

  app.logger.addHandler(logHandler) 

  app.run(debug=True, port=5900, host='0.0.0.0')