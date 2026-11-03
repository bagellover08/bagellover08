#!/usr/bin/env python3
"""Fetch public aggregates only; never write raw results or credentials."""
import json
import math
import os
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.monkeytype.com"
OUTPUT = Path(__file__).resolve().parents[1] / "_data" / "monkeytype.json"
CATEGORIES = (("time", "15"), ("words", "10"))


class CapReached(Exception):
    pass


def request(path, params, key):
    url = API + path + "?" + urlencode(params)
    try:
        with urlopen(Request(url, headers={"Authorization": "ApeKey " + key}), timeout=30) as response:
            payload = json.load(response)
    except HTTPError as exc:
        # Only the API's explicit cap response is a normal pagination boundary.
        if exc.code == 422:
            try:
                message = json.load(exc).get("message", "")
            except (ValueError, AttributeError):
                message = ""
            offset = params.get("offset")
            if offset in (1000, 10000) and message == f"Max results limit of {offset} exceeded.":
                raise CapReached from None
        raise
    if not isinstance(payload, dict) or "data" not in payload:
        raise ValueError("Invalid API response")
    return payload["data"]


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Invalid numeric value")
    return value


def build(key):
    bests = {}
    for mode, mode2 in CATEGORIES:
        data = request("/users/personalBests", {"mode": mode, "mode2": mode2}, key)
        if data is None:
            entries = []
        elif isinstance(data, dict):
            entries = [data]
        elif isinstance(data, list):
            entries = data
        else:
            raise ValueError("Invalid personal bests")
        values = [number(entry["wpm"]) for entry in entries]
        bests[(mode, mode2)] = max(values) if values else None

    results = []
    complete = False
    for offset in range(0, 10001, 1000):
        try:
            batch = request("/results", {"limit": 1000, "offset": offset}, key)
        except CapReached:
            break
        if not isinstance(batch, list) or len(batch) > 1000:
            raise ValueError("Invalid results")
        results.extend(batch)
        if len(batch) < 1000:
            complete = True
            break
    categories = []
    for mode, mode2 in CATEGORIES:
        matches = []
        for row in results:
            if not isinstance(row, dict):
                raise ValueError("Invalid result")
            if row.get("mode") == mode and str(row.get("mode2")) == mode2:
                matches.append((number(row["wpm"]), number(row["acc"])))
        count = len(matches)
        categories.append({"mode": mode, "mode2": mode2, "pb_wpm": bests[(mode, mode2)],
                           "count": count,
                           "mean_wpm": round(sum(x[0] for x in matches) / count, 2) if count else None,
                           "mean_accuracy": round(sum(x[1] for x in matches) / count, 2) if count else None})
    return {"connected": True, "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "complete": complete, "retrieved_count": len(results), "categories": categories}


def main():
    key = os.environ.get("MONKEYTYPE_API_KEY")
    if not key:
        print("Monkeytype update failed: API key is missing.", file=sys.stderr)
        return 1
    try:
        data = build(key)
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", dir=OUTPUT.parent, delete=False, encoding="utf-8") as f:
            temp = Path(f.name)
            try:
                json.dump(data, f, indent=2, allow_nan=False)
                f.write("\n")
            except Exception:
                temp.unlink(missing_ok=True)
                raise
        try:
            os.replace(temp, OUTPUT)
        finally:
            temp.unlink(missing_ok=True)
    except Exception:
        # Do not print exceptions: URLs, response bodies and headers may be sensitive.
        print("Monkeytype update failed; existing data was preserved.", file=sys.stderr)
        return 1
    print("Monkeytype aggregates updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
