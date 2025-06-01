# 🔍 Level 3 Challenge: Sense HAT Integration

## 🎯 Challenge Overview
You’ve learned how to use loops, conditionals, functions, and the Sense HAT. Now, put your skills together to build an interactive project!

---

## 🛠️ Challenge: Build a Mini Weather Display

Create a script that:
1. **Greets the user** using a function and scrolls a message on the LED.
2. **Displays current temperature or humidity** based on joystick input.
3. **Uses a loop** to keep checking for joystick presses.
4. **Exits** the loop and shows a “Goodbye” message when the user presses the middle button.

---

## 💡 Requirements

- Use at least **one function** to handle part of the logic.
- Use **`if/elif/else`** statements to handle joystick direction.
- Use **`while True`** loop to keep the program running.
- Use **`show_message()`** to display text on the LED.
- Read data using `get_temperature()` and `get_humidity()`.

---

## 🧪 Bonus Challenges

- Add pressure readings as an additional option.
- Change the **color** of the text based on the reading (e.g., blue for humidity, red for temperature).
- Use the joystick to cycle through all three sensor types.

---

## 💭 Example Structure (Pseudocode)

```python
show welcome message

while True:
    check joystick input
    if up: show temperature
    elif down: show humidity
    elif right: show pressure (bonus)
    elif middle: break loop and say goodbye
```

---

## ✅ Submission Checklist

Make sure your program includes:
- [ ] At least one custom function
- [ ] A `while` loop to keep the program running
- [ ] Conditional logic using `if/elif/else`
- [ ] Sense HAT input (joystick) and output (LED + sensor data)
- [ ] A clean and readable structure

---

[Back to Level 3 Overview](Level3.md)
