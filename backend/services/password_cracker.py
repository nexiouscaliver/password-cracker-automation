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
    Provides two execution modes:
      - Short-circuit mode (default): stops after one method finds the password.
      - Full mode: runs every technique to assess the overall strength.
    """

    def __init__(self, hash_value, algorithm="sha256", max_length=4, custom_dictionary=None, custom_rules=None):
        """
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
        self.found_password = None  # Updated in short-circuit mode.
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
        """Check if the hash of the guess matches the target hash."""
        try:
            hasher = getattr(hashlib, self.algorithm)
        except AttributeError:
            raise ValueError(f"Unsupported hash algorithm: {self.algorithm}")
        return hasher(guess.encode()).hexdigest() == self.hash_value

    def dictionary_attack(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Dictionary attack skipped; password already found.")
            self.progress["results"]["dictionary_attack"] = self.found_password
            return self.found_password
        logging.info("Starting dictionary attack.")
        common_passwords = self.custom_dictionary if self.custom_dictionary else [
            "password", "123456", "123456789", "qwerty"
        ]
        result = "Failed"
        for candidate in common_passwords:
            if self.hash_match(candidate):
                result = candidate
                logging.info(f"Dictionary attack found password: {candidate}")
                break
        self.progress["results"]["dictionary_attack"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def rainbow_table_lookup(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Rainbow table lookup skipped; password already found.")
            self.progress["results"]["rainbow_table"] = self.found_password
            return self.found_password
        logging.info("Starting rainbow table lookup.")
        result = "Failed"
        if self.algorithm == "md5":
            rainbow_table = {
                "5f4dcc3b5aa765d61d8327deb882cf99": "password",
                "e99a18c428cb38d5f260853678922e03": "abc123",
            }
            result = rainbow_table.get(self.hash_value, "Failed")
            if result != "Failed":
                logging.info(f"Rainbow table lookup found password: {result}")
        self.progress["results"]["rainbow_table"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def hybrid_attack(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Hybrid attack skipped; password already found.")
            self.progress["results"]["hybrid_attack"] = self.found_password
            return self.found_password
        logging.info("Starting hybrid attack.")
        result = "Failed"
        candidates = self.custom_dictionary if self.custom_dictionary else ["password", "123456", "admin"]
        for base in candidates:
            for i in range(100):
                guess = base + str(i)
                if self.hash_match(guess):
                    result = guess
                    logging.info(f"Hybrid attack found password: {guess}")
                    break
            if result != "Failed":
                break
        self.progress["results"]["hybrid_attack"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def rule_based_attack(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Rule-based attack skipped; password already found.")
            self.progress["results"]["rule_based_attack"] = self.found_password
            return self.found_password
        logging.info("Starting rule-based attack.")
        result = "Failed"
        rules = self.custom_rules if self.custom_rules else {'a': '@', 'o': '0'}
        candidates = self.custom_dictionary if self.custom_dictionary else ["password", "admin", "welcome"]
        for word in candidates:
            mutated = word
            for key, val in rules.items():
                mutated = mutated.replace(key, val)
            if self.hash_match(mutated):
                result = mutated
                logging.info(f"Rule-based attack found password: {mutated}")
                break
        self.progress["results"]["rule_based_attack"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def mask_attack(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Mask attack skipped; password already found.")
            self.progress["results"]["mask_attack"] = self.found_password
            return self.found_password
        logging.info("Starting mask attack.")
        result = "Failed"
        for mid in ["", "b", "B", "c", "C"]:
            guess = "A" + mid + "123"
            if self.hash_match(guess):
                result = guess
                logging.info(f"Mask attack found password: {guess}")
                break
        self.progress["results"]["mask_attack"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def markov_chain_attack(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Markov chain attack skipped; password already found.")
            self.progress["results"]["markov_chain_attack"] = self.found_password
            return self.found_password
        logging.info("Starting Markov chain attack.")
        result = "Failed"
        probable_guesses = ["password", "passw0rd", "pass1234"]
        for guess in probable_guesses:
            if self.hash_match(guess):
                result = guess
                logging.info(f"Markov chain attack found password: {guess}")
                break
        self.progress["results"]["markov_chain_attack"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def phonetic_attack(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Phonetic attack skipped; password already found.")
            self.progress["results"]["phonetic_attack"] = self.found_password
            return self.found_password
        logging.info("Starting phonetic attack.")
        result = "Failed"
        phonetic_guesses = ["password", "passwurd", "pazzword"]
        for guess in phonetic_guesses:
            if self.hash_match(guess):
                result = guess
                logging.info(f"Phonetic attack found password: {guess}")
                break
        self.progress["results"]["phonetic_attack"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def ml_guessing(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Machine learning guessing skipped; password already found.")
            self.progress["results"]["ml_guessing"] = self.found_password
            return self.found_password
        logging.info("Starting machine learning guessing attack.")
        result = "Failed"
        ml_guesses = ["password", "123456", "qwerty"]
        for guess in ml_guesses:
            if self.hash_match(guess):
                result = guess
                logging.info(f"Machine learning guessing found password: {guess}")
                break
        self.progress["results"]["ml_guessing"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def brute_force_crack(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Brute force attack skipped; password already found.")
            self.progress["results"]["brute_force"] = self.found_password
            return self.found_password
        logging.info("Starting brute force attack.")
        result = "Failed"
        chars = string.ascii_letters + string.digits
        # To avoid excessive computation, skip if max_length is high.
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
                        result = futures[future]
                        logging.info(f"Brute force found password: {result}")
                        break
            if result != "Failed":
                break
        self.progress["results"]["brute_force"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def combinator_attack(self, allow_short_circuit=True):
        if allow_short_circuit and self.found_password is not None:
            logging.info("Combinator attack skipped; password already found.")
            self.progress["results"]["combinator_attack"] = self.found_password
            return self.found_password
        logging.info("Starting combinator attack.")
        result = "Failed"
        dict1 = self.custom_dictionary if self.custom_dictionary else ["password", "admin"]
        dict2 = ["123", "1234", "12345"]
        for word1 in dict1:
            for word2 in dict2:
                guess = word1 + word2
                if self.hash_match(guess):
                    result = guess
                    logging.info(f"Combinator attack found password: {guess}")
                    break
            if result != "Failed":
                break
        self.progress["results"]["combinator_attack"] = result
        if allow_short_circuit and result != "Failed":
            self.found_password = result
        return result

    def run_all_methods(self):
        """
        Execute all techniques in short-circuit mode (stops once a technique finds the password).
        Techniques are run in an order favoring faster methods.
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
                result = method(allow_short_circuit=True)
            except Exception as e:
                logging.error(f"Error in {name}: {e}")
                result = "Error"
            end_time = time.time()
            logging.info(f"Technique '{name}' completed in {end_time - start_time:.2f} seconds with result: {result}")
            self.progress["completed_techniques"] += 1
            self.progress["remaining_techniques"] = self.progress["total_techniques"] - self.progress["completed_techniques"]
            if self.found_password is not None:
                break
        return self.progress

    def run_all_methods_full(self):
        """
        Execute all techniques independently (full mode) to provide a complete analysis.
        Returns a dictionary with:
          - technique_details: A mapping from technique name to its result and duration.
          - strength_rating: A computed rating based on how many techniques succeeded.
        """
        technique_details = {}
        # Save current found_password and reset for full independent runs.
        original_found = self.found_password
        self.found_password = None

        techniques = {
            "dictionary_attack": self.dictionary_attack,
            "rainbow_table": self.rainbow_table_lookup,
            "hybrid_attack": self.hybrid_attack,
            "rule_based_attack": self.rule_based_attack,
            "mask_attack": self.mask_attack,
            "markov_chain_attack": self.markov_chain_attack,
            "phonetic_attack": self.phonetic_attack,
            "ml_guessing": self.ml_guessing,
            "combinator_attack": self.combinator_attack,
            "brute_force": self.brute_force_crack
        }
        for name, method in techniques.items():
            start_time = time.time()
            try:
                result = method(allow_short_circuit=False)
            except Exception as e:
                logging.error(f"Error in {name}: {e}")
                result = "Error"
            end_time = time.time()
            duration = end_time - start_time
            technique_details[name] = {"result": result, "duration": duration}
            logging.info(f"Technique '{name}' took {duration:.2f} seconds and returned: {result}")

        # Restore original found_password.
        self.found_password = original_found

        # Compute strength rating based on the number of techniques that succeeded.
        successes = sum(1 for details in technique_details.values() if details["result"] not in ["Failed", "Skipped", "Error"])
        if successes == 0:
            strength_rating = "Very Strong"
        elif successes <= 2:
            strength_rating = "Strong"
        elif successes <= 4:
            strength_rating = "Moderate"
        elif successes <= 7:
            strength_rating = "Weak"
        else:
            strength_rating = "Very Weak"

        analysis = {
            "technique_details": technique_details,
            "strength_rating": strength_rating
        }
        return analysis

    def get_progress(self):
        """Return the progress tracking dictionary."""
        return self.progress

def crack_password(hash_value, algorithm="sha256", method="all", extra_data=None):
    """
    Wrapper to crack a hash using a specified method.
    
    :param hash_value: The hash value to crack.
    :param algorithm: The hashing algorithm used.
    :param method: The technique to use. Options:
                   "brute_force", "dictionary_attack", "rainbow_table", "hybrid_attack",
                   "rule_based_attack", "mask_attack", "markov_chain_attack", "phonetic_attack",
                   "ml_guessing", "combinator_attack", "all" (short-circuit mode),
                   or "all_full" (full analysis mode).
    :param extra_data: Optional configuration (e.g., custom_dictionary, custom_rules, max_length).
    :return: If method is "all" or "all_full", returns the progress or analysis dictionary.
             Otherwise, returns a dictionary with "result" (progress details) and "final_password".
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
        "all_full": cracker.run_all_methods_full
    }

    if method not in technique_mapping:
        raise ValueError("Invalid method specified.")

    final_password = technique_mapping[method]()
    if method.startswith("all"):
        return {"result": final_password}
    else:
        return {"result": cracker.get_progress(), "final_password": final_password}
