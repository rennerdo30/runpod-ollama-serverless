#! /usr/bin/env python
import runpod
import requests
import json  # Required for parsing JSON lines


def handler(job):
    base_url = "http://localhost:11434"
    payload = job["input"]["payload"]

    # Ensure streaming is enabled for Ollama
    payload["stream"] = True

    # Make the POST request with streaming enabled
    resp = requests.post(
        url=f"{base_url}/api/{job['input']['method_name']}/",
        headers={"Content-Type": "application/json"},
        json=payload,
        stream=True  # Enable response streaming
    )
    resp.encoding = "utf-8"

    # Stream the response line by line
    for line in resp.iter_lines():
        # Filter out keep-alive new lines
        if line:
            # Parse each JSON line and yield incrementally
            yield json.loads(line)


runpod.serverless.start({"handler": handler, "return_aggregate_stream": True})