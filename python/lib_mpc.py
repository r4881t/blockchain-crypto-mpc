import codecs
from Crypto.Hash import keccak
import mpc_crypto
from binascii import unhexlify
from tests import exec_client_server, CLIENT, SERVER

def public_to_address(public_key: str):
        public_key_bytes = codecs.decode(public_key, 'hex')
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(public_key_bytes)
        keccak_digest = keccak_hash.hexdigest()
        # Take last 20 bytes
        wallet_len = 40
        wallet = '0x' + keccak_digest[-wallet_len:]
        return wallet

def gen_shares():
  other = mpc_crypto.Eddsa(CLIENT)
  btpk = mpc_crypto.Eddsa(SERVER)

  other.initGenerate()
  btpk.initGenerate()

  exec_client_server(other, btpk)

  publicKey = btpk.getPublic().hex()
  bitpackShare = btpk.exportShare().hex()
  otherShare = other.exportShare().hex()
  address = public_to_address(publicKey)

  if test_shares(client=other, server=btpk):
    return {
      'address': address,
      'bitpack_share': bitpackShare,
      'other_share': otherShare
    }

def signMessage(
  bitpack_share: str,
  other_share: str,
  data: str):

  print('Signing message...0')
  other = mpc_crypto.Eddsa(CLIENT, unhexlify(other_share))
  btpk = mpc_crypto.Eddsa(SERVER, unhexlify(bitpack_share))

  print("Signing message...1")

  byteData = data.encode()

  other.initSign(byteData, False)
  print("Signing message...2")
  btpk.initSign(byteData, False)
  print("Signing message...3")

  exec_client_server(other, btpk)
  print("Signing message...4")

  signature = other.getSignResult()
  print("Signing message...5")

  other.verify(byteData, signature)
  print("Signing message...6")
  return signature.hex()

def refresh_shares(
  bitpack_share: str,
  other_share: str):

  other = mpc_crypto.Eddsa(CLIENT, unhexlify(other_share))
  btpk = mpc_crypto.Eddsa(SERVER, unhexlify(bitpack_share))

  other.initRefresh()
  btpk.initRefresh()

  exec_client_server(other, btpk)

  return {
    'bitpack_share': btpk.exportShare().hex(),
    'other_share': other.exportShare().hex()
  }

def test_shares(client, server):
  return True

def bip32_derive(
  bitpack_share: str,
  other_share: str):

  other = mpc_crypto.Eddsa(CLIENT, unhexlify(other_share))
  btpk = mpc_crypto.Eddsa(SERVER, unhexlify(bitpack_share))

  clientObj = mpc_crypto.Bip32(CLIENT)
  serverObj = mpc_crypto.Bip32(SERVER)

  clientObj.initDerive(other, 0, False)
  serverObj.initDerive(btpk, 0, False)

  exec_client_server(clientObj, serverObj)

  clientObj.getDeriveResult()
  serverObj.getDeriveResult()

  return {
    'bitpack_share': serverObj.exportShare().hex(),
    'other_share': clientObj.exportShare().hex()
  }

def gen_shares_generic():
  clientObj = mpc_crypto.GenericSecret(CLIENT)
  serverObj = mpc_crypto.GenericSecret(SERVER)
  clientObj.initGenerate(256)
  serverObj.initGenerate(256)
  exec_client_server(clientObj, serverObj)

  return {
    'bitpack_share': serverObj.exportShare().hex(),
    'other_share': clientObj.exportShare().hex()
  }
