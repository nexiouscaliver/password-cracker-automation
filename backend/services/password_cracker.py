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
    Encapsulates various password cracking techniques along with progress tracking.
    """

    def __init__(self, hash_value, algorithm="sha256", max_length=4, custom_dictionary=None, custom_rules=None):
        """
        Initialize the PasswordCracker instance.

        :param hash_value: The hashed password to crack.
        :param algorithm: The hashing algorithm used (default: "sha256").
        :param max_length: Maximum length for brute-force attempts.
        :param custom_dictionary: Optional list of words for dictionary-based techniques.
        :param custom_rules: Optional dictionary for mutation rules (e.g., {"a": "@", "o": "0"}).
        """
        self.hash_value = hash_value
        self.algorithm = algorithm.lower()
        self.max_length = max_length
        self.custom_dictionary = custom_dictionary
        self.custom_rules = custom_rules
        self.found_password = None  # Once a method finds the password, set it here.
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

    def dictionary_attack(self):
        if self.found_password is not None:
            logging.info("Dictionary attack skipped; password already found.")
            self.progress["results"]["dictionary_attack"] = self.found_password
            return self.found_password
        logging.info("Starting dictionary attack.")
        common_passwords = self.custom_dictionary if self.custom_dictionary else [
            "password", "123456", "123456789", "qwerty"
        ]
        for candidate in common_passwords:
            if self.hash_match(candidate):
                logging.info(f"Dictionary attack found password: {candidate}")
                self.found_password = candidate
                self.progress["results"]["dictionary_attack"] = candidate
                return candidate
        logging.info("Dictionary attack failed.")
        self.progress["results"]["dictionary_attack"] = "Failed"
        return "Failed"

    def rainbow_table_lookup(self):
        if self.found_password is not None:
            logging.info("Rainbow table lookup skipped; password already found.")
            self.progress["results"]["rainbow_table"] = self.found_password
            return self.found_password
        logging.info("Starting rainbow table lookup.")
        if self.algorithm == "md5":
            rainbow_table = {
                "5f4dcc3b5aa765d61d8327deb882cf99": "password",
                "e99a18c428cb38d5f260853678922e03": "abc123",
            }
            result = rainbow_table.get(self.hash_value)
            if result:
                logging.info(f"Rainbow table lookup found password: {result}")
                self.found_password = result
                self.progress["results"]["rainbow_table"] = result
                return result
        logging.info("Rainbow table lookup failed.")
        self.progress["results"]["rainbow_table"] = "Failed"
        return "Failed"

    def hybrid_attack(self):
        if self.found_password is not None:
            logging.info("Hybrid attack skipped; password already found.")
            self.progress["results"]["hybrid_attack"] = self.found_password
            return self.found_password
        logging.info("Starting hybrid attack.")
        # Instead of using dictionary_attack()'s result, loop over all dictionary candidates.
        candidates = self.custom_dictionary if self.custom_dictionary else ["password", "123456", "admin"]
        for base in candidates:
            for i in range(100):
                guess = base + str(i)
                if self.hash_match(guess):
                    logging.info(f"Hybrid attack found password: {guess}")
                    self.found_password = guess
                    self.progress["results"]["hybrid_attack"] = guess
                    return guess
        logging.info("Hybrid attack failed.")
        self.progress["results"]["hybrid_attack"] = "Failed"
        return "Failed"

    def rule_based_attack(self):
        if self.found_password is not None:
            logging.info("Rule-based attack skipped; password already found.")
            self.progress["results"]["rule_based_attack"] = self.found_password
            return self.found_password
        logging.info("Starting rule-based attack.")
        rules = self.custom_rules if self.custom_rules else {'a': '@', 'o': '0'}
        candidates = self.custom_dictionary if self.custom_dictionary else ["password", "admin", "welcome"]
        for word in candidates:
            mutated = word
            for key, val in rules.items():
                mutated = mutated.replace(key, val)
            if self.hash_match(mutated):
                logging.info(f"Rule-based attack found password: {mutated}")
                self.found_password = mutated
                self.progress["results"]["rule_based_attack"] = mutated
                return mutated
        logging.info("Rule-based attack failed.")
        self.progress["results"]["rule_based_attack"] = "Failed"
        return "Failed"

    def mask_attack(self):
        if self.found_password is not None:
            logging.info("Mask attack skipped; password already found.")
            self.progress["results"]["mask_attack"] = self.found_password
            return self.found_password
        logging.info("Starting mask attack.")
        # A fixed pattern simulation.
        for mid in ["", "b", "B", "c", "C"]:
            guess = "A" + mid + "123"
            if self.hash_match(guess):
                logging.info(f"Mask attack found password: {guess}")
                self.found_password = guess
                self.progress["results"]["mask_attack"] = guess
                return guess
        logging.info("Mask attack failed.")
        self.progress["results"]["mask_attack"] = "Failed"
        return "Failed"

    def markov_chain_attack(self):
        if self.found_password is not None:
            logging.info("Markov chain attack skipped; password already found.")
            self.progress["results"]["markov_chain_attack"] = self.found_password
            return self.found_password
        logging.info("Starting Markov chain attack.")
        probable_guesses = ["password", "passw0rd", "pass1234"]
        for guess in probable_guesses:
            if self.hash_match(guess):
                logging.info(f"Markov chain attack found password: {guess}")
                self.found_password = guess
                self.progress["results"]["markov_chain_attack"] = guess
                return guess
        logging.info("Markov chain attack failed.")
        self.progress["results"]["markov_chain_attack"] = "Failed"
        return "Failed"

    def phonetic_attack(self):
        if self.found_password is not None:
            logging.info("Phonetic attack skipped; password already found.")
            self.progress["results"]["phonetic_attack"] = self.found_password
            return self.found_password
        logging.info("Starting phonetic attack.")
        phonetic_guesses = ["password", "passwurd", "pazzword"]
        for guess in phonetic_guesses:
            if self.hash_match(guess):
                logging.info(f"Phonetic attack found password: {guess}")
                self.found_password = guess
                self.progress["results"]["phonetic_attack"] = guess
                return guess
        logging.info("Phonetic attack failed.")
        self.progress["results"]["phonetic_attack"] = "Failed"
        return "Failed"

    def ml_guessing(self):
        if self.found_password is not None:
            logging.info("Machine learning guessing skipped; password already found.")
            self.progress["results"]["ml_guessing"] = self.found_password
            return self.found_password
        logging.info("Starting machine learning guessing attack.")
        ml_guesses = ["password", "123456", "qwerty"]
        for guess in ml_guesses:
            if self.hash_match(guess):
                logging.info(f"Machine learning guessing found password: {guess}")
                self.found_password = guess
                self.progress["results"]["ml_guessing"] = guess
                return guess
        logging.info("Machine learning guessing attack failed.")
        self.progress["results"]["ml_guessing"] = "Failed"
        return "Failed"

    def brute_force_crack(self):
        if self.found_password is not None:
            logging.info("Brute force attack skipped; password already found.")
            self.progress["results"]["brute_force"] = self.found_password
            return self.found_password
        logging.info("Starting brute force attack.")
        chars = string.ascii_letters + string.digits
        # To avoid heavy computation, if max_length is too high, skip brute force.
        if self.max_length > 4:
            logging.info("Brute force attack skipped due to high max_length.")
            self.progress["results"]["brute_force"] = "Skipped"
            return "Skipped"
        for length in range(1, self.max_length + 1):
            with ThreadPoolExecutor() as executor:
                futures = {}
                for attempt in itertools.product(chars, repeat=length):
                    guess = ''.join(attempt)
                    future = executor.submit(self.hash_match, guess)
                    futures[future] = guess
                for future in as_completed(futures):
                    if future.result():
                        found = futures[future]
                        logging.info(f"Brute force found password: {found}")
                        self.found_password = found
                        self.progress["results"]["brute_force"] = found
                        return found
        logging.info("Brute force attack failed.")
        self.progress["results"]["brute_force"] = "Failed"
        return "Failed"

    def combinator_attack(self):
        if self.found_password is not None:
            logging.info("Combinator attack skipped; password already found.")
            self.progress["results"]["combinator_attack"] = self.found_password
            return self.found_password
        logging.info("Starting combinator attack.")
        dict1 = self.custom_dictionary if self.custom_dictionary else ["password", "admin"]
        dict2 = ["123", "1234", "12345"]
        for word1 in dict1:
            for word2 in dict2:
                guess = word1 + word2
                if self.hash_match(guess):
                    logging.info(f"Combinator attack found password: {guess}")
                    self.found_password = guess
                    self.progress["results"]["combinator_attack"] = guess
                    return guess
        logging.info("Combinator attack failed.")
        self.progress["results"]["combinator_attack"] = "Failed"
        return "Failed"

    def run_all_methods(self):
        """
        Execute all cracking techniques sequentially.
        The techniques are reordered so that the fast methods run first;
        once any method finds the password, subsequent methods simply return the found password.
        """
        techniques = [
            ("dictionary_attack", self.dictionary_attack),
            ("rainbow_table", self.rainbow_table_lookup),
            ("hybrid_attack", self.hybrid_attack),
            ("rule_based_attack", self.rule_based_attack),
            ("mask_attack", self.mask_attack),
            ("markov_chain_attack", self.markov_chain_attack),
            ("phonetic_attack", self.phonetic_attack),
            ("ml_guessing", self.ml_guessing),
            ("combinator_attack", self.combinator_attack),
            ("brute_force", self.brute_force_crack)
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
        """Return current progress as a JSON-compatible dictionary."""
        return self.progress


def crack_password(hash_value, algorithm="sha256", method="all", extra_data=None):
    """
    Wrapper function to crack a given hash using a specified technique.

    :param hash_value: The hash value to crack.
    :param algorithm: The hashing algorithm used (e.g., "md5", "sha256").
    :param method: The technique to use; one of:
                   "brute_force", "dictionary_attack", "rainbow_table", "hybrid_attack",
                   "rule_based_attack", "mask_attack", "markov_chain_attack", "phonetic_attack",
                   "ml_guessing", "combinator_attack", or "all".
    :param extra_data: Optional configuration (e.g., custom_dictionary, custom_rules, max_length).
    :return: A dictionary with keys "result" (detailed progress) and "final_password" (the found password or a failure message).
    """
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
