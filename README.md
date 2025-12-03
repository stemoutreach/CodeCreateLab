# Code & Create Lab

**Learn by building.** Code & Create Lab is a self-paced quest that walks students—from absolute beginners to budding roboticists—through the fundamentals of **Python programming**, **physical computing**, and **robot motion**.

Each **Guide** teaches skills. Each **Lab** applies those skills in a small project.

> ### Learn → Try → Do  
> - **Learn** concepts in the *Guide*  
> - **Try** micro-exercises in the *Guide*  
> - **Do** the hands-on project in the *Lab*

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

> Teaching tip: The **Guides** are your mini-lesson notes. The **Labs** are student handouts with rubrics.

---

## 🧠 Core Concepts

- **Python Fundamentals** — variables, conditionals, loops, functions  
- **Sensor I/O** — buttons, distance sensors, environmental sensors  
- **Actuators & Signaling** — LEDs, RGB mixing, speakers, DC motors  
- **Microcontrollers** — Raspberry Pi Pico (MicroPython) & Raspberry Pi (Python)  
- **Robotics Motion** — safe wiring, PWM speed control, turn timing & trim, maze navigation  
- **Engineering Practice** — breadboarding, wiring, iterative debugging, test-as-you-build

---

## 🚀 Learning Path (Guides → Labs)

> **Update:** Sense HAT now has a single lab focused on a Reaction Timer with an optional sensor intermission.  
> The PicoBot track now includes **05 – obstacle sensing & maze exploration**, which builds directly on 04.

| #  | Guide | Lab (goal) | Hardware | Time |
|----|-------|------------|----------|------|
| 00 | [Python Basics](Guides/00-python-basics.md) | [Treasure Hunt (Basic)](Labs/00-treasure-hunt-basic.md) — text adventure with loops & logic | Raspberry Pi only | 30–45 min |
| 01 | [Python Functions](Guides/01-python-functions.md) | [Treasure Hunt (Functions)](Labs/01-treasure-hunt-functions.md) — refactor with functions | Raspberry Pi only | 35–60 min |
| 02 | [Sense HAT](Guides/02-sense-hat.md) | [Sense HAT — Reaction Timer](Labs/02-sense-hat-reaction-timer.md) — LEDs, joystick, timing, optional sensor intermission | Raspberry Pi + Sense HAT | 45–70 min |
| 03 | [Pico Breadboarding](Guides/03-pico-breadboarding.md) | [Pico Breadboard Lab](Labs/03-pico-breadboard-lab.md) — button + LED (+ RGB/buzzer/HC-SR04 optional) | Raspberry Pi + Pico + breadboard + LEDs and sensors | 45–75 min |
| 04 | [PicoBot — Drive with L298N (No Sensors)](Guides/04-picobot.md) | [PicoBot Drive Basics](Labs/04-picobot-drive-basics.md) — forward/turn/stop, PWM trim, timed square | Raspberry Pi + PicoBot (Pico + L298N + motors) | 60–90 min |
| 05 | [PicoBot Sensors & Obstacle Sensing](Guides/05-picobot-sensors-guide.md) | [PicoBot Obstacle Sensing & Maze Explorer](Labs/05-picobot-obstacle-sensing-maze-explorer.md) — HC-SR04 distance sensing, safe stopping, basic maze strategy | Raspberry Pi + PicoBot with ultrasonic sensor | 75–105 min |

> **04 → 05 progression:**  
> - **04** focuses on *reliable motion* (drive, turn, timing, trim).  
> - **05** adds *sensing + decision making* (detect walls, choose turns, explore a maze).

---

## 💻 Classroom Environment (default)

- **Hardware:** Raspberry Pi 500 workstations  
- **IDE:** Thonny (Menu → Programming → Thonny)  
- **Pico tip:** Files saved on the Pico as **`main.py`** auto-run on power-up  

---

## 📁 Repository structure

Top-level layout (see the repo for the most current file list):

```text
.
├─ README.md
├─ ParentVolunteer.md
├─ .github/
│  └─ workflows/          # CI (e.g., optional Markdown link check)
├─ Guides/                # Step-by-step concept Guides (00–05)
│  ├─ 00-python-basics.md
│  ├─ 01-python-functions.md
│  ├─ 02-sense-hat.md
│  ├─ 03-pico-breadboarding.md
│  ├─ 04-picobot.md
│  └─ 05-picobot-sensors-guide.md
├─ Labs/                  # Matching project Labs (00–05)
│  ├─ 00-treasure-hunt-basic.md
│  ├─ 01-treasure-hunt-functions.md
│  ├─ 02-sense-hat-reaction-timer.md
│  ├─ 03-pico-breadboard-lab.md
│  ├─ 04-picobot-drive-basics.md
│  └─ 05-picobot-obstacle-sensing-maze-explorer.md
├─ Example_Code/          # Per-lab starter + mentor solution code
│  ├─ 00-treasure-hunt/
│  ├─ 01-treasure-hunt-functions/
│  ├─ 02-sense-hat-reaction-timer/
│  ├─ 03-pico-breadboard-lab/
│  ├─ 04-picobot-drive-basics/
│  └─ 05-picobot-obstacle-sensing-maze-explorer/
└─ assets/                # Images, wiring diagrams, and other media
   ├─ sense-hat/
   ├─ pico-breadboard/
   └─ picobot/
```

- Each **Guide** and **Lab** uses the same number (00–05) so they’re easy to pair.  
- Each Lab should have a matching folder under `Example_Code/` with:
  - `STUDENT_START.*` — starter or walkthrough code for students  
  - `SOLUTION.*` — mentor/coach-only reference solution  

If your local filenames differ slightly (for example, you keep `.updated.md` suffixes while editing), update the links above to match before publishing.

---

## 🤝 Contributing

We welcome fixes and improvements!

- **Branching:** create a feature branch (e.g., `feature/maze-tweaks`), then open a PR.  
- **File names & links:** use **dash form** for files (e.g., `05-picobot-obstacle-sensing-maze-explorer.md`).  
- **Scope discipline:**  
  - Keep `Labs/04-picobot-drive-basics.md` focused on **L298N drive basics (no sensors)**.  
  - Keep `Labs/05-picobot-obstacle-sensing-maze-explorer.md` focused on **ultrasonic sensing + maze behavior**.  
- **Example code layout:** align new labs with the `Example_Code/` pattern above.

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

---

## 🪪 License & attribution

Made with ❤️ by STEM Outreach volunteers & community mentors. Licensed under the **MIT License**.  
If you reuse or remix, please include attribution (“Code & Create Lab”).  
