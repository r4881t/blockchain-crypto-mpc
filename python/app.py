from crypt import methods
from flask import Flask, request, jsonify
from lib_mpc import gen_shares, signMessage, refresh_shares, bip32_derive, gen_shares_generic
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ping")
def ping():
    return 'pong'

@app.route("/eddsa/gen", methods=['POST'])
def gen():
  res = gen_shares()
  return jsonify(res)

@app.route("/generic/gen", methods=['POST'])
def gen_generic():
  res = gen_shares_generic()
  return jsonify(res)

@app.route("/bip32/derive", methods=['POST'])
def bip32derive():
  data = request.get_json()
  other_share: str = data['other_share']
  btpk_share: str = data['bitpack_share']
  res = bip32_derive(btpk_share, other_share)
  return jsonify(res)

@app.route("/eddsa/sign", methods=['POST'])
def sign():
  data = request.get_json(force=True)
  other_share: str = data['other_share']
  btpk_share: str = data['bitpack_share']
  message: str = data['data']
  print("Signing message...00")
  sig = signMessage(btpk_share, other_share, message)
  return jsonify(sig)

@app.route("/eddsa/refresh", methods=['POST'])
def refresh():
  data = request.get_json(force=True)
  other_share: str = data['other_share']
  btpk_share: str = data['bitpack_share']
  res = refresh_shares(btpk_share, other_share)
  return jsonify(res)
