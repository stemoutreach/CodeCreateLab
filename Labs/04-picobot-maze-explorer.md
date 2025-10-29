
---
title: PicoBot Maze Explorer
level: 04
estimated_time: 60–90 min
difficulty: Intermediate
prereqs:
  - Guide: [04 – PicoBot – Motors & Ultrasonic](../Guides/04-picobot.md)
  - Lab: [03 – Pico Breadboard Lab](../Labs/03-pico-breadboard-lab.md)
rubric:
  - ✅ Must: Robot drives forward and **avoids obstacles** using the ultrasonic sensor
  - ✅ Must: Implements **timed turns** (≈80–90°) via helper functions
  - ✅ Must: Clean loop with a **safe stop** on Ctrl‑C
  - ⭐ Stretch: Chooses left/right using a look‑around routine; optional wall‑following
---

# Goal
Program your **PicoBot** to navigate a simple cardboard maze. Use the ultrasonic sensor to detect obstacles and perform **timed left/right turns** to keep moving until an exit is found.

## Materials
- PicoBot chassis (Pico + L298N + 2 DC motors + HC‑SR04)
- External motor battery (share **GND** with Pico)
- Open floor + a small maze (boxes, books, tape lanes)

## Project layout (recommended)
```
/picobot/
├─ robot_utils.py   # movement + distance helpers (you edit/tune these)
└─ main.py          # the maze logic using robot_utils
```

## Safety & setup
- Power **motors** from their own battery; share **GND** with the Pico.
- Lift wheels off the table when first testing **turns**.
- Keep loose clothes/hair away from wheels.

## Steps
1) **Wire check** — Confirm pins match the guide mapping (IN1=GP6, IN2=GP7, ENA=GP8, IN3=GP4, IN4=GP3, ENB=GP2, TRIG=GP14, ECHO=GP15).
2) **Utilities** — Fill in `robot_utils.py` (pins, move/turn functions, `read_distance_cm()`).
3) **Tune turning** — Adjust `TURN_DURATION` until one call ≈ 80–90° on your floor.
4) **Maze logic** — Use `main.py` starter to drive forward; when blocked, turn left or right (stretch: “look‑around” to pick clearer side).
5) **Iterate** — Reduce getting stuck by adding a brief back‑up before turning; add randomness if needed.

## Starter files
- `robot_utils.py` — motor + sensor helpers
- `main.py` — high‑level navigation loop

## Submission / Demo checklist
- [ ] Robot avoids obstacles and continues moving
- [ ] Pressing **Ctrl‑C** stops motors and exits cleanly
- [ ] (Stretch) Robot **chooses** a side using a look‑around routine
- [ ] You can explain how you tuned `TURN_DURATION`

## Extensions (choose one)
- **Look‑around chooser**: sample left vs. right distance and pick the longer.
- **Back‑off**: reverse a short distance before turning.
- **Wall follower**: keep a fixed distance to the left/right wall (simple P control).

## Troubleshooting
- **Motors won’t move** → Ensure EN pins are **HIGH**; check battery and shared **GND**.
- **Always reads None** → Check TRIG/ECHO pins; ensure nothing blocks the sensor; increase timeout.
- **Spin in place on forward** → One motor reversed; swap its leads or invert logic.
- **Turns too much/too little** → Tweak `TURN_DURATION` (floor friction matters!).

## Reflection
- What strategy does your bot use when distances tie? How would you improve it with minimal extra hardware?
