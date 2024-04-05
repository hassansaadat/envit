import argparse
from envit.encryption import EncryptionManager
import os
import sys
from cryptography.fernet import Fernet


DEFAULT_ENVS_DIR = 'envs'


def get_paths(env_dir, environment):
    environment = environment.lower()
    encrypted_path = os.path.join(env_dir, f'{environment}.env.enc')
    decrypted_path = os.path.join(env_dir, f'{environment}.env')
    return encrypted_path, decrypted_path


def encrypt_file(input_file, output_file, key):
    try:
        with open(input_file, 'r') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    manager = EncryptionManager(key)
    encrypted_data = manager.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)


def decrypt_file(input_file, output_file, key):
    try:
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    manager = EncryptionManager(key)
    decrypted_data = manager.decrypt(encrypted_data)

    with open(output_file, 'w') as f:
        f.write(decrypted_data)


def generate_key():
    key = Fernet.generate_key()
    key_str = key.decode()
    print(key_str)


def main():
    parser = argparse.ArgumentParser(description="Securely encrypt and decrypt environment variables and credentials")
    parser.add_argument('-d', '--env_dir', default=DEFAULT_ENVS_DIR, help='Default env directory')
    subparsers = parser.add_subparsers(dest='command', required=True, help='Subcommands')

    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    encrypt_parser.add_argument('-e', '--environment', required=True, help='Environment file name to encrypt')
    encrypt_parser.add_argument('-k', '--key', required=True, help='Encryption key')

    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument('-e', '--environment', required=True, help='Environment file name to decrypt')
    decrypt_parser.add_argument('-k', '--key', required=True, help='Decryption key')

    subparsers.add_parser('keygen', help='Generate a Secret key')

    args = parser.parse_args()

    if args.command == 'keygen':
        generate_key()
        return

    env_dir = args.env_dir
    environment = args.environment
    key = args.key

    encrypted_file, decrypted_file = get_paths(env_dir, environment)

    if args.command == 'encrypt':
        encrypt_file(decrypted_file, encrypted_file, key)
    elif args.command == 'decrypt':
        decrypt_file(encrypted_file, decrypted_file, key)


if __name__ == "__main__":
    main()
