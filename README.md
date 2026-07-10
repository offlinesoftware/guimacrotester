# guimacrotester
GUI Macro Tester

## Documentation
- In progress

## Backlog
- ~~Allowing loading macro-sequence from file~~
- Implement keyboard shortcuts
- ~~Add icons to GUI elements~~
- ~~Replace macro_sequence list with two-column table~~
- Allow chaining of macros
  - ~~Swap sequence table to top half of display~~
  - ~~Bottom half to take macros from file or current recording~~
  - ~~Need to name them~~
  - Allow sending any sequence in macrosequence up to editing table

- Programatic features
  - Allow for-loops with incrementing values
  - Allow running of macro with custom string for eg. program name
  - Allow pause for user to do something - 'Press any key to continue'

- Allow editing of macros via sequence table
  - Enable or disable cells as editable appropriately
  - Call things different names in table compared to macro dict
  - ~~Allow changing order of events~~
  - ~~Requires playback from table, not just dict~~

- MVC
  - Base both tables on QAbstractTableModel / QTableView

- Allow master offset of all co-ordinates
  - Either by clicked example or entering x/y value
