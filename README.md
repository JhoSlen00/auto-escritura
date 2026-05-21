# KODO - Auto Typing Tool

KODO is a desktop application that automatically types text into any input field on your screen. You write the text once, click where you want it typed, and the app does the rest.


## Requirements

- Python 3.x
- pyautogui
- Pillow

Install dependencies:

    pip install pyautogui pillow


## How to run

    python auto_escritura.py


## How to use

1. Type or paste the text you want to be typed automatically into the text area.
2. Set the number of seconds you want to wait before typing starts (default is 3).
3. Click the **Type** button.
4. During the countdown, click on the field where you want the text to appear.
5. The app will start typing automatically once the timer runs out.


## Buttons

**Type**
Starts the auto-typing process. Disabled while typing is in progress.

**Stop**
Immediately cancels the typing process at any point.

**TAB**
Inserts a tab separator ( | ) at the cursor position in the text area.
Use this to split your text into multiple fields. The app will press the Tab key
between each section, allowing you to fill multiple fields in sequence.

**Clear text**
Deletes everything in the text area.

**⚡ Speed**
Opens the typing speed control window. Click it again to close it.
The window is resizable and stays linked to the main window.


## Typing speed

Click the **⚡ Speed** button at the top right to open the speed panel.
Use the **◀** and **▶** arrows to cycle through five presets:

| Preset    | Interval per key |
|-----------|-----------------|
| Very Slow | 150 ms          |
| Slow      | 80 ms           |
| Normal    | 30 ms (default) |
| Fast      | 10 ms           |
| Turbo     | 3 ms            |

A timeline at the bottom of the panel shows your current position across all presets.
The selected speed applies immediately to the next typing session.


## Wait (seconds) field

Sets how many seconds you have to click on the target field before typing begins.
Only numbers are accepted. Default value is 3.


## TAB separator

To type across multiple fields automatically, use the TAB button to insert a separator
between sections. For example:

    John | Doe | john@email.com

The app will type "John", press Tab, type "Doe", press Tab, and type "john@email.com".


## Possible use cases

**Form filling**
Quickly fill out web forms or desktop app forms that you need to complete repeatedly
with the same or similar data. Paste your data once and let KODO type it for you.

**Login credentials**
Type long passwords or usernames into fields that block paste (Ctrl+V), since KODO
simulates real keystrokes instead of using the clipboard.

**Repetitive data entry**
Automate repetitive data entry tasks such as filling spreadsheets, CRMs, or internal
tools where copy-paste is restricted or slow.

**Multi-field workflows**
Use the TAB separator to fill entire forms in one go — name, email, phone, address —
moving from field to field automatically without touching the keyboard.

**Template text**
Store frequently used text snippets (email templates, standard responses, code blocks)
and type them instantly into any application.

**Accessibility**
Assist users who have difficulty typing quickly or accurately by letting them prepare
text at their own pace and then deploy it in any field with a single click.

**Testing and QA**
Simulate user input during manual testing of applications, filling fields with test
data without slowing down for manual typing.


## Notes

- The app handles both standard ASCII characters and special characters (accents, symbols, etc.).
- ASCII characters are typed directly. Non-ASCII characters are pasted via the clipboard.
- The window is resizable.
- KODO works with any application that accepts keyboard input: browsers, desktop apps, terminals, IDEs, and more.
