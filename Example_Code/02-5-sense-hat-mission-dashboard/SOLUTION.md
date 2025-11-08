
# Coach Solution — Sense HAT Mission Dashboard

> Keep this file coach-only. Provide students the `STUDENT_START.md` and starter `.py`.

**Implementation notes:**
- Icons as 64-tuple lists (K background, icon color per thresholds).
- `render()` chooses icon by mode and sets pixels; overlay uses `show_message` with small speed, or custom glyphs.
- Main loop targets 8 FPS with a short 10ms sleep for responsiveness.
