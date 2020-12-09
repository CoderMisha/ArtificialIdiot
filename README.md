# ArtificialIdiot

## Recommended Way to Run

1. Run `cs175_color_map_monitor.py`, which will spawn a PyGame window to monitor the color map output.

2. Run `cs175_rllib.py`, **move your mouse cursor INTO the Minecraft window (but do NOT click)**. This will allow PyAutoGUI to do all kinds of stuff like turn around and interact with the button that Malo can't do.

## Notice

In case you need to take the control of your mouse, you can *move the cursor into the one of the corner of the display*, and the PyAutoGUI will raise a `pyautogui.FailSafeException`.
