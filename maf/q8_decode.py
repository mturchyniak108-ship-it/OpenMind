import numpy as np


Q8_0 = 8
QK = 32
BLOCK_BYTES = 34


def decode_q8_0(data):
    """
    Decode raw GGUF Q8_0 storage.

    Each block:
        fp16 scale : 2 bytes
        int8 values: 32 bytes

    Returns float32 values.
    """

    raw = np.asarray(data, dtype=np.uint8).reshape(-1)

    if raw.size % BLOCK_BYTES != 0:
        raise ValueError(
            f"Q8_0 storage size {raw.size} is not divisible "
            f"by block size {BLOCK_BYTES}"
        )

    blocks = raw.reshape(-1, BLOCK_BYTES)

    scales = blocks[:, :2].copy().view(np.float16).astype(np.float32)
    values = blocks[:, 2:].view(np.int8).astype(np.float32)

    decoded = values * scales

    return decoded.reshape(-1)


def decode_tensor(tensor):
    if int(tensor.tensor_type) != Q8_0:
        raise ValueError(
            f"{tensor.name} is type {int(tensor.tensor_type)}, "
            f"not Q8_0"
        )

    values = decode_q8_0(tensor.data)

    expected = int(np.prod(tuple(int(x) for x in tensor.shape)))

    if values.size != expected:
        raise ValueError(
            f"{tensor.name}: decoded {values.size} values, "
            f"expected {expected}"
        )

    return values.reshape(tuple(int(x) for x in tensor.shape))
