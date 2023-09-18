"""Semantic Smoke Tests for the Translator UI."""
from datetime import datetime
import jq
import json
import requests
import time
import traceback

debug = True


def main():
    """Run UI Semantic Smoke Tests."""
    # Download queries
    try:
        with open("./tests.json", "r") as f:
            tests = json.load(f)
        # response = requests.get("http://url.to.queries")
        # response.raise_for_status()
        # response = response.json()
    except Exception:
        print("Failed to download test queries")
        return

    for query in tests:
        # Send Query
        query_payload = {
            "type": query["type"],
            "curie": query["curie"],
            "direction": query["direction"],
        }
        try:
            response = requests.post(
                "https://ui.test.transltr.io/api/creative_query",
                headers={
                    "Content-Type": "application/json",
                },
                data=json.dumps(query_payload),
            )
            response.raise_for_status()
            response = response.json()
            if response["status"] == "success":
                query_id = {
                    "qid": response["data"],
                }
            else:
                print(response["data"])
                return
        except Exception:
            print(traceback.format_exc())
            return
        
        # Wait for query to finish
        wait_seconds = 60 * 10
        started = datetime.now()
        finished = False

        while not finished:
            try:
                response = requests.post(
                    "https://ui.test.transltr.io/api/creative_status",
                    headers={
                        "Content-Type": "application/json",
                    },
                    data=json.dumps(query_id),
                )
                response.raise_for_status()
                response = response.json()
                if response["status"] == "running":
                    running_time = (datetime.now() - started).total_seconds()
                    if running_time > wait_seconds:
                        print("Query ran out of time.")
                        return
                    # retry after 10 seconds
                    time.sleep(10)
                elif response["status"] == "error":
                    finished = True
                elif response["status"] == "success":
                    finished = True
            except Exception:
                print(traceback.format_exc())
                return
        
        # Get results
        try:
            response = requests.post(
                "https://ui.test.transltr.io/api/creative_result",
                headers={
                    "Content-Type": "application/json",
                },
                data=json.dumps(query_id),
            )
            response.raise_for_status()
            response = response.json()
            results = response["data"]
        except Exception:
            print(traceback.format_exc())
            return

        # Create assertions list
        assertions = [
            f'.results[:{assertion["top_n_results"]}][] | .subject {"==" if assertion["include"] else "!="} \"{assertion["target_curie"]}\"'
            for assertion in query["assertions"]
        ]
        for assertion in assertions:
            values = jq.compile(assertion).input(results)
            if True in values:
                # test passed
                print("Passed!")
            else:
                print("Fail.")
        if debug:
            now = datetime.now().isoformat()
            with open(f"results_{now}.json", "w") as f:
                json.dump(results, f)


if __name__ == "__main__":
    main()
