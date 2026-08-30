import numpy as np


Q8_BLOCK_SIZE = 32


def q8_0_block_count(n):
    if n % Q8_BLOCK_SIZE != 0:
        raise ValueError(
            f"Q8_0 tensor dimension {n} is not divisible by "
            f"block size {Q8_BLOCK_SIZE}"
        )
    return n // Q8_BLOCK_SIZE


def q8_0_size(n):
    """
    Q8_0 block:

        fp16 scale = 2 bytes
        32 int8 values = 32 bytes

    Total = 34 bytes/block.
    """
    return q8_0_block_count(n) * 34


def describe_q8_0(tensor):
    shape = tuple(int(x) for x in tensor.shape)

    return {
        "shape": shape,
        "raw_bytes": int(tensor.data.nbytes),
        "elements": int(np.prod(shape)),
        "expected_q8_bytes": q8_0_size(shape[0]),
        "blocks": q8_0_block_count(shape[0]),
    }
