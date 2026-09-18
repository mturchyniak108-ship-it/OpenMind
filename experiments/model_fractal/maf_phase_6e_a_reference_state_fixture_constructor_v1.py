#!/usr/bin/env python3
import ast
import hashlib
import json
import os
import re
import subprocess
import unicodedata

BRANCH = "labs/multidimensional-maf"
PROTOCOL_HEAD = "82b7d7cb87f7a50a2f860282a2b1c3c56eaede39"
BASELINE_COUNT = 440
BASELINE_SHA256 = "f206c0eed32daef9ed0cfaae195aa56a343a85437ebd3135aeafdb4c1ffacddd"
CONSTRUCTOR_PATH = "experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_constructor_v1.py"
OUTPUT_PATH = "experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json"

PREREG = "experiments/model_fractal/MAF_PHASE_6E_A_REFERENCE_STATE_FIXTURE_PREREGISTRATION_V1.md"
CHECKPOINT = "experiments/model_fractal/MAF_PHASE_6E_ENTRY_CHECKPOINT.md"
ARCHITECTURE = "experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md"
PROTOCOL = "experiments/model_fractal/MAF_PHASE_6E_A_REFERENCE_STATE_FIXTURE_CONSTRUCTION_PROTOCOL_V1.md"
QUERIES = "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json"
CATALOG = "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json"
TARGET_PROTOCOL = "experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_PROTOCOL.md"
TARGET_IMPL = "experiments/model_fractal/maf_query_to_pk_selection_validation_v1.py"
GEN_AUTH = "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_generation_construction_authority.json"
INVENTORY = "experiments/model_fractal/gguf_tensor_inventory_v1.json"

AUTH = {
    PREREG: "8824025988ccda4adcaa21a989b9dc9dc2a567a0ea82666de5d58e94f77f3411",
    CHECKPOINT: "1807437ea97e46a6cc687adbbe8c384dabae45a562f1d2aef6bd37e43b4bbe35",
    ARCHITECTURE: "7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c",
    PROTOCOL: "4573406d6f91f870e7a370292303fdc881a046016f2643d1dd80dc19d9d17011",
    QUERIES: "32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a",
    CATALOG: "c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900",
    TARGET_PROTOCOL: "9bea52de94d8784f6862eee9108afdd1f52f9ff4d4f95eb03fb78d5477e00c11",
    TARGET_IMPL: "e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873",
    GEN_AUTH: "a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d",
    INVENTORY: "7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee",
}
MODEL_PK = "mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
GEN_PK = "mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0"
MANIFEST_SHA = "28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3"
GGUF_SHA = "507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47"
SCHEMA = "openmind.maf_phase_6e_a_reference_state_fixture.v1"

TOP_KEYS = {"schema","fixture_version","source_model_pk","source_generation_pk","source_manifest_sha256","source_gguf_sha256","query_fixture_sha256","catalog_sha256","expected_target_protocol_sha256","expected_target_implementation_sha256","gguf_tensor_inventory_sha256","queries","objects"}
QUERY_KEYS = {"query_id","query_class","query_text_sha256","required_object_pks"}
OBJECT_KEYS = {"object_pk","tensor_name","tensor_type","dims","element_count","payload_sha256"}

