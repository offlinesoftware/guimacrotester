# guimacrotester
GUI Macro Tester

## Running on Debian- or Ubuntu-based Linux
```
sudo apt install libxcb-cursor0
cd guimacrotester
python -m venv venv
source venv/bin/activate
pip install pyside6
pip install pynput
python src/main.py
```

## To do
- Allow chaining of macros
  - Swap sequence table to top half of display
  - Bottom half to take macros from file or current recording
  - Need to name them
  - Allow sending any sequence in macrosequence up to editing table

- Programatic features
  - Allow for-loops with incrementing values
  - Allow running of macro with custom string for eg. program name

- Allow editing of macros via sequence table
  - Enable or disable cells as editable appropriately
  - Call things different names in table compared to macro dict
  - Allow changing order of events
  - Requires playback from table, not just dict

- Allow master offset of all co-ordinates
  - Either by clicked example or entering x/y values
  - Maybe this replaces notion of screen area?
