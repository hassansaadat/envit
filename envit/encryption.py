from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidKey


class EncryptionManager:
    def __init__(self, key: str):
        try:
            self._validate_key(key)
            self._fernet = Fernet(key.encode())
        except InvalidKey:
            print("Error: Invalid encryption key provided.")
            raise

    def _validate_key(self, key: str) -> None:
        if len(key) != 44:
            raise InvalidKey("Invalid key length")
        try:
            Fernet(key.encode())
        except (TypeError, ValueError):
            raise InvalidKey("Invalid key format")

    def encrypt(self, data: str) -> bytes:
        try:
            encrypted_data = self._fernet.encrypt(data.encode())
        except InvalidToken:
            print("Error: Failed to encrypt data.")
            raise
        return encrypted_data

    def decrypt(self, encrypted_data: bytes) -> str:
        try:
            decrypted_data = self._fernet.decrypt(encrypted_data)
        except InvalidToken:
            print("Error: Failed to decrypt data. Invalid token.")
            raise
        except Exception as e:
            print("Error: Failed to decrypt data.", e)
            raise
        return decrypted_data.decode()
