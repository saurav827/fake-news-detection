#!/usr/bin/env python3
"""Quick training script to test the system"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Starting training process...")

try:
    from train import main
    main()
    print("\n✓ Training completed successfully!")
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
