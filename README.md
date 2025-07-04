
# Code & Create Lab

**Learn by building.** Code & Create Lab is a self‑paced quest that walks students—from absolute beginners to budding roboticists—through the fundamentals of **Python programming**, **physical computing**, and **autonomous navigation**.

Each **Lab** is a milestone project.  Each **Guide** teaches the skills needed to beat that project.  By the final level you’ll have a mecanum‑wheel robot that can recognise AprilTags and drive itself around a course.

---

## 🎯 Updated Purpose

1. **Make STEM approachable** – lower the entry barrier so anyone (Grades 4–10 +) can start creating with code and electronics.  
2. **Turn theory into practice** – every concept is immediately applied in a real, working artefact.  
3. **Promote a growth mindset** – short wins build confidence; stretch goals reward curiosity.  
4. **Empower instructors & mentors** – modular guides, checklists, and wiring diagrams shorten prep time.

---

## 🧠 Core Concepts

| Theme | What you’ll learn |
|-------|-------------------|
| Python Fundamentals | `print`, `input`, variables, conditionals, loops, functions |
| Sensor I/O | Reading temperature, humidity, IMU, ultrasonic distance |
| Actuators & Signalling | LEDs, RGB colour mixing, DC & mecanum motors |
| Microcontrollers | Programming the Raspberry Pi Pico with MicroPython |
| Robotics Algorithms | Wall‑following, maze solving, PID tuning |
| Computer Vision | OpenCV basics, AprilTag detection, pose estimation |
| Engineering Practice | Breadboarding, wiring diagrams, iterative debugging |
| Collaboration | Pair‑programming tips, code reviews, documentation |

---

## 📂 Repository Layout (high‑level)

```text
Labs/        ← final challenge projects
Guides/      ← step‑by‑step how‑tos
Assets/      ← wiring diagrams, images, datasets
README.md    ← (this file)
```

---

## 🗺️ Learning Path

| Level | Lab | Highlights | Hardware | Time |
|:----:|------|------------|----------|------|
| **0** | Treasure Hunt | Text adventure, loops & logic | Computer only | 30 min |
| **1** | Sense HAT Basics | Environmental sensing, LED display | Pi + Sense HAT | 45 min |
| **1.5** | Sense HAT Mission Dashboard | Multi‑sensor fusion, joystick events | Same | 60 min |
| **2** | Pico Breadboarding | Button, ultrasonic, RGB LED | Pi Pico + breadboard | 60 min |
| **3.0** | PicoBot Maze Explorer | Motor control, obstacle avoidance | PicoBot | 90 min |
| **4.0** | MasterPi AprilTags Navigator | OpenCV, AprilTags, mecanum drive | MasterPi | 2 h |

> 🔗 **Guides** for each stage live in the `/Guides` folder.

---

## 📂 Full Repo Layout

```text
CodeCreateLab/
│
├── README.md
│
├── Labs/
│   ├── 0-Treasure_Hunt_Lab.md
│   ├── 1-SenseHat_Basic_Lab.md
│   ├── 1.5-SenseHat_Advance_Lab.md
│   ├── 2-Pico_Breadboarding_Lab.md
│   ├── 3.0-PicoBot_Lab.md
│   └── 4.0-MasterPi_Lab.md
│
├── Guides/
│   ├── Python_Basics_Guide.md
│   ├── SenseHat_Guide.md
│   ├── Pico_Breadboard_Guide.md
│   ├── PicoBot_Guide.md
│   └── MasterPi_AprilTags_Guide.md
│
└── Assets/
    └── (schematics, images, sample data)
```

---

## 🚀 Quick Start

1. **Clone the repo**

   ```bash
   git clone https://github.com/stemoutreach/CodeCreateLab.git
   cd CodeCreateLab
   ```

2. Pick a **Lab** from `/Labs`.  
3. Skim its **Guide** for wiring & install steps.  
4. Open the starter `.py`, fill the `# TODO:` blocks, and run!

---

## 🤝 Contributing

Pull requests and issue reports are welcome.  
Mentors: see `Guides/Mentoring_Tips.md` (coming soon) for checkpoints and facilitation advice.

---

Made with ❤️ by STEM Outreach volunteers & community mentors.  
Licensed under the MIT License.
