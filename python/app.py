from crypt import methods
from flask import Flask, request, jsonify
from lib_mpc import gen_shares, signMessage, refresh_shares
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ping")
def ping():
    return 'pong'

@app.route("/gen", methods=['POST'])
def gen():
  res = gen_shares()
  return jsonify(res)

@app.route("/sign", methods=['POST'])
def sign():
  data = request.get_json(force=True)
  other_share: str = data['other_share']
  btpk_share: str = data['bitpack_share']
  message: str = data['data']
  sig = signMessage(btpk_share, other_share, message)
  return jsonify(sig)

@app.route("/refresh", methods=['POST'])
def refresh():
  data = request.get_json(force=True)
  other_share: str = data['other_share']
  btpk_share: str = data['bitpack_share']
  res = refresh_shares(btpk_share, other_share)
  return jsonify(res)
