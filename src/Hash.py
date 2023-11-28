import hmac
import hashlib
import urllib.parse
import binascii
        
class Hash:

    def __init__(self, pinelabs):
        self.key = pinelabs.key
        self.secret = pinelabs.secret

    def create(self, body):
        # Create hash for the given payload | body
        try:
            # Decoding Secret
            hex_bytes = binascii.unhexlify(self.secret)
            decoded_secret = hex_bytes.decode('latin-1')

            hmac_hash = hmac.new(decoded_secret.encode('latin-1'), body.encode('latin-1'), hashlib.sha256)
            hash_hex = hmac_hash.hexdigest()
            return hash_hex.upper()
        except Exception as e:
            raise Exception(str(e))
        
    def verify(self, hash, response): 
        # Verify hash for the given payload | response
        try:
            # Decoding Secret
            hex_bytes = binascii.unhexlify(self.secret)
            decoded_secret = hex_bytes.decode('latin-1')

            keys_to_remove = ['ppc_DIA_SECRET', 'ppc_DIA_SECRET_TYPE']

            for key in keys_to_remove:
                response.pop(key, None)

            # Sort the keys alphabetically
            sorted_data = {key: response[key] for key in sorted(response.keys())}
            
            # Encode all characters except spaces and forward slashes and ":"
            urlEncodedResponse = '&'.join([f'{key}={self.custom_quote(value)}' for key, value in sorted_data.items()])

            hmac_hash = hmac.new(decoded_secret.encode('latin-1'), urlEncodedResponse.encode('latin-1'), hashlib.sha256)
            hash_hex = hmac_hash.hexdigest()

            return hash_hex.upper() == hash.upper()
        except Exception as e:
            raise Exception(str(e))
        
    def custom_quote(self, value):
        # Encode all characters except spaces and forward slashes
        encoded_value = ''
        for char in value:
            if char == '/' or char == ' ' or char == ':' or char == '=' or char == '*':
                encoded_value += char
            else:
                encoded_value += urllib.parse.quote(char, safe='')

        return encoded_value
        