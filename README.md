# PyGUI-Daikin-control

This library provides a graphical user interface (GUI) based on Python3 and PyQt5 to control a Daikin air conditioning unit.

No air conditioner is controlled yet! There is only an output in the terminal.

## Examples

![Example: Dialog](/.docs/example1_dialog.png?raw=true)

![Example: Implementation with Widget](/.docs/example2_implementation.png?raw=true)  ![Example: Implementation with Button (open Dialog)](/.docs/example3_pushbutton.png?raw=true)

Inspired by the web interface of the user "ael-code": https://github.com/ael-code/daikin-control

## Quick Start

1. `sudo apt install git python3 python3-pyqt5`
2. `git clone https://github.com/DIY-Blub/PyGUI-Daikin-control.git`
3. `python3 pygui-daikin-control/Daikin.py`

## Informations

* Most settings (e.g. texts, positioning, colours,...) can be changed in the config file [AC-control-system.config](src/AC-control-system.config)
* The connection to the air conditioner must be made in the Python file under the method setDaikinAC.

### Implementation options

1. As a standalone solution:

see Quick Start

2. To your own main using a QWidget container
```
from Daikin import *

DialogAC = QtWidgets.QWidget(YourMainWindow.WidgetName)

DaikinGUI = DaikinAC_control()

DaikinGUI.setupUI(DialogAC)
```
3. To your own main using a QPushButton
```
from Daikin import *

DialogAC = QtWidgets.QDialog()

DaikinGUI = DaikinAC_control()

DaikinGUI.setupUI(DialogAC)

YourMainWindow.PushButtonName.clicked.connect(lambda: DialogAC.show())
```

### Todo: connect to a Daikin air conditioning unit

* with MQTT and Node-RED: https://github.com/Apollon77/daikin-controller (untested)
* or with Python: https://github.com/ael-code/daikin-aricon-pylib (untested)

## Copyright protection images

The images are licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ .

Authors of the images are

* [Dave Gandy](https://icon-icons.com/de/pack/Font-Awesome-Icons/936)
* [Daniel Bruce](https://icon-icons.com/de/pack/-Entypo-Icons/1238)

Further information can be found in the src/images folder.

## Changelog
### v1.0.0 (13.03.2020)
* initial release
