#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Wang YaoHua
# 
# Author:     Wang YaoHua <mr.asianwang@gmail.com>
# Maintainer: Wang YaoHua <mr.asianwang@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtDBus import QDBusAbstractInterface, QDBusConnection

idIndex = 0

DBUS_SERVICE = "com.deepin.menu"
DBUS_PATH = "/com/deepin/menu"
DBUS_INTERFACE = "com.deepin.menu.Menu"

class MenuServiceInterface(QDBusAbstractInterface):
    
    ItemInvoked = pyqtSignal(int)

    def __init__(self, ):
        super(MenuServiceInterface, self).__init__(DBUS_SERVICE, DBUS_PATH, DBUS_INTERFACE, 
                                                   QDBusConnection.sessionBus(), None)

    def showMenu(self, x, y, content):
        self.call('ShowMenu', x, y, content)
        
class MenuItem(object):
    def __init__(self, text, icon=None):
        self.id = None
        self.subMenu = Menu()
        
        self.text = text
        self.icon = icon
        
    @property
    def serializableContent(self):
        return {"itemId": self.id, 
                "itemIcon": self.icon, 
                "itemText": self.text, 
                "itemSubMenu": self.subMenu.serializableItemList}
        
    def setSubMenu(self, menu):
        self.subMenu = menu
        
    def setCallBack(self, cb):
        self.cb = cb
        
    def __str__(self):
        return json.dumps(self.serializableContent)
    
class MenuSeparator(object):
    pass

@pyqtSlot(int)
def itemInvoked(itemId):
    print itemId
        
class Menu(object):
    
    def __init__(self, items=None):
        # self.__items = items or []
        self.items = []
        if items:
            self.addMenuItems(items)
            
    @property
    def serializableItemList(self):
        result = []
        for item in self.items:
            result.append(item.serializableContent)
        return result
    
    def addMenuItem(self, item):
        global idIndex
        idIndex += 1
        item.id = idIndex
        self.items.append(item)
        
    def addMenuItems(self, items):
        for item in items:
            self.addMenuItem(item)
        
    def show(self, x, y):
        iface = MenuServiceInterface()
        iface.showMenu(x, y, str(self))
        iface.ItemInvoked.connect(itemInvoked)
        
    @pyqtSlot(int)        
    def itemInvokedSlot(self, itemId):
        print "itemId: ", itemId
        for item in self.items:
            if item.id == itemId:
                pass            # invoke callback function here

    def __str__(self):
        return json.dumps(self.serializableItemList)

if __name__ == "__main__":
    import sys
    from PyQt5.QtCore import QCoreApplication
    
    app = QCoreApplication([])
    
    driver = MenuItem("Driver", "/usr/share/icons/Deepin/apps/16/preferences-driver.png")
    display = MenuItem("Display", "/usr/share/icons/Deepin/apps/16/preferences-display.png")
    show = Menu([MenuItem("Display", "/usr/share/icons/Deepin/apps/16/preferences-display.png")])
    display.setSubMenu(show)
    menu = Menu([driver, display])
    menu.show(200, 200)
    
    sys.exit(app.exec_())