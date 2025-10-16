#!/usr/bin/env python3

import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from cli import FinancialCLI


def main():
    try:
        app = FinancialCLI()
        app.run()
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
