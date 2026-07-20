"""Shared JSON POST + long-running-operation polling for the video rungs."""
import json, time, urllib.request


def post(url, body, headers):
    req = urllib.request.Request(url, json.dumps(body).encode(), headers)
    return json.load(urllib.request.urlopen(req))


def poll(get, tries=60, wait=10):
    for _ in range(tries):
        op = get()
        if op.get("done"):
            return op
        time.sleep(wait)
    raise TimeoutError("generation did not finish")
