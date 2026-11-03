import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from scripts import update_monkeytype as mt


class Response(io.BytesIO):
    def __init__(self, data):
        super().__init__(json.dumps({"data": data}).encode())


class MonkeytypeTests(unittest.TestCase):
    def test_aggregate_object_and_array_bests_and_numeric_mode2(self):
        responses = [Response({"wpm": 90}), Response([{"wpm": 70}, {"wpm": 80}]),
                     Response([{"mode": "time", "mode2": 15, "wpm": 100, "acc": 90},
                               {"mode": "time", "mode2": "15", "wpm": 80, "acc": 100},
                               {"mode": "words", "mode2": 10, "wpm": 60, "acc": 95},
                               {"mode": "words", "mode2": 25, "wpm": 99, "acc": 99}])]
        with patch.object(mt, "urlopen", side_effect=responses) as mock:
            data = mt.build("secret")
        self.assertEqual(mock.call_args_list[0].args[0].get_header("Authorization"), "ApeKey secret")
        self.assertTrue(data["complete"])
        self.assertEqual(data["categories"][0]["mean_wpm"], 90)
        self.assertEqual(data["categories"][0]["mean_accuracy"], 95)
        self.assertEqual(data["categories"][0]["count"], 2)
        self.assertEqual(data["categories"][1]["pb_wpm"], 80)
        self.assertEqual(data["categories"][1]["count"], 1)

    def test_free_cap_is_not_all_time(self):
        error = HTTPError("url", 422, "", {}, io.BytesIO(b'{"message":"Max results limit of 1000 exceeded."}'))
        with patch.object(mt, "urlopen", side_effect=[Response(None), Response([]), Response([{}] * 1000), error]):
            data = mt.build("secret")
        self.assertFalse(data["complete"])
        self.assertEqual(data["retrieved_count"], 1000)

    def test_premium_paginates_and_can_prove_complete(self):
        with patch.object(mt, "urlopen", side_effect=[Response(None), Response([]), Response([{}] * 1000), Response([])]):
            data = mt.build("secret")
        self.assertTrue(data["complete"])
        self.assertEqual(data["retrieved_count"], 1000)

    def test_other_error_preserves_file_and_does_not_log_secret(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "data.json"
            output.write_text("old")
            with patch.object(mt, "OUTPUT", output), patch.dict(os.environ, {"MONKEYTYPE_API_KEY": "secret"}), \
                 patch.object(mt, "urlopen", side_effect=RuntimeError("secret")), patch("sys.stderr", new_callable=io.StringIO) as stderr:
                self.assertEqual(mt.main(), 1)
            self.assertEqual(output.read_text(), "old")
            self.assertNotIn("secret", stderr.getvalue())

    def test_unrecognized_422_is_error(self):
        error = HTTPError("url", 422, "", {}, io.BytesIO(b'{"message":"other error"}'))
        with patch.object(mt, "urlopen", side_effect=error):
            with self.assertRaises(HTTPError):
                mt.request("/results", {"limit": 1000, "offset": 1000}, "secret")


if __name__ == "__main__":
    unittest.main()
