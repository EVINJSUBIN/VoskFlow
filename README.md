# VoskFlow 🎙️⌨️

yoo so basically this is a completly offline, on-device alternative to Wispr Flow. it runs entirely on your local pc so no cloud api keys or privacy issues at all! u just hold a hotkey and talk, and it types it out anywhere. 

## what it does
- **super fast offline dictation:** we use faster-whisper so it punctuates and capitilizes evreything perfectly.
- **global hotkey:** just hold `Ctrl + Space` (u can change this) to start recording. release it and boom, it types.
- **auto types:** it literalley simulates native keyboard events so u can use it in discord, vscode, chome, or whatever active window you have.
- **glass UI:** it has a super clean black glassmorphism pill at the bottom of the screen that bounces to your voice volume!

## how to run it
im assuming u have python installed. 
1. install the stuff: `pip install -r requirements.txt`
2. run it: `python main.py`
3. a lil blue icon will appear in your system tray (bottom right). right click it to open the dashboard and change the wave colors or hotkey.
4. hold `ctrl+space` and talk! 

*(btw the first time u run it, it might freeze for a sec to download the AI model. just give it a min)*

## devlogs

**Day 1: UI and stuff**
built the UI. tkinter sucked so we switched to PyQt6. made a crazy 7-bar audio wave animation that reacts to your mic and added a faux-glass background so it looks exactly like wispr flow. also made it a system tray app.

**Day 2: the engine!!** 
we swapped to faster-whisper cuz its way better. built a background worker to stream audio so there is basically zero latency when u release the key. also added a filter to automatically delete "umm" and "ahh" from the text before it types.

next up: LLM commands so u can say "undo" and it actually presses ctrl+z!!
