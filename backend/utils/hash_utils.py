# utils/hash_utils.py
import hashlib

def verify_hash(password, hash_value, algorithm):
    """
    Verify that the hash of the given password matches the provided hash value.
    
    :param password: Plain text password.
    :param hash_value: Expected hash value.
    :param algorithm: Hash algorithm to use (e.g., "md5", "sha256").
    :return: True if the computed hash matches, False otherwise.
    """
    try:
        hasher = getattr(hashlib, algorithm.lower())
    except AttributeError:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    return hasher(password.encode()).hexdigest() == hash_value
