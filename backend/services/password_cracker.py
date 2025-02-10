# services/password_cracker.py
import hashlib
import itertools
import string

def crack_password(hash_value, hash_algorithm, method, extra_data=None):
    if method == 'brute_force':
        return brute_force_crack(hash_value, hash_algorithm)
    elif method == 'dictionary':
        return dictionary_attack(hash_value, hash_algorithm)
    elif method == 'rainbow':
        return rainbow_table_lookup(hash_value, hash_algorithm)
    else:
        return None

def hash_password(password, hash_algorithm):
    try:
        hash_func = getattr(hashlib, hash_algorithm.lower())
    except AttributeError:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
    return hash_func(password.encode()).hexdigest()

def brute_force_crack(hash_value, hash_algorithm, max_length=4):
    # WARNING: This is a naive brute force implementation for demo purposes.
    characters = string.ascii_lowercase + string.digits
    for length in range(1, max_length + 1):
        for attempt in itertools.product(characters, repeat=length):
            attempt_password = ''.join(attempt)
            if hash_password(attempt_password, hash_algorithm) == hash_value:
                return attempt_password
    return None

def dictionary_attack(hash_value, hash_algorithm, dictionary_file='common_passwords.txt'):
    try:
        with open(dictionary_file, 'r') as f:
            for line in f:
                candidate = line.strip()
                if hash_password(candidate, hash_algorithm) == hash_value:
                    return candidate
    except FileNotFoundError:
        # If dictionary file not found, use a small predefined list
        common_passwords = ['password', '123456', '123456789', 'qwerty']
        for candidate in common_passwords:
            if hash_password(candidate, hash_algorithm) == hash_value:
                return candidate
    return None

def rainbow_table_lookup(hash_value, hash_algorithm):
    # Simulated rainbow table with precomputed MD5 hashes for demonstration.
    rainbow_table = {
        '5f4dcc3b5aa765d61d8327deb882cf99': 'password',  # MD5 for "password"
        'e99a18c428cb38d5f260853678922e03': 'abc123',    # MD5 for "abc123"
    }
    if hash_algorithm.lower() == 'md5':
        return rainbow_table.get(hash_value)
    return None
