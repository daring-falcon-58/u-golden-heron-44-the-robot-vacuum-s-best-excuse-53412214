"""The Robot Vacuum's Best Excuse — make.fun entry program.

Writes one line, the funniest excuse a robot vacuum gives for missing a
spot, to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (``/output/entry.txt`` by
default). Deterministic: no network, no randomness, no clock — the same
bytes on every run.

Gate (from the competition brief): the output must be UTF-8 text of 1 to
140 characters, not only white space. The gate is enforced at import time:
an ENTRY that leaves the gate raises ``ValueError`` before anything is
written. The write is verified by reading the file back and comparing bytes.
"""

import hashlib
import os

ENTRY = "My cliff sensor looked at that dark rug, saw the void, and I don't argue with the void."

# sha256 of the exact bytes written to entry.txt (verified across runs).
EXPECTED_SHA256 = "974a4b6546d1f7f6c2d623fcd5d1fec23aa09a62f445462bb16bad4b03e61f84"

MAX_CHARS = 140


def _validate(text):
    if not isinstance(text, str):
        raise ValueError("ENTRY must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "ENTRY must be 1 to %d characters, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("ENTRY must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("ENTRY must be a single line")


_validate(ENTRY)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        back = fh.read()
    if back != data:
        raise OSError("write-back verification failed for %s" % path)
    if hashlib.sha256(back).hexdigest() != EXPECTED_SHA256:
        raise OSError("sha256 digest self-check failed for %s" % path)
    print("wrote %d bytes to %s" % (len(data), path))


if __name__ == "__main__":
    main()
