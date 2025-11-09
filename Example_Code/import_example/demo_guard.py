"""
demo_guard.py
--------------
A tiny module that shows how the main-guard works.
Run this file directly, then import it from another file.
"""

def helper():
    print("[demo_guard.helper] I am a helper that can be imported.")

def main():
    print("[demo_guard.main] Running main() because the file was executed directly.")

print(f"[demo_guard] __name__ = {__name__}")

if __name__ == "__main__":
    # Only runs when you press Run ▶ on THIS file (executed directly).
    # Does NOT run when another file does: import demo_guard
    main()
