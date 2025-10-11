import json
from datetime import datetime
from tqdm import tqdm


def main() -> None:
    filename_base = "example-data-"
    rowset = [
        10,
        100,
        1000,
        5000,
        10000,
        15000,
        20000,
        50000,
        100000,
        200000,
        500000,
        int(1e6),
        int(5e6),
        int(1e7),
        int(5e7),
        int(1e8),
        int(5e8),
        int(1e9),
    ]

    data = {
        "user_id": 1337,
        "username": "dev0rce",
        "last_login": datetime.now().isoformat(),
        "banned": False,
    }

    for rows in tqdm(rowset, desc="Generating files"):
        filename = filename_base + f"{rows}.jsonl"
        tqdm.write(f"generating file {filename}...")
        with open(filename, "a") as f:
            for row in tqdm(range(rows), leave=False, desc="Dump iterating"):
                json.dump(data, f)
                f.write("\n")


if __name__ == "__main__":
    main()
