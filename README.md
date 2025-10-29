
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

---

## ✅ Contribution guidelines
We welcome fixes and new content. Please:
- Follow the **NN‑prefix** and **kebab‑case** filenames used above.  
- Keep each Guide/Lab under ~2 pages; include **rubric**, **troubleshooting**, **extensions**.  
- Put images in `assets/` and use relative links.  
- Run Markdown/YAML checks (see below).

---

## 🔧 Quality checks (optional but recommended)
Add these to `.github/workflows/docs-qc.yml` to lint Markdown and validate links:

```yaml
name: Docs QC
on: [push, pull_request]
jobs:
  lint-and-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: DavidAnson/markdownlint-cli2-action@v15
        with:
          globs: "**/*.md"
      - name: Check links
        uses: lycheeverse/lychee-action@v1
        with:
          args: --verbose --no-progress --exclude-mailto "README.md **/*.md"
```

---

## 🪪 License & attribution
Made with ❤️ by STEM Outreach volunteers & community mentors. Licensed under the **MIT License**.  
If you reuse or remix, please include attribution (“Code & Create Lab”).

---

## 🙋 FAQ
**Do students need to install software?**  
- For **Pico** work, use **Thonny** with MicroPython firmware.  
- For **Sense HAT**, use Raspberry Pi OS with the `sense-hat` package.

**Can we reorder modules?**  
Yes—00 ↔ 01 are a pair; 02/02.5 (Sense HAT) and 03/04 (Pico → PicoBot) can run as separate tracks depending on hardware.

**Where are slides?**  
Use the **Guides** as your speaking notes. If you want a docs site, consider MkDocs + Material and point it at these files.
