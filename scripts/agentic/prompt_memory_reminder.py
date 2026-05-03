#!/usr/bin/env python3
import json, sys
sys.stdout.write(json.dumps({
    "systemMessage": "Use /memory as the canonical instruction source. Avoid adding duplicated rules to runtime adapter folders."
}))
