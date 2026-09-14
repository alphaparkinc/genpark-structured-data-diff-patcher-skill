import json, sys
from client import StructuredDataDiffPatcherClient

def handle_mcp_request(payload):
    method = payload.get("method")
    req_id = payload.get("id", 1)
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "data-diff-patcher", "version": "1.0.0"}}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [{"name": "compute_and_apply_patch", "description": "Computes minimal RFC 6902 JSON patch and applies atomic modifications."}]}}
    elif method == "tools/call":
        client = StructuredDataDiffPatcherClient()
        res = client.compute_and_apply_patch()
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "ACTIVE"}}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(handle_mcp_request({"method": "tools/list"})))
    else:
        client = StructuredDataDiffPatcherClient()
        print(json.dumps(client.compute_and_apply_patch(), indent=2))
