import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import StructuredDataDiffPatcherClient

def main():
    client = StructuredDataDiffPatcherClient()
    res = client.compute_and_apply_patch()
    print("=== Structured Data Diff Patcher Output ===")
    print(f"Total Operations: {res['operations_count']} | Cleanly Applied: {res['patch_applied_cleanly']}")
    print("\nRFC 6902 Patch Operations:")
    for op in res['operations']:
        print(f"  - [{op['op'].upper()}] {op['path']} -> {op.get('value')}")

if __name__ == '__main__':
    main()
