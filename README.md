
# Code & Create Lab

**Learn by building.** Code & Create Lab is a self‑paced quest that walks students—from absolute beginners to budding roboticists—through the fundamentals of **Python programming**, **physical computing**, and **autonomous navigation**.

Each **Guide** teaches skills. Each **Lab** applies those skills in a small project. By the final level, you’ll have a Pico‑powered robot that senses, moves, and navigates.

---

## 🎯 Purpose
1. **Make STEM approachable** — lower the entry barrier so anyone (Grades 6–12+) can start creating with code and electronics.  
2. **Turn theory into practice** — every concept is immediately applied in a working artifact.  
3. **Promote a growth mindset** — short wins build confidence; stretch goals reward curiosity.  
4. **Empower instructors & mentors** — modular guides, checklists, and wiring diagrams keep prep light.

---

## 🧭 How to use this repo
1. Start with a **Guide**, then complete the matching **Lab** with the same number.  
2. Copy the starter from `Example_Code/<NN-...>.py` when provided.  
3. Demo your Lab using the **Submission Checklist** and try at least one **Extension**.

> If you’re teaching, the **Guides** are your slide notes. The **Labs** are student handouts with rubrics.

---

## 🧠 Core Concepts
- **Python Fundamentals** — variables, conditionals, loops, functions  
- **Sensor I/O** — temperature, humidity, pressure, IMU  
- **Actuators & Signaling** — LEDs, RGB mixing, DC motors  
- **Microcontrollers** — Raspberry Pi Pico (MicroPython) & Raspberry Pi (Python)  
- **Robotics Algorithms** — obstacle avoidance, maze strategies  
- **Engineering Practice** — breadboarding, wiring, iterative debugging

---

## 🚀 Learning Path (Guides → Labs)

| # | Guide | Lab (goal) | Hardware | Time |
|---|---|---|---|---|
| 00 | [Python Basics](Guides/00-python-basics.md) | [Treasure Hunt (Basic)](Labs/00-treasure-hunt-basic.md) — text adventure with loops & logic | Computer only | 30–45 min |
| 01 | [Python Functions](Guides/01-python-functions.md) | [Treasure Hunt (Functions)](Labs/01-treasure-hunt-functions.md) — refactor with functions | Computer only | 35–60 min |
| 02 | [Sense HAT](Guides/02-sense-hat.md) | [Sense HAT Basics — Weather Warning Light](Labs/02-sense-hat-basics.md) | Raspberry Pi + Sense HAT | 30–45 min |
| 02.5 | — | [Sense HAT Advanced — Mission Dashboard](Labs/02-5-sense-hat-advanced.md) | Raspberry Pi + Sense HAT | 45–75 min |
| 03 | [Pico Breadboarding](Guides/03-pico-breadboarding.md) | [Pico Breadboard Lab](Labs/03-pico-breadboard-lab.md) — button + LED (+ RGB/ultrasonic option) | Pico + breadboard | 45–75 min |
| 04 | [PicoBot — Motors & Ultrasonic](Guides/04-picobot.md) | [PicoBot Maze Explorer](Labs/04-picobot-maze-explorer.md) — avoid obstacles & navigate | PicoBot (Pico + L298N + HC‑SR04) | 60–90 min |

**Starters:** see `Example_Code/` for runnable `.py` files that align with many labs.

---

## 📁 Repository structure
```
.
├─ README.md
├─ Guides/
│  ├─ 00-python-basics.md
│  ├─ 01-python-functions.md
│  ├─ 02-sense-hat.md
│  ├─ 03-pico-breadboarding.md
│  └─ 04-picobot.md
├─ Labs/
│  ├─ 00-treasure-hunt-basic.md
│  ├─ 01-treasure-hunt-functions.md
│  ├─ 02-sense-hat-basics.md
│  ├─ 02-5-sense-hat-advanced.md
│  ├─ 03-pico-breadboard-lab.md
│  └─ 04-picobot-maze-explorer.md
├─ Example_Code/
│  ├─ 00-treasure-hunt-basic.py
│  ├─ 01-treasure-hunt-functions.py
│  ├─ 02-sense-hat-basics.py
│  ├─ 02-5-sense-hat-mission-dashboard.py
│  ├─ 03-pico-breadboard-lab.py
│  └─ 04-picobot-maze-explorer/
│     ├─ robot_utils.py
│     └─ main.py
└─ assets/ (images, wiring diagrams)
```

## 🪪 License & attribution
Made with ❤️ by STEM Outreach volunteers & community mentors. Licensed under the **MIT License**.  
If you reuse or remix, please include attribution (“Code & Create Lab”).

---

