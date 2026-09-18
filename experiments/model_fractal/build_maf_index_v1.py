import hashlib
import json
from pathlib import Path

MAF = Path(
    "experiments/model_fractal/maf_representation_v1.json"
)

OUT = Path(
    "experiments/model_fractal/maf_index_v1.json"
)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if not MAF.exists():
        raise SystemExit(f"Missing MAF: {MAF}")

    maf = json.loads(
        MAF.read_text(encoding="utf-8")
    )

    index = {}

    for tensor in maf["global_tensors"]:
        name = tensor["name"]

        if name in index:
            raise SystemExit(
                f"DUPLICATE TENSOR NAME: {name}"
            )

        index[name] = {
            "index": tensor["index"],
            "type": tensor["type"],
            "dims": tensor["dims"],
            "elements": tensor["elements"],
            "offset": tensor["offset"],
            "file_start": tensor["file_start"],
            "span_bytes": tensor["span_bytes"],
            "payload_sha256": tensor["payload_sha256"],
            "decoded_elements": tensor["decoded_elements"],
        }

    for layer, tensors in maf["layers"].items():
        for tensor in tensors:
            name = tensor["name"]

            if name in index:
                raise SystemExit(
                    f"DUPLICATE TENSOR NAME: {name}"
                )

            index[name] = {
                "index": tensor["index"],
                "type": tensor["type"],
                "dims": tensor["dims"],
                "elements": tensor["elements"],
                "offset": tensor["offset"],
                "file_start": tensor["file_start"],
                "span_bytes": tensor["span_bytes"],
                "payload_sha256": tensor["payload_sha256"],
                "decoded_elements": tensor["decoded_elements"],
            }

    if len(index) != 339:
        raise SystemExit(
            f"INDEX COUNT ERROR: {len(index)}"
        )

    canonical = json.dumps(
        index,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    index_hash = sha256_bytes(canonical)

    output = {
        "format": "openmind.maf_index.v1",

        "source": {
            "path": maf["source"]["path"],
            "sha256": maf["source"]["sha256"],
            "bytes": maf["source"]["bytes"],
        },

        "representation": {
            "source_maf":
                "experiments/model_fractal/maf_representation_v1.json",
            "source_representation_sha256":
                maf["representation"][
                    "representation_sha256"
                ],
            "index_sha256": index_hash,
        },

        "tensor_count": len(index),

        "index": index,
    }

    OUT.write_text(
        json.dumps(
            output,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print(" OPENMIND / INDEXED MAF ACCESS V1")
    print("=" * 72)
    print(f"source sha256:       {maf['source']['sha256']}")
    print(f"tensor count:        {len(index)}")
    print(f"index sha256:        {index_hash}")
    print(f"output:              {OUT}")
    print()
    print("INDEXED MAF BUILD COMPLETE")


if __name__ == "__main__":
    main()
