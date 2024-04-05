import pytest
from cryptography.exceptions import InvalidKey
from cryptography.fernet import Fernet

from envit.encryption import EncryptionManager


@pytest.fixture
def encryption_manager():
    key = Fernet.generate_key().decode()  # Generate a random key for testing
    return EncryptionManager(key)


def test_encrypt_decrypt(encryption_manager):
    data = 'This is a secret message.'

    encrypted_data = encryption_manager.encrypt(data)
    decrypted_data = encryption_manager.decrypt(encrypted_data)

    assert decrypted_data == data


def test_invalid_token(encryption_manager):
    data_to_encrypt = "Test data"
    encrypted_data = encryption_manager.encrypt(data_to_encrypt)

    # Manipulate encrypted data to make it invalid
    manipulated_data = bytearray(encrypted_data)
    manipulated_data[0] = (manipulated_data[0] + 1) % 256  # Modify the first byte to make it invalid

    # Attempt to decrypt the manipulated data
    with pytest.raises(Exception):
        encryption_manager.decrypt(bytes(manipulated_data))


def test_invalid_key():
    with pytest.raises(InvalidKey):
        key = 'InvalidKey'
        data = 'This is a secret message.'

        manager = EncryptionManager(key)
        manager.encrypt(data)
