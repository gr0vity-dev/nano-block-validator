import nano_lib_py as nl


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


class BlockValidator:
    def __init__(self, block: nl.Block, difficulty: NanoBlockDifficulty):
        self.difficulty = difficulty
        self.block = block

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


class BetaBlockValidator(BlockValidator):
    def __init__(self, block: nl.Block):
        diff = BetaDifficulty
        super().__init__(block, diff)


class LiveBlockValidator(BlockValidator):
    def __init__(self, block: nl.Block):
        diff = LiveDifficulty
        super().__init__(block, diff)


def nl_get_block_hash(block: nl.Block):
    return block.block_hash


def nl_block_from_json(block):
    block = nl.Block.from_json(block, verify=False)
    return block
