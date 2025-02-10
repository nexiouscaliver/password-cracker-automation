# tests/test_password_cracker.py

import hashlib
import pytest
from services.password_cracker import PasswordCracker, crack_password

def get_hash(password, algorithm='md5'):
    hasher = getattr(hashlib, algorithm)
    return hasher(password.encode()).hexdigest()

@pytest.fixture
def md5_password():
    password = "password"
    hashed = get_hash(password, "md5")
    return password, hashed

def test_brute_force_attack():
    # Use a short password so brute force completes quickly.
    test_password = "abc"
    hashed = get_hash(test_password, "md5")
    cracker = PasswordCracker(hashed, algorithm="md5", max_length=3)
    result = cracker.brute_force_crack()
    assert result == test_password

def test_dictionary_attack(md5_password):
    password, hashed = md5_password
    cracker = PasswordCracker(hashed, algorithm="md5", custom_dictionary=["password", "admin"])
    result = cracker.dictionary_attack()
    assert result == password

def test_rainbow_table_lookup(md5_password):
    password, hashed = md5_password
    cracker = PasswordCracker(hashed, algorithm="md5")
    result = cracker.rainbow_table_lookup()
    assert result == password

def test_hybrid_attack():
    base_password = "password"
    hybrid_password = "password1"
    hashed = get_hash(hybrid_password, "md5")
    cracker = PasswordCracker(hashed, algorithm="md5", custom_dictionary=["password", "admin"])
    result = cracker.hybrid_attack()
    assert result == hybrid_password

def test_rule_based_attack():
    base_password = "password"
    mutated = "p@ssword"
    hashed = get_hash(mutated, "md5")
    cracker = PasswordCracker(hashed, algorithm="md5", custom_dictionary=["password"], custom_rules={"a": "@"})
    result = cracker.rule_based_attack()
    assert result == mutated

def test_mask_attack():
    # Monkey-patch hash_match to simulate a match.
    cracker = PasswordCracker("dummy", algorithm="md5")
    cracker.hash_match = lambda guess: guess == "A123"
    result = cracker.mask_attack()
    assert result == "A123"

def test_markov_chain_attack():
    probable = "passw0rd"
    hashed = get_hash(probable, "md5")
    cracker = PasswordCracker(hashed, algorithm="md5")
    result = cracker.markov_chain_attack()
    assert result == probable

def test_phonetic_attack():
    phonetic = "pazzword"
    hashed = get_hash(phonetic, "md5")
    cracker = PasswordCracker(hashed, algorithm="md5")
    result = cracker.phonetic_attack()
    assert result == phonetic

def test_ml_guessing():
    ml_guess = "123456"
    hashed = get_hash(ml_guess, "md5")
    cracker = PasswordCracker(hashed, algorithm="md5")
    result = cracker.ml_guessing()
    assert result == ml_guess

def test_combinator_attack():
    combinator = "admin1234"
    hashed = get_hash(combinator, "md5")
    cracker = PasswordCracker(hashed, algorithm="md5", custom_dictionary=["admin"])
    result = cracker.combinator_attack()
    assert result in ["admin123", "admin1234", "admin12345"]

def test_run_all_methods():
    base_password = "password"
    hashed = get_hash(base_password, "md5")
    # Use a custom dictionary so that dictionary_attack finds the password quickly.
    cracker = PasswordCracker(hashed, algorithm="md5", custom_dictionary=["password"])
    progress = cracker.run_all_methods()
    # Even though several techniques are skipped, all 10 techniques complete.
    assert progress["completed_techniques"] == progress["total_techniques"]

def test_crack_password_wrapper(md5_password):
    base_password, hashed = md5_password
    result_dict = crack_password(hashed, algorithm="md5", method="rainbow_table")
    assert result_dict["final_password"] == base_password
