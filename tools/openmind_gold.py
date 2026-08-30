#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


PS = "🟡⏱️ ===== PASTE BACK TO CHAT FROM HERE ===== ⏱️🟡"
PE = "🟡⏱️ ===== END PASTE-BACK SECTION ===== ⏱️🟡"

GS = "🟨📦 ===== GOLD STANDARD RETURN PACKET ===== 📦🟨"
GE = "🟨📦 ===== END GOLD STANDARD RETURN PACKET ===== 📦🟨"


def run(*args, cwd=None, text=True):
    return subprocess.run(
        list(args),
        cwd=cwd,
        capture_output=True,
        text=text,
    )


def sha_bytes(data):
    return hashlib.sha256(
        data
    ).hexdigest()


def sha_file(path):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        for chunk in iter(
            lambda: f.read(
                8 * 1024 * 1024
            ),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def packet(
    status,
    fields,
    classification,
    next_gate,
    failures=None,
):
    failures = failures or []

    print()
    print(PS)

    print()
    print(GS)

    print(
        "STATUS        :",
        status,
    )

    for key, value in fields:
        print(
            f"{key:<14}:",
            value,
        )

    print(
        "FAILS         :",
        len(failures),
    )

    print(
        "FIRST FAILURE :",
        failures[0]
        if failures
        else "NONE",
    )

    print(
        "CLASSIFICATION:",
        classification,
    )

    print(
        "NEXT GATE     :",
        next_gate,
    )

    print(GE)

    if failures:
        print()
        print(
            "===== FAILURE-FOCUSED CHECKS ====="
        )

        for item in failures:
            print(item)

    print()
    print(PE)


def untracked(repo):
    proc = run(
        "git",
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
        cwd=repo,
        text=False,
    )

    if proc.returncode:
        return (
            proc.returncode,
            [],
            None,
        )

    paths = sorted(
        os.fsdecode(item)
        for item in proc.stdout.split(b"\0")
        if item
    )

    payload = b"\0".join(
        os.fsencode(path)
        for path in paths
    )

    return (
        0,
        paths,
        sha_bytes(payload),
    )


def remote_head(
    repo,
    branch,
):
    proc = run(
        "git",
        "ls-remote",
        "--heads",
        "origin",
        f"refs/heads/{branch}",
        cwd=repo,
    )

    if proc.returncode:
        return None

    lines = [
        line
        for line in proc.stdout.splitlines()
        if line.strip()
    ]

    if len(lines) != 1:
        return None

    parts = lines[0].split()

    return (
        parts[0]
        if len(parts) == 2
        else None
    )


def audit_block(path):
    failures = []
    py_blocks = 0

    try:
        text = path.read_text(
            encoding="utf-8"
        )

    except Exception as exc:
        return (
            [
                f"read_error:"
                f"{type(exc).__name__}:"
                f"{exc}"
            ],
            0,
        )

    if (
        "`" * 3
    ) in text:
        failures.append(
            "nested_markdown_fence"
        )

    for number, line in enumerate(
        text.splitlines(),
        1,
    ):
        if re.match(
            r"^\s*(?:exit|logout)\b",
            line,
        ):
            failures.append(
                f"session_terminator:"
                f"{number}"
            )

        if re.search(
            (
                r"(^|[;&|]\s*)"
                r"git\s+add\s+"
                r"(?:-A|--all|\.)"
                r"\s*(?:$|[;&|])"
            ),
            line,
        ):
            failures.append(
                f"broad_git_add:"
                f"{number}"
            )

    shell = run(
        "bash",
        "-n",
        str(path),
    )

    if shell.returncode:
        detail = (
            shell.stderr
            or shell.stdout
        ).strip().replace(
            "\n",
            " | ",
        )

        failures.append(
            "bash_syntax:"
            + detail
        )

    lines = text.splitlines()

    opener = re.compile(
        (
            r"^\s*"
            r"(?:python|python3)"
            r"(?:\s+[^<\n]*)?"
            r"\s+<<-?\s*"
            r"(['\"]?)"
            r"([A-Za-z_]"
            r"[A-Za-z0-9_]*)"
            r"\1\s*$"
        )
    )

    index = 0

    while index < len(lines):
        match = opener.match(
            lines[index]
        )

        if not match:
            index += 1
            continue

        tag = match.group(2)
        start = index + 1
        end = start

        while (
            end < len(lines)
            and lines[end] != tag
        ):
            end += 1

        if end >= len(lines):
            failures.append(
                f"python_heredoc_unclosed:"
                f"{index + 1}:"
                f"{tag}"
            )
            break

        py_blocks += 1

        source = (
            "\n".join(
                lines[start:end]
            )
            + "\n"
        )

        try:
            compile(
                source,
                f"{path}:{index + 1}",
                "exec",
            )

        except SyntaxError as exc:
            failures.append(
                f"python_compile:"
                f"{index + 1}:"
                f"{exc.lineno}:"
                f"{exc.msg}"
            )

        index = end + 1

    return (
        failures,
        py_blocks,
    )


def cmd_block(args):
    path = Path(
        args.path
    ).expanduser().resolve()

    failures, count = (
        audit_block(path)
    )

    packet(
        "GOLD STANDARD BLOCK AUDIT",
        [
            (
                "FILE",
                path,
            ),
            (
                "SHA256",
                sha_file(path)
                if path.is_file()
                else None,
            ),
            (
                "PY HEREDOCS",
                count,
            ),
        ],
        (
            "BLOCK_CLEAN"
            if not failures
            else "BLOCK_BLOCKED"
        ),
        (
            "EXECUTION MAY PROCEED"
            if not failures
            else
            "FIX FIRST FAILURE BEFORE EXECUTION"
        ),
        failures,
    )

    return (
        0
        if not failures
        else 2
    )


def cmd_repo(args):
    repo = Path(
        args.repo
    ).expanduser().resolve()

    failures = []

    branch = run(
        "git",
        "branch",
        "--show-current",
        cwd=repo,
    ).stdout.strip()

    head = run(
        "git",
        "rev-parse",
        "HEAD",
        cwd=repo,
    ).stdout.strip()

    if (
        args.branch
        and branch
        != args.branch
    ):
        failures.append(
            f"branch:{branch}"
        )

    if (
        args.head
        and head
        != args.head
    ):
        failures.append(
            f"head:{head}"
        )

    if run(
        "git",
        "diff",
        "--cached",
        "--quiet",
        cwd=repo,
    ).returncode:
        failures.append(
            "staging_not_empty"
        )

    if run(
        "git",
        "diff",
        "--quiet",
        cwd=repo,
    ).returncode:
        failures.append(
            "tracked_worktree_dirty"
        )

    rc, paths, inventory_sha = (
        untracked(repo)
    )

    if rc:
        failures.append(
            "untracked_inventory_error"
        )

    if (
        args.untracked_count
        is not None
        and len(paths)
        != args.untracked_count
    ):
        failures.append(
            f"untracked_count:"
            f"{len(paths)}"
        )

    if (
        args.untracked_sha
        and inventory_sha
        != args.untracked_sha
    ):
        failures.append(
            f"untracked_sha:"
            f"{inventory_sha}"
        )

    hooks_dir = run(
        "git",
        "rev-parse",
        "--git-path",
        "hooks",
        cwd=repo,
    ).stdout.strip()

    executable = []

    for name in (
        "pre-commit",
        "commit-msg",
        "pre-push",
    ):
        path = (
            Path(hooks_dir)
            / name
        )

        if (
            path.is_file()
            and os.access(
                path,
                os.X_OK,
            )
        ):
            executable.append(
                str(path)
            )

    if (
        executable
        and not args.allow_hooks
    ):
        failures.append(
            "executable_hooks:"
            + ",".join(
                executable
            )
        )

    remote = (
        remote_head(
            repo,
            args.remote_branch,
        )
        if args.remote_branch
        else None
    )

    if (
        args.remote_head
        and remote
        != args.remote_head
    ):
        failures.append(
            f"remote_head:"
            f"{remote}"
        )

    packet(
        "GOLD STANDARD REPOSITORY AUTHORITY",
        [
            (
                "REPO",
                repo,
            ),
            (
                "BRANCH",
                branch,
            ),
            (
                "HEAD",
                head,
            ),
            (
                "UNTRACKED",
                len(paths),
            ),
            (
                "UNTRACKED SHA",
                inventory_sha,
            ),
            (
                "REMOTE",
                remote,
            ),
        ],
        (
            "REPO_AUTHORITY_CLEAN"
            if not failures
            else
            "REPO_AUTHORITY_BLOCKED"
        ),
        (
            "OPERATION MAY PROCEED"
            if not failures
            else
            "AUDIT FIRST FAILURE ONLY"
        ),
        failures,
    )

    return (
        0
        if not failures
        else 2
    )


def cmd_snapshot(args):
    repo = Path(
        args.repo
    ).expanduser().resolve()

    branch = run(
        "git",
        "branch",
        "--show-current",
        cwd=repo,
    ).stdout.strip()

    head = run(
        "git",
        "rev-parse",
        "HEAD",
        cwd=repo,
    ).stdout.strip()

    rc, paths, inventory_sha = (
        untracked(repo)
    )

    data = {
        "branch":
            branch,

        "head":
            head,

        "staging_empty":
            run(
                "git",
                "diff",
                "--cached",
                "--quiet",
                cwd=repo,
            ).returncode
            == 0,

        "tracked_worktree_clean":
            run(
                "git",
                "diff",
                "--quiet",
                cwd=repo,
            ).returncode
            == 0,

        "untracked_count":
            len(paths)
            if rc == 0
            else None,

        "untracked_sha256":
            inventory_sha,
    }

    if args.json:
        print(
            json.dumps(
                data,
                sort_keys=True,
            )
        )

        return 0

    packet(
        "GOLD STANDARD SNAPSHOT",
        [
            (
                "BRANCH",
                branch,
            ),
            (
                "HEAD",
                head,
            ),
            (
                "STAGE EMPTY",
                data[
                    "staging_empty"
                ],
            ),
            (
                "TRACKED CLEAN",
                data[
                    "tracked_worktree_clean"
                ],
            ),
            (
                "UNTRACKED",
                data[
                    "untracked_count"
                ],
            ),
            (
                "UNTRACKED SHA",
                inventory_sha,
            ),
        ],
        "SNAPSHOT_CAPTURED",
        (
            "BIND THESE VALUES INTO "
            "THE NEXT MUTATING BLOCK"
        ),
    )

    return 0


def cmd_verify(args):
    failures = []

    for spec in args.sha256:
        if "=" not in spec:
            failures.append(
                f"bad_sha_spec:"
                f"{spec}"
            )
            continue

        raw, expected = (
            spec.split(
                "=",
                1,
            )
        )

        path = Path(
            raw
        ).expanduser()

        if not path.is_file():
            failures.append(
                f"missing_file:"
                f"{path}"
            )
            continue

        actual = sha_file(
            path
        )

        if actual != expected:
            failures.append(
                f"sha256:"
                f"{path}:"
                f"{actual}"
            )

    for raw in args.absent:
        path = Path(
            raw
        ).expanduser()

        if (
            path.exists()
            or path.is_symlink()
        ):
            failures.append(
                f"expected_absent:"
                f"{path}"
            )

    packet(
        "GOLD STANDARD ARTIFACT VERIFY",
        [
            (
                "SHA CHECKS",
                len(
                    args.sha256
                ),
            ),
            (
                "ABSENT CHECKS",
                len(
                    args.absent
                ),
            ),
        ],
        (
            "ARTIFACTS_VERIFIED"
            if not failures
            else
            "ARTIFACT_VERIFY_BLOCKED"
        ),
        (
            "PROCEED"
            if not failures
            else
            "AUDIT FIRST FAILURE ONLY"
        ),
        failures,
    )

    return (
        0
        if not failures
        else 2
    )


def cmd_packet(args):
    fields = []

    for item in args.field:
        if "=" not in item:
            raise SystemExit(
                f"invalid --field: "
                f"{item}"
            )

        fields.append(
            tuple(
                item.split(
                    "=",
                    1,
                )
            )
        )

    packet(
        args.status,
        fields,
        args.classification,
        args.next_gate,
    )

    return 0


def cmd_selftest(_args):
    failures = []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        cases = {
            "good":
                (
                    "cd /tmp\n"
                    "python - <<'PY'\n"
                    "x = 1\n"
                    "print(x)\n"
                    "PY\n"
                ),

            "exit":
                "exit 1\n",

            "fence":
                (
                    "echo '"
                    + ("`" * 3)
                    + "'\n"
                ),

            "python":
                (
                    "python - <<'PY'\n"
                    "if True print('x')\n"
                    "PY\n"
                ),

            "add":
                "git add .\n",
        }

        results = {}

        for name, text in (
            cases.items()
        ):
            path = (
                root
                / f"{name}.sh"
            )

            path.write_text(
                text,
                encoding="utf-8",
            )

            results[name] = (
                audit_block(
                    path
                )[0]
            )

        if results["good"]:
            failures.append(
                "good_block_failed"
            )

        if not any(
            item.startswith(
                "session_terminator:"
            )
            for item
            in results["exit"]
        ):
            failures.append(
                "exit_not_detected"
            )

        if (
            "nested_markdown_fence"
            not in results["fence"]
        ):
            failures.append(
                "fence_not_detected"
            )

        if not any(
            item.startswith(
                "python_compile:"
            )
            for item
            in results["python"]
        ):
            failures.append(
                "python_error_not_detected"
            )

        if not any(
            item.startswith(
                "broad_git_add:"
            )
            for item
            in results["add"]
        ):
            failures.append(
                "broad_add_not_detected"
            )

    packet(
        "GOLD STANDARD SELFTEST",
        [
            (
                "TESTS",
                5,
            ),
        ],
        (
            "SELFTEST_PASS"
            if not failures
            else
            "SELFTEST_FAIL"
        ),
        (
            "HELPER READY"
            if not failures
            else
            "FIX HELPER BEFORE USE"
        ),
        failures,
    )

    return (
        0
        if not failures
        else 2
    )


def parser():
    root = argparse.ArgumentParser(
        prog="openmind-gold"
    )

    sub = root.add_subparsers(
        dest="command",
        required=True,
    )

    item = sub.add_parser(
        "block"
    )

    item.add_argument(
        "path"
    )

    item.set_defaults(
        func=cmd_block
    )

    item = sub.add_parser(
        "repo"
    )

    item.add_argument(
        "--repo",
        default=".",
    )

    item.add_argument(
        "--branch"
    )

    item.add_argument(
        "--head"
    )

    item.add_argument(
        "--untracked-count",
        type=int,
    )

    item.add_argument(
        "--untracked-sha"
    )

    item.add_argument(
        "--remote-branch"
    )

    item.add_argument(
        "--remote-head"
    )

    item.add_argument(
        "--allow-hooks",
        action="store_true",
    )

    item.set_defaults(
        func=cmd_repo
    )

    item = sub.add_parser(
        "snapshot"
    )

    item.add_argument(
        "--repo",
        default=".",
    )

    item.add_argument(
        "--json",
        action="store_true",
    )

    item.set_defaults(
        func=cmd_snapshot
    )

    item = sub.add_parser(
        "verify"
    )

    item.add_argument(
        "--sha256",
        action="append",
        default=[],
        metavar="PATH=SHA256",
    )

    item.add_argument(
        "--absent",
        action="append",
        default=[],
    )

    item.set_defaults(
        func=cmd_verify
    )

    item = sub.add_parser(
        "packet"
    )

    item.add_argument(
        "--status",
        required=True,
    )

    item.add_argument(
        "--classification",
        required=True,
    )

    item.add_argument(
        "--next-gate",
        required=True,
    )

    item.add_argument(
        "--field",
        action="append",
        default=[],
    )

    item.set_defaults(
        func=cmd_packet
    )

    item = sub.add_parser(
        "selftest"
    )

    item.set_defaults(
        func=cmd_selftest
    )

    return root


def main():
    args = (
        parser()
        .parse_args()
    )

    return args.func(
        args
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
