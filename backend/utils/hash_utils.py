# utils/hash_utils.py
import hashlib

def verify_hash(password, hash_value, hash_algorithm):
    try:
        hash_func = getattr(hashlib, hash_algorithm.lower())
    except AttributeError:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
    return hash_func(password.encode()).hexdigest() == hash_value
