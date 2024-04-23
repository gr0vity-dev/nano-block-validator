import nano_lib_py as nl
from abc import ABC, abstractmethod
import json


class NanoBlockDifficulty:

    epoch_1 = ""
    epoch_2_base = ""
    epoch_2_receive = ""


class LiveDifficulty(NanoBlockDifficulty):

    epoch_1 = "ffffffc000000000"
    epoch_2_base = "fffffff800000000"
    epoch_2_receive = "fffffe0000000000"


class BetaDifficulty(NanoBlockDifficulty):

    epoch_1 = "fffff00000000000"
    epoch_2_base = "fffff00000000000"
    epoch_2_receive = "ffffe00000000000"


class ValidatorInterface(ABC):

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def get_block_hash(self):
        pass


class HashValidator(ValidatorInterface):
    def __init__(self, json_data, difficulty: NanoBlockDifficulty):
        self.account = json_data["account"]
        self.hash = json_data.get("hash")
        self.signature = json_data["signature"]
        self.difficulty = difficulty

    def get_block_hash(self):
        return self.hash

    def validate(self):
        base = self.difficulty.epoch_2_base
        receive = self.difficulty.epoch_2_receive
        epoch1 = self.difficulty.epoch_1

        return {
            "is_signature_valid": self._validate_signature(self.account, self.hash, self.signature),
            "is_work_valid_base": None,
            "is_work_valid_receive": None,
            "is_work_valid_epoch1": None,
            "difficulty": "0000000000000000",
            "epoch1_difficulty": epoch1,
            "base_difficulty": base,
            "receive_difficulty": receive,
            "base_multiplier": 0,
            "receive_multiplier": 0,
            "epoch1_multiplier": 0
        }

    def _validate_signature(self, account, block_hash, signature):
        public_key = nl.get_account_public_key(account_id=account)
        nl.validate_public_key(public_key)
        vk = nl.blocks.VerifyingKey(nl.blocks.unhexlify(public_key))
        try:
            vk.verify(
                sig=nl.blocks.unhexlify(signature),
                msg=nl.blocks.unhexlify(block_hash)
            )
            return True
        except Exception:
            return False


class BlockValidator(ValidatorInterface):
    def __init__(self, block_text, difficulty: NanoBlockDifficulty):
        self.block: nl.Block = nl.Block.from_json(block_text, verify=False)
        self.difficulty = difficulty

    def get_block_hash(self):
        return self.block.block_hash

    def validate(self):

        base = self.difficulty.epoch_2_base
        receive = self.difficulty.epoch_2_receive
        epoch1 = self.difficulty.epoch_1

        return {
            "is_signature_valid": self._validate_signature(),
            "is_work_valid_base": self._validate_work(base),
            "is_work_valid_receive": self._validate_work(receive),
            "is_work_valid_epoch1": self._validate_work(epoch1),
            "difficulty": self._get_difficulty(),
            "epoch1_difficulty": epoch1,
            "base_difficulty": base,
            "receive_difficulty": receive,
            "base_multiplier": self._calculate_multiplier(base),
            "receive_multiplier": self._calculate_multiplier(receive),
            "epoch1_multiplier": self._calculate_multiplier(epoch1)
        }

    def _get_difficulty(self, as_hex=True):
        return nl.get_work_value(
            block_hash=self.block.work_block_hash, work=self.block.work, as_hex=as_hex)

    def _validate_signature(self):
        try:
            self.block.verify_signature()
            return True
        except nl.InvalidSignature:
            return False

    def _validate_work(self, difficulty):
        try:
            self.block.verify_work(difficulty=difficulty)
            return True
        except:
            return False

    def _calculate_multiplier(self, difficulty):
        return nl.derive_work_multiplier(self._get_difficulty(), difficulty)


class BetaBlockValidator(ValidatorInterface):
    def __init__(self, block_text):
        diff = BetaDifficulty
        self.validator = get_validator(block_text, diff)

    def validate(self):
        return self.validator.validate()

    def get_block_hash(self):
        return self.validator.get_block_hash()


class LiveBlockValidator(ValidatorInterface):
    def __init__(self, block_text):
        diff = LiveDifficulty
        self.validator = get_validator(block_text, diff)

    def validate(self):
        return self.validator.validate()

    def get_block_hash(self):
        return self.validator.get_block_hash()


def get_validator(block_text, difficulty):
    json_data = json.loads(block_text)
    if "hash" in json_data and "work" not in json_data:
        return HashValidator(json_data, difficulty)
    else:
        return BlockValidator(block_text, difficulty)