def git(*args):
    return subprocess.run(("git",) + tuple(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"

def zparts(blob):
    return [x for x in blob.split(b"\0") if x]

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def head_bytes(path):
    result = git("show", "HEAD:" + path)
    need(result.returncode == 0, "cannot read frozen path: " + path)
    return result.stdout

def _normalize_query(text):
    if not isinstance(text, str):
        raise RuntimeError(
            "query must be str"
        )

    text = unicodedata.normalize(
        "NFKC",
        text,
    ).casefold()

    text = re.sub(
        r"[._/\-]",
        " ",
        text,
    )

    text = "".join(
        char
        if (
            char.isalnum()
            or char.isspace()
        )
        else " "
        for char in text
    )

    text = " ".join(
        text.split()
    )

    if not text:
        raise RuntimeError(
            "empty normalized query"
        )

    return text


def _independent_query_intent(text):
    normalized = _normalize_query(
        text
    )

    layers = set(
        int(match.group(1))
        for match in re.finditer(
            (
                r"(?:^|\s)"
                r"(?:layer|block|blk)"
                r"\s+([0-9]+)"
                r"(?:\s|$)"
            ),
            normalized,
        )
    )

    if len(layers) > 1:
        raise RuntimeError(
            "multiple distinct query layers"
        )

    layer = (
        next(iter(layers))
        if layers
        else None
    )

    words = set(
        normalized.split()
    )

    tags = set()

    if (
        "attention" in words
        or "attn" in words
    ):
        tags.add("attn")

    if (
        "query" in words
        or "q" in words
    ):
        tags.add("q")

    if (
        "key" in words
        or "k" in words
    ):
        tags.add("k")

    if (
        "value" in words
        or "v" in words
    ):
        tags.add("v")

    if (
        "feed forward" in normalized
        or "feedforward" in words
        or "ffn" in words
        or "mlp" in words
    ):
        tags.add("ffn")

    if (
        "down projection" in normalized
        or "down" in words
    ):
        tags.add("down")

    if (
        "up projection" in normalized
        or "up" in words
    ):
        tags.add("up")

    if "gate" in words:
        tags.add("gate")

    if (
        "normalization" in words
        or "norm" in words
    ):
        tags.add("norm")

    if (
        "token embedding" in normalized
        or "token embeddings" in normalized
        or "embedding" in words
        or "embeddings" in words
        or "embd" in words
    ):
        tags.add("embedding")

    if (
        "lm head" in normalized
        or "output" in words
    ):
        tags.add("output")

    return (
        layer,
        frozenset(tags),
    )


def _independent_tensor_descriptor(
    tensor_name,
):
    if not isinstance(
        tensor_name,
        str,
    ):
        raise RuntimeError(
            "tensor name must be str"
        )

    normalized = unicodedata.normalize(
        "NFKC",
        tensor_name,
    ).casefold()

    normalized = re.sub(
        r"[._/\-]",
        " ",
        normalized,
    )

    words = normalized.split()

    match = re.search(
        (
            r"(?:^|\s)"
            r"blk\s+([0-9]+)"
            r"(?:\s|$)"
        ),
        normalized,
    )

    layer = (
        int(match.group(1))
        if match
        else None
    )

    mapping = {
        "attn": "attn",
        "q": "q",
        "k": "k",
        "v": "v",
        "ffn": "ffn",
        "down": "down",
        "up": "up",
        "gate": "gate",
        "norm": "norm",
        "embd": "embedding",
        "embedding": "embedding",
        "embeddings": "embedding",
        "output": "output",
    }

    tags = frozenset(
        mapping[word]
        for word in words
        if word in mapping
    )

    return (
        layer,
        tags,
    )


def _independent_targets(
    query_text,
    catalog_entries,
):
    (
        query_layer,
        query_tags,
    ) = _independent_query_intent(
        query_text
    )

    if (
        query_layer is None
        and not query_tags
    ):
        return tuple()

    output = []

    for entry in catalog_entries:
        (
            candidate_layer,
            candidate_tags,
        ) = _independent_tensor_descriptor(
            entry["tensor_name"]
        )

        if (
            query_layer is not None
            and candidate_layer
            != query_layer
        ):
            continue

        if not query_tags.issubset(
            candidate_tags
        ):
            continue

        output.append(
            entry["object_pk"]
        )

    return tuple(output)

def funcs(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

def static_boundary():
    source = head_bytes(CONSTRUCTOR_PATH).decode("utf-8")
    tree = ast.parse(source, filename=CONSTRUCTOR_PATH)
    fm = funcs(tree)
    imports = set()
    import_from = False
    subprocess_ok = True
    os_escape_ok = True
    forbidden_ok = True
    git_literal_ok = True
    forbidden = {"generate","inference","infer","llama","matmul","forward","maf_native","native_compute","tensor_compute","socket","connect","request","urlopen"}

    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.update(a.name.split(".", 1)[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            import_from = True

    for fname, fnode in fm.items():
        for node in ast.walk(fnode):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                    subprocess_ok = subprocess_ok and fname in {"git","load_docs_a","load_docs_b"} and node.func.attr == "run"
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    os_escape_ok = os_escape_ok and node.func.attr not in {"system","popen","spawnl","spawnlp","spawnv","spawnvp"}
            name = node.func.id.casefold() if isinstance(node.func, ast.Name) else node.func.attr.casefold() if isinstance(node.func, ast.Attribute) else ""
            forbidden_ok = forbidden_ok and not any(term in name for term in forbidden)
            if isinstance(node.func, ast.Name) and node.func.id == "git":
                git_literal_ok = git_literal_ok and bool(node.args) and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str)

    a = fm.get("build_a")
    b = fm.get("build_b")
    distinct = a is not None and b is not None and ast.dump(a, include_attributes=False) != ast.dump(b, include_attributes=False)
    return all([
        imports == {"ast","hashlib","json","os","re","subprocess","unicodedata"},
        not import_from,
        subprocess_ok,
        os_escape_ok,
        forbidden_ok,
        git_literal_ok,
        distinct,
    ])

def preflight():
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    parent = git("rev-parse", "HEAD^")
    dirty = git("diff", "--name-only", "-z")
    staged = git("diff", "--cached", "--name-only", "-z")
    untracked = git("ls-files", "-z", "--others", "--exclude-standard")
    scope = git("diff-tree", "--no-commit-id", "--name-status", "-r", "-z", "HEAD^", "HEAD")
    frozen = git("show", "HEAD:" + CONSTRUCTOR_PATH)
    need(all(r.returncode == 0 for r in [branch,head,parent,dirty,staged,untracked,scope,frozen]), "repository read failure")
    need(branch.stdout.decode().strip() == BRANCH, "branch mismatch")
    head_value = head.stdout.decode().strip()
    need(head_value != PROTOCOL_HEAD, "constructor not frozen")
    need(parent.stdout.decode().strip() == PROTOCOL_HEAD, "constructor parent mismatch")
    need(zparts(scope.stdout) == [b"A", CONSTRUCTOR_PATH.encode()], "constructor commit scope mismatch")
    need(not zparts(dirty.stdout), "tracked worktree dirty")
    need(not zparts(staged.stdout), "index not empty")
    need(len(zparts(untracked.stdout)) == BASELINE_COUNT and sha(untracked.stdout) == BASELINE_SHA256, "untracked baseline mismatch")
    with open(CONSTRUCTOR_PATH, "rb") as handle:
        local = handle.read()
    need(local == frozen.stdout, "constructor worktree differs from frozen blob")
    need(not os.path.lexists(OUTPUT_PATH), "fixture output already exists")
    return head_value

def need_a(ok, message):
    if not ok:
        raise RuntimeError("A: " + message)

def need_b(ok, message):
    if not ok:
        raise RuntimeError("B: " + message)

def load_docs_a():
    docs = {}
    for path, expected in AUTH.items():
        result = subprocess.run(("git","show","HEAD:" + path), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        need_a(result.returncode == 0, "authority read failure: " + path)
        need_a(sha(result.stdout) == expected, "authority SHA mismatch: " + path)
        docs[path] = result.stdout
    return docs

def load_docs_b():
    docs = dict()
    for path in sorted(AUTH.keys()):
        result = subprocess.run(["git","show","HEAD:" + path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        need_b(result.returncode == 0, "authority read failure: " + path)
        expected = AUTH.get(path)
        actual = hashlib.sha256(bytes(result.stdout)).hexdigest()
        need_b(actual == expected, "authority SHA mismatch: " + path)
        docs[path] = bytes(result.stdout)
    return docs

def build_a(docs):
    qd = json.loads(docs[QUERIES].decode())
    cd = json.loads(docs[CATALOG].decode())
    gd = json.loads(docs[GEN_AUTH].decode())
    inv = json.loads(docs[INVENTORY].decode())
    qs, cs, gs, ts = qd["queries"], cd["entries"], gd["targets"], inv["tensors"]
    need_a((len(qs),len(cs),len(gs),len(ts)) == (40,12,12,339), "A source counts mismatch")
    need_a(qd["source_generation_pk"] == GEN_PK and cd["source_generation_pk"] == GEN_PK, "A generation mismatch")
    need_a(qd["source_manifest_sha256"] == MANIFEST_SHA and cd["source_manifest_sha256"] == MANIFEST_SHA, "A manifest mismatch")
    need_a(gd["bindings"]["model_pk"] == MODEL_PK, "A model mismatch")
    need_a(gd["bindings"]["source_gguf"]["sha256"] == GGUF_SHA and inv["source"]["sha256"] == GGUF_SHA, "A GGUF mismatch")

    cpk = {x["object_pk"]: x for x in cs}
    gpk = {x["object_pk"]: x for x in gs}
    need_a(len(cpk) == 12 and len(gpk) == 12 and set(cpk) == set(gpk), "A object authority mismatch")
    by_name = {}
    for x in ts:
        by_name.setdefault(x["name"], []).append(x)

    classes = {"specific_intent":0,"multi_target_intent":0,"fallback_control":0}
    specific = set()
    required = set()
    outq = []
    for i, q in enumerate(qs, 1):
        need_a(set(q) == {"query_class","query_id","query_text"}, "A query keys mismatch")
        need_a(q["query_id"] == "q{:03d}".format(i), "A query order mismatch")
        need_a(q["query_class"] in classes and isinstance(q["query_text"], str) and bool(q["query_text"]), "A query invalid")
        classes[q["query_class"]] += 1
        targets = sorted(_independent_targets(q["query_text"], cs))
        if q["query_class"] == "specific_intent":
            need_a(len(targets) == 1, "A specific cardinality")
            specific.add(targets[0])
        elif q["query_class"] == "multi_target_intent":
            need_a(len(targets) >= 2, "A multi cardinality")
        else:
            need_a(len(targets) == 0, "A fallback cardinality")
        need_a(all(pk in cpk for pk in targets), "A catalog membership")
        required.update(targets)
        row = {"query_id":q["query_id"],"query_class":q["query_class"],"query_text_sha256":sha(q["query_text"].encode()),"required_object_pks":targets}
        need_a(set(row) == QUERY_KEYS and row["required_object_pks"] == sorted(row["required_object_pks"]), "A query output invalid")
        outq.append(row)

    need_a(classes == {"specific_intent":24,"multi_target_intent":8,"fallback_control":8}, "A class counts")
    need_a(len(specific) == 12, "A unique specific count")
    objects = []
    for pk in sorted(required):
        c, g = cpk[pk], gpk[pk]
        match = by_name.get(g["tensor_name"], [])
        need_a(len(match) == 1, "A inventory uniqueness")
        t = match[0]
        need_a(c["tensor_name"] == g["tensor_name"] and c["tensor_type"] == g["catalog_tensor_type"] and c["dims"] == g["dims"] and c["element_count"] == g["element_count"], "A catalog metadata")
        need_a(t["type"] == g["tensor_type_name"] and t["dims"] == g["dims"] and t["elements"] == g["element_count"], "A inventory metadata")
        payload = t["payload_sha256"]
        need_a(isinstance(payload, str) and re.fullmatch(r"[0-9a-f]{64}", payload) is not None, "A payload SHA")
        row = {"object_pk":pk,"tensor_name":g["tensor_name"],"tensor_type":g["tensor_type_name"],"dims":g["dims"],"element_count":g["element_count"],"payload_sha256":payload}
        need_a(set(row) == OBJECT_KEYS, "A object output keys")
        objects.append(row)
    need_a([x["object_pk"] for x in objects] == sorted(x["object_pk"] for x in objects), "A object order")
    fixture = {
        "schema": SCHEMA,
        "fixture_version": 1,
        "source_model_pk": MODEL_PK,
        "source_generation_pk": GEN_PK,
        "source_manifest_sha256": MANIFEST_SHA,
        "source_gguf_sha256": GGUF_SHA,
        "query_fixture_sha256": AUTH[QUERIES],
        "catalog_sha256": AUTH[CATALOG],
        "expected_target_protocol_sha256": AUTH[TARGET_PROTOCOL],
        "expected_target_implementation_sha256": AUTH[TARGET_IMPL],
        "gguf_tensor_inventory_sha256": AUTH[INVENTORY],
        "queries": outq,
        "objects": objects,
    }
    need_a(set(fixture) == TOP_KEYS, "top schema mismatch")
    return fixture

def build_b(docs):
    qd = json.loads(bytes(docs[QUERIES]).decode("utf-8"))
    cd = json.loads(bytes(docs[CATALOG]).decode("utf-8"))
    gd = json.loads(bytes(docs[GEN_AUTH]).decode("utf-8"))
    inv = json.loads(bytes(docs[INVENTORY]).decode("utf-8"))
    qs = list(qd.get("queries", []))
    cs = list(cd.get("entries", []))
    gs = list(gd.get("targets", []))
    ts = list(inv.get("tensors", []))
    need_b((len(qs),len(cs),len(gs),len(ts)) == (40,12,12,339), "B source counts mismatch")
    need_b(qd.get("source_generation_pk") == GEN_PK and cd.get("source_generation_pk") == GEN_PK, "B generation mismatch")
    need_b(qd.get("source_manifest_sha256") == MANIFEST_SHA and cd.get("source_manifest_sha256") == MANIFEST_SHA, "B manifest mismatch")
    need_b(gd.get("bindings",{}).get("model_pk") == MODEL_PK, "B model mismatch")
    need_b(gd.get("bindings",{}).get("source_gguf",{}).get("sha256") == GGUF_SHA and inv.get("source",{}).get("sha256") == GGUF_SHA, "B GGUF mismatch")

    classes = []
    specific = set()
    required = set()
    outq = []
    for offset in range(40):
        q = qs[offset]
        qid = "q{:03d}".format(offset + 1)
        need_b(sorted(q.keys()) == ["query_class","query_id","query_text"], "B query keys mismatch")
        need_b(q.get("query_id") == qid, "B query order mismatch")
        qc, text = q.get("query_class"), q.get("query_text")
        need_b(qc in {"specific_intent","multi_target_intent","fallback_control"} and isinstance(text, str) and len(text) > 0, "B query invalid")
        classes.append(qc)
        targets = list(_independent_targets(text, cs))
        targets.sort()
        if qc == "specific_intent":
            need_b(len(targets) == 1, "B specific cardinality")
            specific.update(targets)
        if qc == "multi_target_intent":
            need_b(len(targets) >= 2, "B multi cardinality")
        if qc == "fallback_control":
            need_b(targets == [], "B fallback cardinality")
        for pk in targets:
            need_b(sum(1 for item in cs if item.get("object_pk") == pk) == 1, "B catalog membership")
        required.update(targets)
        row = {"query_id":qid,"query_class":qc,"query_text_sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),"required_object_pks":list(targets)}
        need_b(sorted(row.keys()) == sorted(QUERY_KEYS) and row["required_object_pks"] == sorted(row["required_object_pks"]), "B query output invalid")
        outq.append(row)

    need_b(classes.count("specific_intent") == 24 and classes.count("multi_target_intent") == 8 and classes.count("fallback_control") == 8, "B class counts")
    need_b(len(specific) == 12, "B unique specific count")

    objects = []
    for pk in sorted(list(required)):
        cm = [x for x in cs if x.get("object_pk") == pk]
        gm = [x for x in gs if x.get("object_pk") == pk]
        need_b(len(cm) == 1 and len(gm) == 1, "B object authority")
        c, g = cm[0], gm[0]
        tm = [x for x in ts if x.get("name") == g.get("tensor_name")]
        need_b(len(tm) == 1, "B inventory uniqueness")
        t = tm[0]
        need_b(all([
            c.get("tensor_name") == g.get("tensor_name"),
            c.get("tensor_type") == g.get("catalog_tensor_type"),
            c.get("dims") == g.get("dims"),
            c.get("element_count") == g.get("element_count"),
            t.get("type") == g.get("tensor_type_name"),
            t.get("dims") == g.get("dims"),
            t.get("elements") == g.get("element_count"),
        ]), "B metadata mismatch")
        payload = t.get("payload_sha256")
        need_b(isinstance(payload, str) and len(payload) == 64 and all(ch in "0123456789abcdef" for ch in payload), "B payload SHA")
        row = {"object_pk":pk,"tensor_name":g.get("tensor_name"),"tensor_type":g.get("tensor_type_name"),"dims":g.get("dims"),"element_count":g.get("element_count"),"payload_sha256":payload}
        need_b(sorted(row.keys()) == sorted(OBJECT_KEYS), "B object output keys")
        objects.append(row)

    order = [x.get("object_pk") for x in objects]
    need_b(order == sorted(order) and len(order) == len(set(order)), "B object order or uniqueness")
    fixture = dict()
    fixture["schema"] = SCHEMA
    fixture["fixture_version"] = 1
    fixture["source_model_pk"] = MODEL_PK
    fixture["source_generation_pk"] = GEN_PK
    fixture["source_manifest_sha256"] = MANIFEST_SHA
    fixture["source_gguf_sha256"] = GGUF_SHA
    fixture["query_fixture_sha256"] = AUTH.get(QUERIES)
    fixture["catalog_sha256"] = AUTH.get(CATALOG)
    fixture["expected_target_protocol_sha256"] = AUTH.get(TARGET_PROTOCOL)
    fixture["expected_target_implementation_sha256"] = AUTH.get(TARGET_IMPL)
    fixture["gguf_tensor_inventory_sha256"] = AUTH.get(INVENTORY)
    fixture["queries"] = outq
    fixture["objects"] = objects
    need_b(sorted(fixture.keys()) == sorted(TOP_KEYS), "top schema mismatch")
    return fixture

def policy_a(value):
    need_a(set(value) == TOP_KEYS, "fixture top keys invalid")
    need_a(all(set(x) == QUERY_KEYS for x in value["queries"]), "fixture query keys invalid")
    need_a(all(set(x) == OBJECT_KEYS for x in value["objects"]), "fixture object keys invalid")
    keys = []
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            for key, child in item.items():
                keys.append(str(key).casefold())
                stack.append(child)
        elif isinstance(item, list):
            stack.extend(item)
    need_a(not any(k in {"selected_object_pks","selector_rank","selector_score","selector_hit","selector_success"} for k in keys), "selector state present")
    need_a(not any(term in key for key in keys for term in {"sufficiency","fidelity","avoidance","performance"}), "science result present")

def policy_b(value):
    need_b(sorted(value.keys()) == sorted(TOP_KEYS), "fixture top keys invalid")
    for row in value.get("queries", []):
        need_b(sorted(row.keys()) == sorted(QUERY_KEYS), "fixture query keys invalid")
    for row in value.get("objects", []):
        need_b(sorted(row.keys()) == sorted(OBJECT_KEYS), "fixture object keys invalid")
    forbidden_exact = {"selected_object_pks","selector_rank","selector_score","selector_hit","selector_success"}
    forbidden_terms = ("sufficiency","fidelity","avoidance","performance")
    pending = [value]
    while pending:
        item = pending.pop(0)
        if isinstance(item, dict):
            for key in item:
                folded = str(key).casefold()
                need_b(folded not in forbidden_exact, "selector state present")
                need_b(not any(term in folded for term in forbidden_terms), "science result present")
                pending.append(item[key])
        elif isinstance(item, list):
            pending.extend(item)

def rf_labels(raw):
    found = re.findall(r"^(RF[0-9]{2})[ \t]*[—:-][ \t]*(.+)$", raw.decode("utf-8"), re.M)
    need([x[0] for x in found] == ["RF{:02d}".format(i) for i in range(1,31)], "RF labels invalid")
    return dict(found)

def verify_post_write(expected):
    with open(OUTPUT_PATH, "rb") as handle:
        need(handle.read() == expected, "fixture reread mismatch")
    dirty = git("diff", "--name-only", "-z")
    staged = git("diff", "--cached", "--name-only", "-z")
    untracked = git("ls-files", "-z", "--others", "--exclude-standard")
    need(all(r.returncode == 0 for r in [dirty,staged,untracked]), "post-write Git failure")
    need(not zparts(dirty.stdout) and not zparts(staged.stdout), "post-write tracked/index mutation")
    items = zparts(untracked.stdout)
    output_b = OUTPUT_PATH.encode()
    need(sum(1 for x in items if x == output_b) == 1, "fixture untracked identity")
    baseline = [x for x in items if x != output_b]
    blob = b"\0".join(baseline) + (b"\0" if baseline else b"")
    need(len(baseline) == BASELINE_COUNT and sha(blob) == BASELINE_SHA256, "post-write baseline mismatch")

def rollback_verified():
    dirty = git("diff", "--name-only", "-z")
    staged = git("diff", "--cached", "--name-only", "-z")
    untracked = git("ls-files", "-z", "--others", "--exclude-standard")
    return all([
        dirty.returncode == 0,
        staged.returncode == 0,
        untracked.returncode == 0,
        not os.path.lexists(OUTPUT_PATH),
        not zparts(dirty.stdout),
        not zparts(staged.stdout),
        len(zparts(untracked.stdout)) == BASELINE_COUNT,
        sha(untracked.stdout) == BASELINE_SHA256,
    ])

def main():
    created = False
    rollback_ok = True
    try:
        head = preflight()
        need(static_boundary(), "static execution boundary failed")
        docs_a = load_docs_a()
        fixture_a = build_a(docs_a)
        policy_a(fixture_a)
        bytes_a = canonical(fixture_a)

        docs_b = load_docs_b()
        fixture_b = build_b(docs_b)
        policy_b(fixture_b)
        bytes_b = canonical(fixture_b)

        need(fixture_a == fixture_b, "A/B fixture mismatch")
        need(bytes_a == bytes_b, "A/B byte mismatch")
        labels = rf_labels(docs_a[PREREG])

        fd = os.open(OUTPUT_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        created = True
        with os.fdopen(fd, "wb") as handle:
            handle.write(bytes_a)
            handle.flush()
            os.fsync(handle.fileno())
        verify_post_write(bytes_a)

        print()
        print("🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨")
        print("PHASE 6E-A REFERENCE-STATE FIXTURE V1 — CONSTRUCTION")
        print()
        print("[ FROZEN CONSTRUCTION AUTHORITY ]")
        print("  Constructor HEAD               : " + head)
        print("  Constructor parent             : " + PROTOCOL_HEAD)
        print("  Independent A/B builders       : PASS")
        print("  Static execution boundary      : PASS")
        print("  Selector executed              : NO")
        print()
        print("[ RF01-RF30 ]")
        for i in range(1,31):
            key = "RF{:02d}".format(i)
            print("  {} : PASS — {}".format(key, labels[key].strip()))
        print()
        print("[ FIXTURE IDENTITY ]")
        print("  Path                           : " + OUTPUT_PATH)
        print("  Bytes                          : " + str(len(bytes_a)))
        print("  SHA256                         : " + sha(bytes_a))
        print("  Independent reconstruction     : PASS")
        print("  Post-write verification        : PASS")
        print()
        print("[ AUTHORIZATION BOUNDARY ]")
        print("  Fixture constructed            : YES")
        print("  Phase 6E-A sufficiency science : NO")
        print("  Bounded expansion              : NO")
        print("  Inference                      : NO")
        print("  MAF-native compute             : NO")
        print("  Network access                 : NO")
        print("  Git staging                    : NO")
        print("  Commit created                 : NO")
        print()
        print("🟨🟨🟨 PASTE BACK TO CHAT FROM HERE 🟨🟨🟨")
        return True
    except Exception as exc:
        if created and os.path.lexists(OUTPUT_PATH):
            try:
                os.unlink(OUTPUT_PATH)
            except Exception:
                rollback_ok = False
        rollback_ok = rollback_ok and rollback_verified()
        print()
        print("🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨")
        print("PHASE 6E-A REFERENCE-STATE FIXTURE V1 — CONSTRUCTION")
        print()
        print("[ DISPOSITION ]")
        print("  Construction verdict           : FAIL")
        print("  Error                          : " + type(exc).__name__ + ": " + str(exc))
        print("  Rollback verified              : " + ("PASS" if rollback_ok else "FAIL"))
        print("  Fixture preserved              : NO")
        print("  Phase 6E-A science             : NO")
        print("  Network access                 : NO")
        print("  Git staging                    : NO")
        print("  Commit created                 : NO")
        print()
        print("🟨🟨🟨 PASTE BACK TO CHAT FROM HERE 🟨🟨🟨")
        return False

if __name__ == "__main__":
    raise SystemExit(0 if main() else 2)
