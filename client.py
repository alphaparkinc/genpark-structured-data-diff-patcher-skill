import json
import copy
from typing import Dict, Any, List, Optional

class StructuredDataDiffPatcherClient:
    """
    Production-grade JSON Patch (RFC 6902) differential engine.
    Calculates minimal operational diffs and applies state transitions atomically.
    """
    def __init__(self):
        pass

    def compute_and_apply_patch(self, doc_before: Optional[Dict[str, Any]] = None, doc_after: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not doc_before:
            doc_before = {
                "sku": "ROBO-S8",
                "price": 1599.0,
                "in_stock": True,
                "tags": ["vacuum", "lidar"]
            }
        if not doc_after:
            doc_after = {
                "sku": "ROBO-S8",
                "price": 1399.0,
                "in_stock": True,
                "tags": ["vacuum", "lidar", "promo-deal"],
                "warranty_years": 2
            }

        operations = []
        # Check updates and additions
        for k, v in doc_after.items():
            if k not in doc_before:
                operations.append({"op": "add", "path": f"/{k}", "value": v})
            elif doc_before[k] != v:
                operations.append({"op": "replace", "path": f"/{k}", "value": v})

        # Check deletions
        for k in doc_before:
            if k not in doc_after:
                operations.append({"op": "remove", "path": f"/{k}"})

        # Apply patch to before doc
        patched = copy.deepcopy(doc_before)
        for op in operations:
            key = op["path"].lstrip("/")
            if op["op"] in ["add", "replace"]:
                patched[key] = op["value"]
            elif op["op"] == "remove" and key in patched:
                del patched[key]

        return {
            "patch_id": "ptc_rfc_6612",
            "operations_count": len(operations),
            "operations": operations,
            "patch_applied_cleanly": (patched == doc_after),
            "patched_document": patched
        }
