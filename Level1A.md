# Level 1A – Raspberry Pi Setup

Welcome to Lesson 1A of the Code and Create Lab! In this part, you will focus on getting your Raspberry Pi set up and ready to go. No coding yet—just the essentials to get started!

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/Pi3Setup.jpg" width="400" > 
    
---

## 🚀 Goals

* Connect Raspberry Pi to monitor, keyboard, and mouse
* Boot the Raspberry Pi
* Connect to Wi-Fi
* Open the terminal
* Understand the Raspberry Pi desktop environment

---

## ⚖️ Materials Needed

* Raspberry Pi (any model with desktop OS installed)
* MicroSD card (preloaded with Raspberry Pi OS)
* Monitor and HDMI cable
* Keyboard and mouse
* Power supply

---

## 🧩 What Is the Raspberry Pi 3? (10 min)
- Overview of ports (USB, HDMI, GPIO, SD card)
- Differences from a regular laptop
- Introduce concept of general-purpose computing and sensors

    <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/RPi3-B-intro.jpg" width="400" > 

---
## ⚡ Step-by-Step Instructions

### 1. Connect Your Pi

* Insert the microSD card into the Raspberry Pi.
* Connect the keyboard, mouse, and monitor.
* Plug in the power supply to turn on your Pi.

    <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/Connecting.jpg" width="400" > 
    
    <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/Connected.jpg" width="400" > 


### 2. First Boot

* Wait for the Raspberry Pi OS to start.
* Follow the on-screen setup: choose country, time zone, and set a password.

### 3. Connect to Wi-Fi

* Click the network icon (top right) and choose your Wi-Fi.
* Enter the password to connect.

### 4. Update the System

Open the terminal and type:

```bash
sudo apt update && sudo apt full-upgrade
```

Press Enter and wait for the update to finish.

### 5. Explore the Desktop

* Open the terminal (black icon on top bar)
* Open the Raspberry Pi menu (top left corner)
* Find Thonny Python under Programming menu

---

## 🔧 Helpful Tips

* If your Pi doesn’t boot, check that the SD card is inserted properly.
* Use a good quality power supply—low power can cause problems.
* Don’t remove the power plug without shutting down! Use the shutdown option in the menu.

---

## 🎯 What’s Next?

You're ready for [Level 1B](Level1B.md), where you'll write your first Python programs! 
