import nano_lib_py as nl


class BlockValidator:
    def __init__(self, block: nl.Block, base_difficulty, receive_difficulty):
        self.block = block
        self.base_difficulty = base_difficulty
        self.receive_difficulty = receive_difficulty

    def validate(self):

        base = self.base_difficulty
        receive = self.receive_difficulty

        return {
            "is_signature_valid": self._validate_signature(),
            "is_work_valid_base": self._validate_work(base),
            "is_work_valid_receive": self._validate_work(receive),
            "difficulty": self._get_difficulty(),
            "base_difficulty": self.base_difficulty,
            "receive_difficulty": self.receive_difficulty,
            "base_multiplier": self._calculate_multiplier(base),
            "receive_multiplier": self._calculate_multiplier(receive)
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
        self.block = block
        self.base_difficulty = "fffff00000000000"
        self.receive_difficulty = "ffffe00000000000"
        super().__init__(block, self.base_difficulty, self.receive_difficulty)


class LiveBlockValidator(BlockValidator):
    def __init__(self, block: nl.Block):
        self.block = block
        self.base_difficulty = "fffffff800000000"
        self.receive_difficulty = "fffffe0000000000"
        super().__init__(block, self.base_difficulty, self.receive_difficulty)


def nl_get_block_hash(block: nl.Block):
    return block.block_hash


def nl_block_from_json(block):
    block = nl.Block.from_json(block, verify=False)
    return block
