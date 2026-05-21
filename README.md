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
3. Click the Type button.
4. During the countdown, click on the field where you want the text to appear.
5. The app will start typing automatically once the timer runs out.


## Buttons

Type
    Starts the auto-typing process. Disabled while typing is in progress.

Stop
    Immediately cancels the typing process at any point.

TAB
    Inserts a tab separator ( | ) at the cursor position in the text area.
    Use this to split your text into multiple fields. The app will press the Tab key
    on your keyboard between each section, allowing you to fill multiple fields in sequence.

Clear text
    Deletes everything in the text area.


## Wait (seconds) field

Sets how many seconds you have to click on the target field before typing begins.
Only numbers are accepted. Default value is 3.


## TAB separator

To type across multiple fields automatically, use the TAB button to insert a separator
between sections. For example:

    John | Doe | john@email.com

The app will type "John", press Tab, type "Doe", press Tab, and type "john@email.com".


## Notes

- The app handles both standard ASCII characters and special characters (accents, symbols, etc.).
- ASCII characters are typed directly. Non-ASCII characters are pasted via the clipboard.
- The window is resizable.
