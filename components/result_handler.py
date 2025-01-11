import json
import logging

class JsonResultHandler:
    def __init__(self, filename: str = "results.json"):
        self.filename = filename

    def save_results(self, results: dict[str, list[str]]) -> None:
        with open(self.filename, 'w') as f:
            json.dump(results, f, indent=4)
        logging.info(f"Results saved to {self.filename}")
