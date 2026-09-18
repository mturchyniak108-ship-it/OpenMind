import hashlib
import json
from pathlib import Path

INVENTORY = Path(
    "experiments/model_fractal/gguf_tensor_inventory_v1.json"
)

OUT = Path(
    "experiments/model_fractal/maf_representation_v1.json"
)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def layer_from_name(name):
    if name.startswith("blk."):
        parts = name.split(".")
        if len(parts) >= 2 and parts[1].isdigit():
            return int(parts[1])
    return None


def component_from_name(name):
    if name.startswith("blk."):
        parts = name.split(".")
        if len(parts) >= 3:
            return ".".join(parts[2:])
    return name


def main():
    if not INVENTORY.exists():
        raise SystemExit(
            f"Missing inventory: {INVENTORY}"
        )

    inventory = json.loads(
        INVENTORY.read_text(encoding="utf-8")
    )

    tensors = inventory["tensors"]

    if len(tensors) != 339:
        raise SystemExit(
            f"Unexpected tensor count: {len(tensors)}"
        )

    layers = {}
    globals_ = []

    for t in tensors:
        name = t["name"]
        layer = layer_from_name(name)

        node = {
            "index": int(t["index"]),
            "name": name,
            "type": t["type"],
            "dims": list(t["dims"]),
            "elements": int(t["elements"]),
            "offset": int(t["offset"]),
            "file_start": int(t["file_start"]),
            "span_bytes": int(t["span_bytes"]),
            "payload_sha256": t["payload_sha256"],
            "decoded_elements": int(
                t["decoded_elements"]
            ),
        }

        if layer is None:
            globals_.append(node)
        else:
            layers.setdefault(
                str(layer),
                []
            ).append(node)

    for layer in layers:
        layers[layer].sort(
            key=lambda x: (
                x["file_start"],
                x["name"],
            )
        )

    globals_.sort(
        key=lambda x: (
            x["file_start"],
            x["name"],
        )
    )

    layer_ids = sorted(
        int(x) for x in layers
    )

    if layer_ids != list(range(28)):
        raise SystemExit(
            f"Unexpected layer IDs: {layer_ids}"
        )

    component_counts = {
        layer: len(layers[layer])
        for layer in sorted(
            layers,
            key=lambda x: int(x)
        )
    }

    if any(
        count != 12
        for count in component_counts.values()
    ):
        raise SystemExit(
            f"Unexpected layer component counts: "
            f"{component_counts}"
        )

    canonical = {
        "source_sha256": inventory["source"]["sha256"],
        "gguf": inventory["gguf"],
        "tensor_type_counts": inventory["tensor_type_counts"],
        "globals": globals_,
        "layers": {
            layer: layers[layer]
            for layer in sorted(
                layers,
                key=lambda x: int(x)
            )
        },
    }

    canonical_bytes = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    representation_hash = sha256_bytes(
        canonical_bytes
    )

    output = {
        "format": "openmind.maf_representation.v1",
        "representation": {
            "kind": "deterministic_tensor_index",
            "lossless": True,
            "payload_embedded": False,
            "source_manifest": str(INVENTORY),
            "source_sha256": inventory["source"]["sha256"],
            "representation_sha256": representation_hash,
        },
        "source": inventory["source"],
        "gguf": inventory["gguf"],
        "tensor_type_counts": inventory[
            "tensor_type_counts"
        ],
        "layer_count": len(layer_ids),
        "layer_ids": layer_ids,
        "layer_component_counts": component_counts,
        "global_tensors": globals_,
        "layers": {
            layer: layers[layer]
            for layer in sorted(
                layers,
                key=lambda x: int(x)
            )
        },
    }

    OUT.write_text(
        json.dumps(
            output,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print(" OPENMIND / DETERMINISTIC MAF REPRESENTATION V1")
    print("=" * 72)
    print(f"source sha256:       {inventory['source']['sha256']}")
    print(f"tensor count:        {len(tensors)}")
    print(f"layer count:         {len(layer_ids)}")
    print(f"global tensors:      {len(globals_)}")
    print(f"F32 tensors:         {inventory['tensor_type_counts']['F32']}")
    print(f"Q8_0 tensors:        {inventory['tensor_type_counts']['Q8_0']}")
    print(f"representation sha:  {representation_hash}")
    print(f"output:              {OUT}")
    print()
    print("MAF REPRESENTATION BUILD COMPLETE")


if __name__ == "__main__":
    main()
