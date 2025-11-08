
# PicoBot — Drive Basics (Student Starter)

> Goal: Drive forward, turn, and stop using an L298N motor driver with PWM trim. **No sensors** for this lab.

## Files in this folder
- `main.py` — skeleton you will complete
- *(Coach only)* `SOLUTION.md` — full reference solution (don’t peek!)

## Steps
1. Wire the L298N to your Pico (see Guide: `Guides/04-picobot.updated.md` for pin map).
2. In Thonny, select **MicroPython (Raspberry Pi Pico)** as the interpreter.
3. Open `main.py`:
   - Set the GPIO pin numbers for `ENA/ENB/IN1/IN2/IN3/IN4`.
   - Complete the TODOs to implement `forward(ms)`, `turn_left(ms)`, `turn_right(ms)`, and `stop()`.
   - Use `set_trim(left, right)` to balance your motors.
4. Save to the Pico as **`main.py`** so it runs on boot.
5. Test the demo route (a timed square). Tweak `PWM_DUTY` and trim as needed.

## Safety
- Keep wheels off the table when first testing.
- Always call `stop()` before errors or exiting (`Ctrl+C`).

## Checklist
- [ ] Robot drives forward in a straight line (trim adjusted)
- [ ] Robot can turn left and right
- [ ] `stop()` reliably stops both motors
- [ ] Timed square route completes without intervention
