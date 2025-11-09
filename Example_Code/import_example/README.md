# Main-Guard Demo (Run vs Import)

This pair shows what happens when you **run** a file vs **import** it.

## Files
- `demo_guard.py` — module with a `main()` and a **main-guard**.
- `use_guard.py` — imports `demo_guard` and calls its `helper()`.

## Try it in Thonny (Raspberry Pi 500)
1) Open `demo_guard.py` and press **Run ▶**.  
   **Expected output (example):**
   ```
   [demo_guard] __name__ = __main__
   [demo_guard.main] Running main() because the file was executed directly.
   ```

2) Open `use_guard.py` and press **Run ▶**.  
   **Expected output (example):**
   ```
   [demo_guard] __name__ = demo_guard
   [use_guard] __name__ = __main__
   [use_guard] After importing demo_guard, calling its helper():
   [demo_guard.helper] I am a helper that can be imported.
   ```

## What happened?
- When you **run** `demo_guard.py`, `__name__` is `__main__`, so its `main()` executes.
- When you **import** it from `use_guard.py`, `__name__` becomes `demo_guard`, so the **main-guard**
  prevents `main()` from running automatically. You still can call any functions you exported.

## Common pitfall
- Forgetting the `()` in the guard line:
  ```python
  if __name__ == "__main__":
      main  # ❌ does nothing (this is just a reference, not a call)
  ```
  Correct:
  ```python
  if __name__ == "__main__":
      main()  # ✅ actually calls main
  ```
