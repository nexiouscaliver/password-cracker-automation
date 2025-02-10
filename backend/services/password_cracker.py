# services/password_cracker.py

import hashlib
import itertools
import string
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class PasswordCracker:
    """
    A class to encapsulate various password cracking techniques along with progress tracking.
    """

    def __init__(self, hash_value, algorithm="sha256", max_length=4, custom_dictionary=None, custom_rules=None):
        """
        Initialize the PasswordCracker instance.

        :param hash_value: The hashed password to crack.
        :param algorithm: The hashing algorithm used (default is "sha256").
        :param max_length: Maximum length for brute-force attempts.
        :param custom_dictionary: Optional list of words for dictionary-based techniques.
        :param custom_rules: Optional dictionary for mutation rules (e.g., {"a": "@", "o": "0"}).
        """
        self.hash_value = hash_value
        self.algorithm = algorithm.lower()
        self.max_length = max_length
        self.custom_dictionary = custom_dictionary
        self.custom_rules = custom_rules

        # Initialize progress tracking dictionary
        self.progress = {
            "total_techniques": 10,
            "completed_techniques": 0,
            "remaining_techniques": 10,
            "results": {
                "brute_force": None,
                "dictionary_attack": None,
                "rainbow_table": None,
                "hybrid_attack": None,
                "rule_based_attack": None,
                "mask_attack": None,
                "markov_chain_attack": None,
                "phonetic_attack": None,
                "ml_guessing": None,
                "combinator_attack": None,
            }
        }

    def hash_match(self, guess):
        """
        Check whether the guess, when hashed, matches the target hash.
        """
        try:
            hasher = getattr(hashlib, self.algorithm)
        except AttributeError:
            raise ValueError(f"Unsupported hash algorithm: {self.algorithm}")
        return hasher(guess.encode()).hexdigest() == self.hash_value

    def brute_force_crack(self):
        """
        Brute force attack: try all possible combinations of characters up to self.max_length.
        Uses a simple sequential approach (which you could later optimize further via parallelism).
        """
        logging.info("Starting brute force attack.")
        chars = string.ascii_letters + string.digits
        for length in range(1, self.max_length + 1):
            # Instead of a full-blown parallelization, we illustrate a threaded approach per length group.
            with ThreadPoolExecutor() as executor:
                # Prepare a list of all combinations for the current length in batches.
                futures = {}
                for attempt in itertools.product(chars, repeat=length):
                    guess = ''.join(attempt)
                    future = executor.submit(self.hash_match, guess)
                    futures[future] = guess

                for future in as_completed(futures):
                    if future.result():
                        found = futures[future]
                        logging.info(f"Brute force found password: {found}")
                        self.progress["results"]["brute_force"] = found
                        return found

        logging.info("Brute force attack failed.")
        self.progress["results"]["brute_force"] = "Failed"
        return None

    def dictionary_attack(self):
        """
        Dictionary attack: check a list of common passwords (or a custom dictionary if provided).
        """
        logging.info("Starting dictionary attack.")
        common_passwords = self.custom_dictionary if self.custom_dictionary else [
            "password", "123456", "123456789", "qwerty"
        ]
        for candidate in common_passwords:
            if self.hash_match(candidate):
                logging.info(f"Dictionary attack found password: {candidate}")
                self.progress["results"]["dictionary_attack"] = candidate
                return candidate
        logging.info("Dictionary attack failed.")
        self.progress["results"]["dictionary_attack"] = "Failed"
        return None

    def rainbow_table_lookup(self):
        """
        Rainbow table lookup: use a precomputed mapping (only simulated for md5 in this example).
        """
        logging.info("Starting rainbow table lookup.")
        if self.algorithm == "md5":
            rainbow_table = {
                "5f4dcc3b5aa765d61d8327deb882cf99": "password",
                "e99a18c428cb38d5f260853678922e03": "abc123",
            }
            result = rainbow_table.get(self.hash_value)
            if result:
                logging.info(f"Rainbow table lookup found password: {result}")
                self.progress["results"]["rainbow_table"] = result
                return result

        logging.info("Rainbow table lookup failed.")
        self.progress["results"]["rainbow_table"] = "Failed"
        return None

    def hybrid_attack(self):
        """
        Hybrid attack: combine a dictionary word with brute force (e.g., by appending numbers).
        """
        logging.info("Starting hybrid attack.")
        base = self.dictionary_attack()
        if base and base != "Failed":
            for i in range(100):
                guess = base + str(i)
                if self.hash_match(guess):
                    logging.info(f"Hybrid attack found password: {guess}")
                    self.progress["results"]["hybrid_attack"] = guess
                    return guess
        logging.info("Hybrid attack failed.")
        self.progress["results"]["hybrid_attack"] = "Failed"
        return None

    def rule_based_attack(self):
        """
        Rule-based attack: apply mutation rules (for example, replacing letters with symbols) to dictionary words.
        """
        logging.info("Starting rule-based attack.")
        rules = self.custom_rules if self.custom_rules else {'a': '@', 'o': '0'}
        candidates = self.custom_dictionary if self.custom_dictionary else ["password", "admin", "welcome"]
        for word in candidates:
            mutated = word
            for key, val in rules.items():
                mutated = mutated.replace(key, val)
            if self.hash_match(mutated):
                logging.info(f"Rule-based attack found password: {mutated}")
                self.progress["results"]["rule_based_attack"] = mutated
                return mutated
        logging.info("Rule-based attack failed.")
        self.progress["results"]["rule_based_attack"] = "Failed"
        return None

    def mask_attack(self):
        """
        Mask attack: use a specific pattern (for instance, guessing that the password starts with 'A' and ends with '123').
        """
        logging.info("Starting mask attack.")
        # This is a simple simulation with a fixed pattern.
        for mid in ["", "b", "B", "c", "C"]:
            guess = "A" + mid + "123"
            if self.hash_match(guess):
                logging.info(f"Mask attack found password: {guess}")
                self.progress["results"]["mask_attack"] = guess
                return guess
        logging.info("Mask attack failed.")
        self.progress["results"]["mask_attack"] = "Failed"
        return None

    def markov_chain_attack(self):
        """
        Markov chain attack: generate password guesses based on probabilities derived from password datasets.
        (This implementation is a placeholder simulating a few probable guesses.)
        """
        logging.info("Starting Markov chain attack.")
        probable_guesses = ["password", "passw0rd", "pass1234"]
        for guess in probable_guesses:
            if self.hash_match(guess):
                logging.info(f"Markov chain attack found password: {guess}")
                self.progress["results"]["markov_chain_attack"] = guess
                return guess
        logging.info("Markov chain attack failed.")
        self.progress["results"]["markov_chain_attack"] = "Failed"
        return None

    def phonetic_attack(self):
        """
        Phonetic attack: generate guesses based on similar pronunciation patterns.
        """
        logging.info("Starting phonetic attack.")
        phonetic_guesses = ["password", "passwurd", "pazzword"]
        for guess in phonetic_guesses:
            if self.hash_match(guess):
                logging.info(f"Phonetic attack found password: {guess}")
                self.progress["results"]["phonetic_attack"] = guess
                return guess
        logging.info("Phonetic attack failed.")
        self.progress["results"]["phonetic_attack"] = "Failed"
        return None

    def ml_guessing(self):
        """
        Machine learning guessing: use (or simulate) a model to predict likely passwords.
        (This is a dummy implementation for demonstration purposes.)
        """
        logging.info("Starting machine learning guessing attack.")
        ml_guesses = ["password", "123456", "qwerty"]
        for guess in ml_guesses:
            if self.hash_match(guess):
                logging.info(f"Machine learning guessing found password: {guess}")
                self.progress["results"]["ml_guessing"] = guess
                return guess
        logging.info("Machine learning guessing attack failed.")
        self.progress["results"]["ml_guessing"] = "Failed"
        return None

    def combinator_attack(self):
        """
        Combinator attack: combine words from multiple dictionaries to form new guesses.
        """
        logging.info("Starting combinator attack.")
        dict1 = self.custom_dictionary if self.custom_dictionary else ["password", "admin"]
        dict2 = ["123", "1234", "12345"]
        for word1 in dict1:
            for word2 in dict2:
                guess = word1 + word2
                if self.hash_match(guess):
                    logging.info(f"Combinator attack found password: {guess}")
                    self.progress["results"]["combinator_attack"] = guess
                    return guess
        logging.info("Combinator attack failed.")
        self.progress["results"]["combinator_attack"] = "Failed"
        return None

    def run_all_methods(self):
        """
        Execute all cracking techniques sequentially while updating progress and logging details.
        """
        techniques = [
            ("brute_force", self.brute_force_crack),
            ("dictionary_attack", self.dictionary_attack),
            ("rainbow_table", self.rainbow_table_lookup),
            ("hybrid_attack", self.hybrid_attack),
            ("rule_based_attack", self.rule_based_attack),
            ("mask_attack", self.mask_attack),
            ("markov_chain_attack", self.markov_chain_attack),
            ("phonetic_attack", self.phonetic_attack),
            ("ml_guessing", self.ml_guessing),
            ("combinator_attack", self.combinator_attack)
        ]
        for name, method in techniques:
            start_time = time.time()
            logging.info(f"Starting technique: {name}")
            try:
                result = method()
            except Exception as e:
                logging.error(f"Error in {name}: {e}")
                result = "Error"
            end_time = time.time()
            logging.info(f"Technique '{name}' completed in {end_time - start_time:.2f} seconds with result: {result}")
            self.progress["completed_techniques"] += 1
            self.progress["remaining_techniques"] = self.progress["total_techniques"] - self.progress["completed_techniques"]
        return self.progress

    def get_progress(self):
        """
        Return current progress as a JSON-compatible dictionary.
        """
        return self.progress


