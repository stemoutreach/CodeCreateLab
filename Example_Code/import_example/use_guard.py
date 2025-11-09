"""
use_guard.py
-------------
Import demo_guard and call its helper(). Notice that demo_guard.main() does not run
on import thanks to the main-guard.
"""

import demo_guard

print(f"[use_guard] __name__ = {__name__}")
print("[use_guard] After importing demo_guard, calling its helper():")
demo_guard.helper()
