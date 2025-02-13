#! /usr/bin/env python
import runpod
import requests
import json  # Required for parsing JSON lines

def handler(job):
    """
    Handler for processing each RunPod job.
    It forwards the request to a local Ollama instance (running at localhost:11434),
    streaming the response line by line.
    """

    base_url = "http://localhost:11434"
    
    # job["input"] is the payload you send when calling the endpoint.
    # Example expected format of job["input"]:
    # {
    #   "method_name": "chat",      # or "generate" or any Ollama method
    #   "payload": {
    #       "prompt": "Why is the sky blue?",
    #       ...
    #   }
    # }
    
    method_name = job["input"].get("method_name", "chat")
    payload = job["input"].get("payload", {})
    
    # Ensure streaming is enabled for Ollama
    payload["stream"] = True
    payload["options"] = { "num_ctx": 40960 }
    

    # Make the POST request to your local Ollama endpoint
    resp = requests.post(
        url=f"{base_url}/api/{method_name}/",
        headers={"Content-Type": "application/json"},
        json=payload,
        stream=True  # Enable response streaming
    )
    resp.encoding = "utf-8"

    # Stream the response line by line
    for line in resp.iter_lines():
        # Filter out keep-alive new lines
        if not line:
            continue

        # Ollama returns streaming data in JSON lines
        data = json.loads(line)
        
        # You can yield the entire JSON or just a subset,
        # for example: data["message"]["content"]
        yield data


# Important: "return_aggregate_stream" must be True to enable streaming from RunPod.
runpod.serverless.start(
    {
        "handler": handler,
        "return_aggregate_stream": True
    }
)