def crack_password(hash_value, algorithm="sha256", method="all", extra_data=None):
    """
    Wrapper function to crack a given hash using a specified technique.

    Parameters:
      - hash_value (str): The hash value to crack.
      - algorithm (str): The hashing algorithm used (e.g., "md5", "sha256").
      - method (str): The technique to use. Valid options are:
          "brute_force", "dictionary_attack", "rainbow_table", "hybrid_attack",
          "rule_based_attack", "mask_attack", "markov_chain_attack", "phonetic_attack",
          "ml_guessing", "combinator_attack", or "all" (to run all techniques sequentially).
      - extra_data (dict): Optional configuration (e.g., custom_dictionary, custom_rules, max_length).

    Returns:
      A dictionary with two keys:
        - "result": the progress dictionary (including detailed technique results).
        - "final_password": the password found by the selected method (or None/"Failed").
    """
    # Allow overriding defaults via extra_data
    custom_dictionary = extra_data.get("custom_dictionary") if extra_data else None
    custom_rules = extra_data.get("custom_rules") if extra_data else None
    max_length = extra_data.get("max_length", 4) if extra_data else 4

    cracker = PasswordCracker(
        hash_value,
        algorithm=algorithm,
        max_length=max_length,
        custom_dictionary=custom_dictionary,
        custom_rules=custom_rules
    )

    # Map method names to class methods.
    technique_mapping = {
        "brute_force": cracker.brute_force_crack,
        "dictionary_attack": cracker.dictionary_attack,
        "rainbow_table": cracker.rainbow_table_lookup,
        "hybrid_attack": cracker.hybrid_attack,
        "rule_based_attack": cracker.rule_based_attack,
        "mask_attack": cracker.mask_attack,
        "markov_chain_attack": cracker.markov_chain_attack,
        "phonetic_attack": cracker.phonetic_attack,
        "ml_guessing": cracker.ml_guessing,
        "combinator_attack": cracker.combinator_attack,
        "all": cracker.run_all_methods,
    }

    if method not in technique_mapping:
        raise ValueError("Invalid method specified.")

    final_password = technique_mapping[method]()
    return {"result": cracker.get_progress(), "final_password": final_password}
