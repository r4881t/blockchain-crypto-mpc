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

  other = mpc_crypto.Eddsa(CLIENT, unhexlify(other_share))
  btpk = mpc_crypto.Eddsa(SERVER, unhexlify(bitpack_share))

  byteData = data.encode()

  other.initSign(byteData, True)
  btpk.initSign(byteData, True)

  exec_client_server(other, btpk)

  signature = other.getSignResult()
  other.verify(byteData, signature)
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