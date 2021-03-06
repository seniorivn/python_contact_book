#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    import sys
    from PyQt5.QtWidgets import (QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout, QApplication, QMessageBox, QTableWidget, QTableWidgetItem
        )
    from contact import Contact
    import sqlite3
except ImportError as e:
    exit("You should resolve dependencies "+ str(e))

class MainWindow(QMainWindow):
    """Main window of contactbook gui"""
    def __init__(self, *args):
        super().__init__()

        self.initUI()


    def initUI(self):
        """init user interface"""
        self.database = QLabel('database')
        self.cid   = QLabel('contact id')
        self.fname = QLabel('First name')
        self.lname = QLabel('Last name')
        self.mname = QLabel('Middle name')
        self.phone = QLabel('Phone')
        self.bday = QLabel('Birthday date')

        self.databaseEdit = QLineEdit("./contacts.db")
        self.cidEdit = QLineEdit()
        self.fnameEdit = QLineEdit()
        self.lnameEdit = QLineEdit()
        self.mnameEdit = QLineEdit()
        self.phoneEdit = QLineEdit()
        self.bdayEdit  = QLineEdit()
        self.add = QPushButton("Add contact")
        self.delete = QPushButton("Delete contact")
        self.find = QPushButton("Find contact")
        self.lst = QPushButton("List of all contacts")
        self.remind = QPushButton("Remind birthdays")
        self.add.clicked.connect(self.addClicked)
        self.delete.clicked.connect(self.deleteClicked)
        self.find.clicked.connect(self.findClicked)
        self.lst.clicked.connect(self.lstClicked)
        self.remind.clicked.connect(self.remindClicked)

        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(self.database, 0, 0)
        grid.addWidget(self.databaseEdit, 0, 1, 1, 4)

        grid.addWidget(self.cid, 1, 0)
        grid.addWidget(self.cidEdit, 1, 1, 1, 4)

        grid.addWidget(self.fname, 2, 0)
        grid.addWidget(self.fnameEdit, 2, 1, 1, 4)

        grid.addWidget(self.mname, 4, 0)
        grid.addWidget(self.mnameEdit, 4, 1, 1, 4)

        grid.addWidget(self.lname, 5, 0)
        grid.addWidget(self.lnameEdit, 5, 1, 1, 4)

        grid.addWidget(self.phone, 6, 0)
        grid.addWidget(self.phoneEdit, 6, 1, 1, 4)

        grid.addWidget(self.bday, 7, 0)
        grid.addWidget(self.bdayEdit, 7, 1, 1, 4)

        grid.addWidget(self.add, 8, 0)
        grid.addWidget(self.delete, 8, 1)
        grid.addWidget(self.find, 8, 2)
        grid.addWidget(self.lst, 8, 3)
        grid.addWidget(self.remind, 8, 4)

        self.grid = grid
        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        self.setGeometry(400, 400, 350, 300)
        self.setWindowTitle('ContactBook')
        self.show()

    def addClicked(self):
        """add contact when button add clicked"""
        contact = self.getContact()
        c, connection = self.connectToDatabase()
        added, phoneexist, comment = contact.add(contact, c, ())
        if added:
            QMessageBox.question(self, 'Contact added', comment+" " + str(contact.get_tuple()), QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.question(self, 'Contact not added', comment, QMessageBox.Ok, QMessageBox.Ok)
        connection.commit()
        connection.close()
    def deleteClicked(self):
        """delete contact when button delete clicked"""
        contact = self.getContact()
        c, connection = self.connectToDatabase()
        result, comment =contact.delete(contact, c)
        self.showResult(result)
        if result:
            QMessageBox.question(self, 'Contact deleted', comment+" " + str(contact.get_tuple()), QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.question(self, 'Contact not deleted', comment, QMessageBox.Ok, QMessageBox.Ok)
        connection.commit()
        connection.close()
    def findClicked(self):
        """find contact when button find clicked"""
        contact = self.getContact()
        c, connection = self.connectToDatabase()
        finded=contact.find(contact, c)
        if finded:
            # print(tabulate(finded, headers=["Id","first name","last name","middle name","phone","birthday date"]))
            self.showResult(finded)
        else:
            self.showResult(finded)
            QMessageBox.question(self, 'Nothing finded', "there is no any contact "+(("like:"+str(contact)) if str(contact) else ""), QMessageBox.Ok, QMessageBox.Ok)
        connection.commit()
        connection.close()
    def lstClicked(self):
        """list all contacts"""
        contact = self.getContact()
        c, connection = self.connectToDatabase()
        result = contact.lst((), c)
        self.showResult(result)
        connection.close()
    def remindClicked(self):
        """Remind about birthdays in this or next month"""
        contact = self.getContact()
        c, connection = self.connectToDatabase()
        remind=contact.reminder(c)
        self.showResult(remind)
        if remind:
            QMessageBox.question(self, 'Reminder', "Don't forget about birthday congratulations", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.question(self, 'Reminder', "there is no one who have birthday in this or next month", QMessageBox.Ok, QMessageBox.Ok)
        connection.close()
    def showResult(self, contacts):
        """show table with results"""
        try:
            if contacts:
                self.table = QTableWidget(len(contacts),6)
                headers=["ID","first name","last name","middle name","phone","birthday date"]
                for i, h in enumerate(headers): 
                    self.table.setHorizontalHeaderItem(i,QTableWidgetItem(h))
                for i,c in enumerate(contacts):
                    for k,item in enumerate(c):
                        self.table.setCellWidget(i, k, QLabel(str(item)))
                self.grid.addWidget(self.table, 9, 0, 12, 0)
            else:
                self.grid.removeWidget(self.table)
                self.table.deleteLater()
                # self.grid.addWidget(QLabel("Empty Table"), 8, 0, 12, 0)
        except Exception as e:
            print(str(e))


    def getContact(self):
        """get contacts from fields in gui"""
        contact = Contact()
        try:
            contact.cid   = self.cidEdit.text()
            contact.fname = self.fnameEdit.text()
            contact.mname = self.mnameEdit.text()
            contact.lname = self.lnameEdit.text()
            contact.phone = self.phoneEdit.text()
            contact.bday  = self.bdayEdit.text()
        except Exception as e:
            QMessageBox.question(self, 'Error', str(e), QMessageBox.Ok, QMessageBox.Ok)
        return contact
    def connectToDatabase(self):
        database = self.databaseEdit.text()
        connection = sqlite3.connect(database)
        c = connection.cursor()
        try:
            c.execute("create table contacts(id integer primary key autoincrement, fname text, lname text, mname text, phone text, bday text)")
            self.statusBar().showMessage("new database " + database + " was created", 3000)
        except sqlite3.Error as e:
            self.statusBar().showMessage("Existing database " + database, 3000)
        return c, connection


    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class App(QApplication):
    """Main class of application"""
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.main = MainWindow()
        # self.connect(self, SIGNAL("lastWindowClosed()"), self.byebye )
        self.main.show()

    def byebye( self ):
        self.exit(0)
    def lastWindowClosed(self, event):
        self.byebye()

def main(args):
    global app
    app = App(args)
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
