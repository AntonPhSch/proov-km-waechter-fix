# log_util.py
# A minimal append-to-file logger.
# Hand-rolled in 2013; modernized 2025.

import time

LOG_LINES: list[str] = []   # module-level buffer; flushed to disk by flush_log()


def log(message: str) -> None:
    """Timestamp a message, print it, and add it to the flush buffer."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Append all buffered log lines to the file at path, then clear the buffer."""
    with open(path, "a", encoding="utf-8") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
