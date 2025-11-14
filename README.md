# Code & Create Lab

**Learn by building.** Code & Create Lab is a self‑paced quest that walks students—from absolute beginners to budding roboticists—through the fundamentals of **Python programming**, **physical computing**, and **robot motion**.

Each **Guide** teaches skills. Each **Lab** applies those skills in a small project.

> ### Learn → Try → Do
> - **Learn** concepts in the *Guide*  
> - **Try** micro‑exercises in the *Guide*  
> - **Do** the hands‑on project in the *Lab*

---

## 🎯 Purpose
1. **Make STEM approachable** — start simple, build confidence, and keep moving.  
2. **Turn theory into practice** — every concept is applied immediately.  
3. **Promote a growth mindset** — short wins with stretch challenges.  
4. **Empower instructors & mentors** — modular guides, checklists, and wiring diagrams.

---

## 🧭 How to use this repo
1. Start with a **Guide**, then complete the matching **Lab** with the same number.  
2. Open **Thonny** on a **Raspberry Pi 500** (classroom default) and run the examples.  
3. Use the **hint** in each lab to open its `STUDENT_START.md` when you’re stuck for 5–7 minutes.  
4. Demo your Lab using the **Submission Checklist** and try at least one **Extension**.

> Teaching tip: The **Guides** are your mini‑lesson notes. The **Labs** are student handouts with rubrics.

---

## 🧠 Core Concepts
- **Python Fundamentals** — variables, conditionals, loops, functions  
- **Sensor I/O** — temperature, humidity, pressure 
- **Actuators & Signaling** — LEDs, RGB mixing, DC motors  
- **Microcontrollers** — Raspberry Pi Pico (MicroPython) & Raspberry Pi (Python)  
- **Robotics Motion** — safe wiring, PWM speed control, turn timing & trim  
- **Engineering Practice** — breadboarding, wiring, iterative debugging

---

## 🚀 Learning Path (Guides → Labs)

> **Update:** Sense HAT now has a single lab focused on a Reaction Timer with an optional sensor intermission.

| # | Guide | Lab (goal) | Hardware | Time |
|---|---|---|---|---|
| 00 | [Python Basics](Guides/00-python-basics.md) | [Treasure Hunt (Basic)](Labs/00-treasure-hunt-basic.md) — text adventure with loops & logic | Raspberry Pi only | 30–45 min |
| 01 | [Python Functions](Guides/01-python-functions.md) | [Treasure Hunt (Functions)](Labs/01-treasure-hunt-functions.md) — refactor with functions | Raspberry Pi only | 35–60 min |
| 02 | [Sense HAT](Guides/02-sense-hat.md) | [Sense HAT — Reaction Timer](Labs/02-sense-hat-reaction-timer.md) — LEDs, joystick, timing, optional sensor intermission | Raspberry Pi + Sense HAT | 45–70 min |
| 03 | [Pico Breadboarding](Guides/03-pico-breadboarding.md) | [Pico Breadboard Lab](Labs/03-pico-breadboard-lab.md) — button + LED (+ RGB/buzzer/HC‑SR04 optional) | Raspberry Pi + Pico + breadboard | 45–75 min |
| 04 | [PicoBot — Drive with L298N (No Sensors)](Guides/04-picobot.md) | **[PicoBot Drive Basics](Labs/04-picobot-drive-basics.md)** — forward/turn/stop, PWM trim, timed square | Raspberry Pi+ PicoBot (Pico + L298N) | 60–90 min |

> **Note:** We intentionally split the 04 lab into **Drive Basics (no sensors)** first. Obstacle sensing (e.g., HC‑SR04) comes later, after reliable motion.

---

## 💻 Classroom Environment (default)
- **Hardware:** Raspberry Pi 500 workstations  
- **IDE:** Thonny (Menu → Programming → Thonny)  
- **Pico tip:** Files saved on the Pico as **`main.py`** auto‑run on power‑up

---


## 📁 Repository structure
```
.
├─ README.md
├─ Guides/
│  ├─ 00-python-basics.md
│  ├─ 01-python-functions.updated.md
│  ├─ 02-sense-hat.md
│  ├─ 03-pico-breadboarding.updated.md
│  └─ 04-picobot.updated.md
├─ Labs/
│  ├─ 02-sense-hat-reaction-timer.md
│  ├─ 00-treasure-hunt-basic.md
│  ├─ 01-treasure-hunt-functions.md
│  │  │  ├─ 03-pico-breadboard-lab.md
│  └─ 04-picobot-drive-basics.md
├─ Example_Code/   (per-lab folders with STUDENT_START.md + SOLUTION.md)
└─ assets/         (images, wiring diagrams)
```

> Filenames with `.updated.md` indicate the newest classroom-ready versions. You can rename them to replace the originals when ready.

---



---

## 🤝 Contributing
We welcome fixes and improvements!

- **Branching:** create a feature branch (e.g., `chore/links-lychee`), open a PR.
- **Filenames & links:** use **dash form** for files (e.g., `02-5-sense-hat-advanced.md`). You may keep “02.5” as a human‑readable label **in text**, but **never** in filenames or link URLs.
- **Drive‑only scope for #04:** keep `Labs/04-picobot-drive-basics.md` focused on **L298N drive basics (no sensors)** to avoid drift.
- **Example code layout:** each lab should have a matching folder under `Example_Code/` with `STUDENT_START.md` and (coach‑only) `SOLUTION.md`.

**Optional CI: Markdown link check (Lychee)**  
Create `.github/workflows/markdown-link-check.yml`:
```yaml
name: Check links
on:
  push:
  pull_request:
jobs:
  link-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lychee Link Checker
        uses: lycheeverse/lychee-action@v1
        with:
          args: >-
            --verbose
            --no-progress
            --accept 200,204,429
            --exclude-mail
            --exclude-path "assets/**"
            --include-fragments
            .
        env:
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```


## 🪪 License & attribution
Made with ❤️ by STEM Outreach volunteers & community mentors. Licensed under the **MIT License**.  
If you reuse or remix, please include attribution (“Code & Create Lab”).

