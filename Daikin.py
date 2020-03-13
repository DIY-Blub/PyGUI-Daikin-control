#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import configparser

# load config
ACconfig = configparser.ConfigParser()
ACconfig.read('src/AC-control-system.config')

# define design elements
Button_Icon_size = int(ACconfig["BUTTONS_DESIGN"]["button_icon_size"])
Button_size = int(ACconfig["BUTTONS_DESIGN"]["button_size"])
Button_BackgroundColor = ACconfig["BUTTONS_DESIGN"]["button_background-color"]
Button_BackgroundColor_pressed = ACconfig["BUTTONS_DESIGN"]["button_background-color_pressed"]

# define settings
useToolTip = ACconfig.getboolean("SETTINGS", "use_tooltips")
showTemperature = ACconfig.getboolean("SETTINGS", "show_temperature")
showWings = ACconfig.getboolean("SETTINGS", "show_wings")
showHumidity = ACconfig.getboolean("SETTINGS", "show_humidity")


class DaikinAC_control(object):
    def __init__(self):
        # initialization values
        self.currentPower = int(ACconfig["SETTINGS"]["ACpower"])
        self.currentMode = int(ACconfig["SETTINGS"]["ACmode"])
        self.currentWings = int(ACconfig["SETTINGS"]["ACwings"])
        self.currentTemp = int(ACconfig["SETTINGS"]["ACtemp"])
        self.currentFan = int(ACconfig["SETTINGS"]["ACfan"])
        self.currentHum = int(ACconfig["SETTINGS"]["AChum"])

    def setupUI(self, DialogAC):
        self.DialogAC = DialogAC
        self.DialogAC.setObjectName("DialogAC")
        self.DialogAC.resize(int(ACconfig["POSITIONS"]["dialog_width"]), int(ACconfig["POSITIONS"]["dialog_height"]))

        self.setDialogStylesheet()


        # SETUP POWER
        self.PushButtonPower = QtWidgets.QPushButton(self.DialogAC)
        self.PushButtonPower.setGeometry(QtCore.QRect(int(ACconfig["POSITIONS"]["power_x"]), int(ACconfig["POSITIONS"]["power_y"]), 80, 40))
        self.PushButtonPower.setMinimumSize(QtCore.QSize(80, 40))
        self.PushButtonPower.setStyleSheet("font-size:20px; text-align:left; padding:2px;")
        self.PushButtonPower.setProperty('class','ACButton')
        self.PushButtonPower.setText("OFF")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(ACconfig["PATHS"]["images"] + "AC_power.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PushButtonPower.setIcon(icon)
        self.PushButtonPower.clicked.connect(lambda: self.ButtonPower())


        # SETUP MODE
        self.mode = []
        for key in ACconfig["MODE_IMAGE"].keys():
            self.mode.append({'id':int(key), 'image': ACconfig["MODE_IMAGE"][key], 'text': ACconfig["MODE_TEXT"][key], 'value': int(ACconfig["MODE_VALUE"][key])})

        if len(self.mode) == 6:
            groupModeB = 221
        else:
            groupModeB = 181

        self.groupMode = QtWidgets.QGroupBox(self.DialogAC)
        self.groupMode.setGeometry(QtCore.QRect(int(ACconfig["POSITIONS"]["mode_x"]), int(ACconfig["POSITIONS"]["mode_y"]), groupModeB, 80))
        self.groupMode.setObjectName("groupMode")
        self.groupMode.setTitle(ACconfig["GROUP_TITLES"]["mode"])
        self.LayoutMode = QtWidgets.QHBoxLayout(self.groupMode)
        self.LayoutMode.setObjectName("LayoutMode")

        for mode in self.mode:
            button = QtWidgets.QToolButton()
            button.setMinimumSize(QtCore.QSize(Button_size, Button_size))
            button.setProperty('class',str("ACButton activemode" + str(mode['id'])))
            if useToolTip:
                button.setToolTip(mode['text'])
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(str(ACconfig["PATHS"]["images"] + mode["image"])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(Button_Icon_size, Button_Icon_size))
            button.clicked.connect(lambda pressed, arg=str(mode['id']): self.ButtonMode(arg))
            self.LayoutMode.addWidget(button)


        # SETUP WINGS
        if showWings:
            self.wings = []
            for key in ACconfig["WINGS_IMAGE"].keys():
                self.wings.append({'id':int(key), 'image': ACconfig["WINGS_IMAGE"][key], 'text': ACconfig["WINGS_TEXT"][key], 'value': int(ACconfig["WINGS_VALUE"][key])})

            self.groupWings = QtWidgets.QGroupBox(self.DialogAC)
            self.groupWings.setGeometry(QtCore.QRect(int(ACconfig["POSITIONS"]["wings_x"]), int(ACconfig["POSITIONS"]["wings_y"]), 121, 80))
            self.groupWings.setObjectName("groupWings")
            self.groupWings.setTitle(ACconfig["GROUP_TITLES"]["wings"])
            self.LayoutWings = QtWidgets.QHBoxLayout(self.groupWings)
            self.LayoutWings.setObjectName("LayoutWings")

            for wings in self.wings:
                button = QtWidgets.QToolButton()
                button.setMinimumSize(QtCore.QSize(Button_size, Button_size))
                button.setText(mode["text"])
                button.setProperty('class',str("ACButton activewings" + str(wings['id'])))
                if useToolTip:
                    button.setToolTip(wings['text'])
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(str(ACconfig["PATHS"]["images"] + wings["image"])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                button.setIcon(icon)
                button.setIconSize(QtCore.QSize(Button_Icon_size, Button_Icon_size))
                button.clicked.connect(lambda pressed, arg=str(wings['id']): self.ButtonWings(arg))
                self.LayoutWings.addWidget(button)


        # SETUP FAN
        self.fan = []
        for key in ACconfig["FAN_IMAGE"].keys():
            self.fan.append({'id':int(key), 'image': ACconfig["FAN_IMAGE"][key], 'text': ACconfig["FAN_TEXT"][key], 'value': int(ACconfig["FAN_VALUE"][key])})

        self.groupFan = QtWidgets.QGroupBox(self.DialogAC)
        self.groupFan.setGeometry(QtCore.QRect(int(ACconfig["POSITIONS"]["fan_x"]), int(ACconfig["POSITIONS"]["fan_y"]), 251, 80))
        self.groupFan.setObjectName("groupFan")
        self.groupFan.setTitle(ACconfig["GROUP_TITLES"]["fan"])
        self.LayoutFan = QtWidgets.QHBoxLayout(self.groupFan)
        self.LayoutFan.setObjectName("LayoutFan")

        for fan in self.fan:
            button = QtWidgets.QToolButton()
            button.setMinimumSize(QtCore.QSize(Button_size, Button_size))
            button.setText(mode["text"])
            button.setProperty('class',str("ACButton activefan" + str(fan['id'])))
            if useToolTip:
                button.setToolTip(fan['text'])
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(str(ACconfig["PATHS"]["images"] + fan["image"])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(Button_Icon_size, Button_Icon_size))
            button.clicked.connect(lambda pressed, arg=str(fan['id']): self.ButtonFan(arg))
            self.LayoutFan.addWidget(button)


        # SETUP TEMP
        if showTemperature:
            self.groupTemp = QtWidgets.QGroupBox(self.DialogAC)
            self.groupTemp.setGeometry(QtCore.QRect(int(ACconfig["POSITIONS"]["temp_x"]), int(ACconfig["POSITIONS"]["temp_y"]), 151, 100))
            self.groupTemp.setObjectName("groupTemp")
            self.groupTemp.setTitle(ACconfig["GROUP_TITLES"]["temp"])
            self.SpinboxTemp = QtWidgets.QSpinBox(self.groupTemp)
            self.SpinboxTemp.setGeometry(QtCore.QRect(5, 20, 100, 75))
            self.SpinboxTemp.setRange(18, 31)
            self.SpinboxTemp.setSingleStep(1)
            self.SpinboxTemp.setSuffix("°C")
            self.SpinboxTemp.setValue(int(ACconfig["SETTINGS"]["ACtemp"]))
            self.SpinboxTemp.valueChanged.connect(lambda: self.BoxTemp(self.SpinboxTemp.value()))


        # SETUP HUM
        if showHumidity:
            self.groupHum = QtWidgets.QGroupBox(self.DialogAC)
            self.groupHum.setGeometry(QtCore.QRect(int(ACconfig["POSITIONS"]["hum_x"]), int(ACconfig["POSITIONS"]["hum_y"]), 151, 100))
            self.groupHum.setObjectName("groupHum")
            self.groupHum.setTitle(ACconfig["GROUP_TITLES"]["hum"])
            self.SpinboxHum = QtWidgets.QSpinBox(self.groupHum)
            self.SpinboxHum.setGeometry(QtCore.QRect(5, 20, 100, 75))
            self.SpinboxHum.setRange(40, 60)
            self.SpinboxHum.setSingleStep(5)
            self.SpinboxHum.setSuffix("%")
            self.SpinboxHum.setValue(int(ACconfig["SETTINGS"]["AChum"]))
            self.SpinboxHum.valueChanged.connect(lambda: self.BoxHum(self.SpinboxHum.value()))


    def setDialogStylesheet(self):
        self.DialogAC.setStyleSheet(".QGroupBox, .QHBoxLayout, .QGridLayout, .QSpinBox {\n"
                             "    padding: 0px;\n"
                             "    margin: 0px;\n"
                             "    border: 0;\n"
                             "}\n"
                             ".QSpinBox {\n"
                             "    border: 1px solid grey;\n"
                             "    border-radius: 2px;\n"
                             "    background-color: " + Button_BackgroundColor + ";\n"
                             "    font-size: 20px;\n"
                             "}\n"
                             ".QSpinBox::up-button, .QSpinBox::down-button {\n"
                             "    width: " + str(Button_size) + "px;\n"
                             "    height: " + str(Button_size) + "px;\n"
                             "    border: 1px solid grey;\n"
                             "    border-radius: 2px;\n"
                             "    background-color: " + Button_BackgroundColor + ";\n"
                             "}\n"
                             ".QSpinBox::up-button:pressed, .QSpinBox::down-button:pressed {\n"
                             "    background-color: " + Button_BackgroundColor_pressed + ";\n"
                             "}\n"
                             ".QSpinBox::up-arrow {\n"
                             "    image: url(" + str(ACconfig["PATHS"]["images"]) + "AC_target_up.png);\n"
                             "    width: " + str(Button_Icon_size) + "px;\n"
                             "    height: " + str(Button_Icon_size) + "px;\n"
                             "}\n"
                             ".QSpinBox::down-arrow {\n"
                             "    image: url(" + str(ACconfig["PATHS"]["images"]) + "AC_target_down.png);\n"
                             "    width: " + str(Button_Icon_size) + "px;\n"
                             "    height: " + str(Button_Icon_size) + "px;\n"
                             "}\n"
                             ".ACButton {\n"
                             "    background-color: " + Button_BackgroundColor + ";\n"
                             "    border: 1px solid grey;\n"
                             "    border-radius: 2px;\n"
                             "}\n"
                             ".ACButton:pressed {\n"
                             "    background-color: " + Button_BackgroundColor_pressed + ";\n"
                             "}\n"
                             ".activepower {\n"
                             "    background-color: " + Button_BackgroundColor_pressed + ";\n"
                             "}\n"
                             ".activemode" + str(self.currentMode) + " {\n"
                             "    background-color: " + Button_BackgroundColor_pressed + ";\n"
                             "}\n"
                             ".activewings" + str(self.currentWings) + " {\n"
                             "    background-color: " + Button_BackgroundColor_pressed + ";\n"
                             "}\n"
                             ".activefan" + str(self.currentFan) + " {\n"
                             "    background-color: " + Button_BackgroundColor_pressed + ";\n"
                             "}"
                            )

    def ButtonPower(self):
        if self.currentPower == 0:
            self.currentPower = 1
            self.PushButtonPower.setText("ON")
            self.PushButtonPower.setProperty("class","ACButton activepower")
        elif self.currentPower == 1:
            self.currentPower = 0
            self.PushButtonPower.setText("OFF")
            self.PushButtonPower.setProperty("class","ACButton")
        else:
            self.currentPower = 0
            self.PushButtonPower.setText("OFF")
            self.PushButtonPower.setProperty("class","ACButton")
        self.setDialogStylesheet()
        self.setDaikinAC()

    def ButtonMode(self,button):
        self.currentMode = int(button)
        self.setDialogStylesheet()
        self.setDaikinAC()

    def ButtonWings(self,button):
        self.currentWings = int(button)
        self.setDialogStylesheet()
        self.setDaikinAC()

    def ButtonFan(self,button):
        self.currentFan = int(button)
        self.setDialogStylesheet()
        self.setDaikinAC()

    def BoxTemp(self,value):
        self.currentTemp = int(value)
        self.setDaikinAC()

    def BoxHum(self,value):
        self.currentHum = int(value)
        self.setDaikinAC()

    def setDaikinAC(self):
        # In this method the connection to the device should be established.
        print("Power: " + str(self.currentPower))
        print(ACconfig["GROUP_TITLES"]["mode"] + ": " + str(self.currentMode))
        print(ACconfig["GROUP_TITLES"]["wings"] + ": " + str(self.currentWings))
        print(ACconfig["GROUP_TITLES"]["temp"] + ": " + str(self.currentTemp))
        print(ACconfig["GROUP_TITLES"]["fan"] + ": " + str(self.currentFan))
        print(ACconfig["GROUP_TITLES"]["hum"] + ": " + str(self.currentHum))
        print("")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogAC = QtWidgets.QDialog()
    DaikinGUI = DaikinAC_control()
    DaikinGUI.setupUI(DialogAC)
    DialogAC.show()
    sys.exit(app.exec_())
