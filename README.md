# Code & Create Lab

**Learn by building.** Code & Create Lab is a self-paced quest that walks students—from absolute beginners to budding roboticists—through the fundamentals of **Python programming**, **physical computing**, and **robot motion**.

Each **Guide** teaches skills. Each **Lab** applies those skills in a small project. By the final level, you’ll have a Pico-powered robot that you assembled, wired, and drove yourself.

---

## 🎯 Purpose
1. **Make STEM approachable** — lower the entry barrier so anyone (Grades 6–12+) can start creating with code and electronics.  
2. **Turn theory into practice** — every concept is immediately applied in a working artifact.  
3. **Promote a growth mindset** — short wins build confidence; stretch goals reward curiosity.  
4. **Empower instructors & mentors** — modular guides, checklists, and wiring diagrams keep prep light.

---

## 🧭 How to use this repo

### Our learning loop: Learn → Try → Do
- **Learn** (Guides): short, focused explanations with tiny examples.
- **Try** (Guides): quick practice right after you learn something.
- **Do** (Labs): build a small project that proves you can apply it.

1. Start with a **Guide**, then complete the matching **Lab** with the same number.  
2. Use the **Skeleton Starter** from `Example_Code/<NN-...>.py` when provided.  
3. Demo your Lab using the **Submission Checklist** and try at least one **Extension**.

> Teaching? Use **Guides** as your notes. **Labs** are student handouts with rubrics.
>
> New to the program? See the **[Parent & Volunteer Guide](ParentVolunteer.md)**.

---

## 🛠️ Setup (classroom default)
- **Hardware:** Raspberry Pi 500 running Raspberry Pi OS  
- **IDE:** Thonny (Menu → Programming → Thonny)  
- **Save your work:** `~/Documents/CodeCreate/`  
- **Interpreters:**  
  - Raspberry Pi & Sense HAT labs → **Python 3** in Thonny  
  - Pico & PicoBot labs → **MicroPython (Raspberry Pi Pico)** in Thonny (choose from the interpreter menu)
- If you’re working outside the lab, you can prototype simple Python in a browser REPL and move to Thonny later.

---

## 🧠 Core Concepts
- **Python Fundamentals** — variables, conditionals, loops, functions  
- **Sensor I/O** — temperature, humidity, pressure, IMU  
- **Actuators & Signaling** — LEDs, RGB mixing, DC motors  
- **Microcontrollers** — Raspberry Pi Pico (MicroPython) & Raspberry Pi (Python)  
- **Robot Motion** — motor polarity, speed trim, timed turns, basic path patterns  
- **Engineering Practice** — breadboarding, wiring, iterative debugging

---

## 🚀 Learning Path (Guides → Labs)

| #  | Guide | Lab (goal) | Hardware | Time |
|----|------|------------|----------|------|
| 00 | [Python Basics](Guides/00-python-basics.md) | [Treasure Hunt (Basic)](Labs/00-treasure-hunt-basic.md) — text adventure with loops & logic | Computer only | 30–45 min |
| 01 | [Python Functions](Guides/01-python-functions.md) | [Treasure Hunt (Functions)](Labs/01-treasure-hunt-functions.md) — refactor with functions | Computer only | 35–60 min |
| 02 | [Sense HAT](Guides/02-sense-hat.md) | [Sense HAT Basics — Weather Warning Light](Labs/02-sense-hat-basics.md) | Raspberry Pi + Sense HAT | 30–45 min |
| 02.5 | *(optional)* Advanced Sense HAT | [Mission Dashboard](Labs/02-5-sense-hat-advanced.md) — icons, smoothing, dashboards | Raspberry Pi + Sense HAT | 35–60 min |
| 03 | [Pico Breadboarding](Guides/03-pico-breadboarding.md) | [Pico Breadboard Lab](Labs/03-pico-breadboard-lab.md) — button + LED (optional RGB/buzzer) | Pico + breadboard | 45–75 min |
| 04 | **PicoBot — Drive with L298N** ([Guide](Guides/04-picobot.md)) | **PicoBot Drive Basics** — forward/turn/stop, speed trim, timed square *(ultrasonic deferred)* ([Lab](Labs/04-picobot-maze-explorer.md)) | Pico + L298N + chassis + 2× DC motors | 60–90 min |

**Note:** We’ve intentionally **deferred ultrasonic** work for now. The current 04 lab focuses on reliable driving and calibration. (The filename may still say `04-picobot-maze-explorer.md` until the next commit.)

**Starters:** See `Example_Code/` for runnable `.py` files aligned with many labs.

---

## 📁 Repository structure
```
.
├─ README.md
├─ ParentVolunteer.md
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
│  └─ 04-picobot-maze-explorer.md   ← drives L298N for now; ultrasonic later
├─ Example_Code/
│  ├─ 00-treasure-hunt-basic.py
│  ├─ 01-treasure-hunt-functions.py
│  ├─ 02-sense-hat-basics.py
│  ├─ 02-5-sense-hat-mission-dashboard.py
│  ├─ 03-pico-breadboard-lab.py
│  └─ 04-picobot-maze-explorer/
│     ├─ robot_utils.py
│     └─ main.py
└─ assets/   # images, wiring diagrams
```

---

## 🤝 Contributing
Issues and PRs welcome! If you’re adding a new Guide/Lab, please follow the **template order** and include a single **Skeleton Starter** (no spoilers). Keep links **relative** and validate that code fences and headers render cleanly.

---

## 🪪 License & attribution
Made with ❤️ by STEM Outreach volunteers & community mentors. Licensed under the **MIT License**.  
If you reuse or remix, please include attribution (“Code & Create Lab”).
