import time
import psycopg2
from whatsapp_api_client_python import API
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QWidget
from AppWindow import Ui_MainWindow
from ContactWindow import Ui_Form
from InsertPersonWindow import Ui_Dialog

class App(QMainWindow):
    count = 0
    prev_button = None

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        self.insert_person = InsertPerson()
        self.contact = Contact()

        self.beggining_proccess()
        self.ui.settings_button.clicked.connect(self.open_settings_page)
        self.ui.new_message_button.clicked.connect(self.open_new_msg_page)
        self.ui.show_contact_button.clicked.connect(self.open_contact_window)
        self.ui.new_person_button.clicked.connect(self.open_new_person_window)
        self.insert_person.ui.insert_button.clicked.connect(self.insert_new_person)
        self.ui.delete_msg_button.clicked.connect(self.delete_msg)
        self.ui.send_button.clicked.connect(self.send_msg)
        self.ui.send_button_2.clicked.connect(self.send_msg)
        self.ui.increase_message_button.clicked.connect(self.increase_msg)
        self.ui.decrease_person_button.clicked.connect(self.decrease_person)
        self.ui.increase_person_button.clicked.connect(self.open_contact_window)
        self.contact.ui.insert_button.clicked.connect(self.increase_person)
        self.contact.ui.delete_button.clicked.connect(self.delete_person)
        self.ui.save_button.clicked.connect(self.save_msg)
        self.ui.dark_green_button.clicked.connect(self.update_sett)
        self.ui.beige_button.clicked.connect(self.update_sett)
        self.ui.brown_button.clicked.connect(self.update_sett)
        self.ui.grey_button.clicked.connect(self.update_sett)
        self.ui.light_green_button.clicked.connect(self.update_sett)
        self.ui.pink_button.clicked.connect(self.update_sett)
        self.ui.english_button.clicked.connect(self.update_sett)
        self.ui.information_button.clicked.connect(self.info_about_app)
        self.ui.previous_button.clicked.connect(self.previous_page)
        self.ui.previous_button_2.clicked.connect(self.previous_page)

    def beggining_proccess(self):
        """
        Method that runs when the application is started.
        It includes the following operations.\n
        1. PostgreSQL connects.\n
        2. Applies the saved contacts to Contact Window in application.\n
        3. Reads saved message information from database.\n
        4. Applies knowledge saved message information read.\n
        5. Reads saved theme and languages settings from database.\n
        6. Applies knowledge of theme and language read.
        """
        self.connect()
        self.contact_list()
        [self.msg_frame(msg) for msg in self.get_saved_title()]
        self.apply_sett(self.get_sett()["theme"], self.get_sett()["language"])

    def contact_list(self):
        """
        Method that applies the saved contacts to Contact Window in application.
        """
        row_count  = self.contact.ui.contact_list.rowCount()
        self.cur.execute('SELECT "tel_number" FROM contacts')
        numbers = self.cur.fetchall()
        self.cur.execute('SELECT "full_name" FROM contacts')
        names = self.cur.fetchall()
        for i in range(0, len(names)):
            self.contact.ui.contact_list.insertRow(row_count)
            self.contact.ui.contact_list.setItem(row_count, 0, QTableWidgetItem(str("".join(numbers[i]))))
            self.contact.ui.contact_list.setItem(row_count, 1, QTableWidgetItem(str("".join(names[i]))))
            row_count = row_count + 1

    def get_saved_title(self) -> list:
        """
        Method that reads saved message titles from database.
        """
        self.cur.execute('SELECT "title" FROM saved_message')
        msg_list = []
        [msg_list.append("".join(i)) for i in self.cur.fetchall()]
        return msg_list

    def get_sett(self) -> dict[str,str]:
        """
        Method that reads saved theme and languages settings from database.
        """
        self.cur.execute('SELECT "theme" FROM settings_info')
        theme = str("".join(self.cur.fetchone()))
        self.cur.execute('SELECT "language" FROM settings_info')
        lang = str("".join(self.cur.fetchone()))
        return {"theme": theme, "language": lang}
    
    def apply_sett(self, theme : str, lang : str):
        """
        Method that applies knowledge of theme and language read.
        """
        if theme == "pink":
            self.pink()
        elif theme == "grey":
            self.grey()
        elif theme == "dark_green":
            self.dark_green()
        elif theme == "light_green":
            self.light_green()
        elif theme == "beige":
            self.beige()
        elif theme == "brown":
            self.brown()
        if lang == "english":
            self.english()

    def open_settings_page(self):
        """
        Method that opens Settings Page (page_3).
        """
        self.ui.stackedWidget.setCurrentIndex(2)

    def open_new_msg_page(self):
        """
        Method that opens New Message Page (page_2).
        """
        self.clear_page()
        self.ui.stackedWidget.setCurrentIndex(1)
        self.prev_button = self.sender()

    def open_new_person_window(self):
        """
        Method that opens Insert Person Window.
        """
        self.insert_person.show()

    def insert_new_person(self):
        """
        Method that inserts new person to contacts in app and SQL.\n
        That person must have unique values, valid phone number (sample: +1234567890).
        That person must not have None value.
        """
        row_count  = self.contact.ui.contact_list.rowCount()
        full_name = self.insert_person.ui.full_name.text()
        phone_number = self.insert_person.ui.phone_number.text()
        if self.insert_person.none_value(full_name, phone_number) == True:
            self.none_value_error()
        elif self.unique_person(full_name, phone_number) == False:
            self.unique_person_error()
        elif self.insert_person.valid_number(phone_number) == False:
            self.insert_person.valid_number_error()
        else:
            self.cur.execute('INSERT INTO contacts (tel_number, full_name) VALUES (%s, %s);',(phone_number, full_name))
            self.contact.ui.contact_list.insertRow(row_count)
            self.contact.ui.contact_list.setItem(row_count, 1, QTableWidgetItem(full_name))
            self.contact.ui.contact_list.setItem(row_count, 0, QTableWidgetItem(phone_number))
            self.insert_person.clear_page()
            self.completed()

    def color_rgb(self, color: str):
        """
        Method that returns rgb values of theme colors.
        """
        if color == "pink":
            return "background-color: rgb(169, 117, 119);"
        elif color == "grey":
            return "background-color: rgb(170, 170, 170);"
        elif color == "dark_green":
            return "background-color: rgb(29, 71, 75);"
        elif color == "light_green":
            return "background-color: rgb(103, 128, 126);"
        elif color == "beige":
            return "background-color: rgb(197, 183, 173);"
        elif color == "brown":
            return "background-color: rgb(137, 119, 90);"
    
    def msg_frame(self, text: str):
        """
        Method that creates Message Frame in Main Page (page_1).\n
        It inculudes just PyQt5 GUI codes.
        """
        self.frame = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        self.frame.setMinimumSize(QtCore.QSize(0, 65))
        self.frame.setToolTip("")
        self.frame.setStyleSheet(self.color_rgb(color = self.get_sett().get("theme")))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame_{}".format(str(self.count)))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_box = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.message_box.setFont(font)
        self.message_box.setStyleSheet("")
        self.message_box.setIconSize(QtCore.QSize(40, 40))
        self.message_box.setCheckable(True)
        self.message_box.setChecked(False)
        self.message_box.setAutoRepeat(False)
        self.message_box.setAutoExclusive(False)
        self.message_box.setObjectName("message_box_{}".format(str(self.count)))
        self.message_box.setText("{}".format(text))
        self.horizontalLayout.addWidget(self.message_box)
        self.edit_button = QtWidgets.QPushButton(self.frame)
        self.edit_button.setMinimumSize(QtCore.QSize(30, 35))
        self.edit_button.setMaximumSize(QtCore.QSize(45, 16777215))
        self.edit_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.edit_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/1705774343469.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_button.setIcon(icon2)
        self.edit_button.setIconSize(QtCore.QSize(25, 30))
        self.edit_button.setObjectName("edit_button_{}".format(str(self.count)))
        self.horizontalLayout.addWidget(self.edit_button)
        self.ui.verticalLayout_3.addWidget(self.frame)
        self.edit_button.clicked.connect(self.edit_msg)
        self.count = self.count + 1

    def get_msg_info(self, title : str) -> dict[str, list, bool, int, int, list] | None:
        """
        Method that returns information about a message saved in the database as a dict.
        """
        msg_info = {"title": "",
                    "msg": [],
                    "auto_timer": None,
                    "wait_time": 0,
                    "repetition": 0,
                    "contacts": []}
        self.cur.execute("SELECT * FROM saved_message where title = '{}';".format(title,))
        i = self.cur.fetchone()
        if i != None:
            msg_info["title"] = title
            msg_info["msg"] = list(i[1])
            msg_info["auto_timer"] = i[2]
            msg_info["wait_time"] = i[3]
            msg_info["repetition"] = i[4]
            msg_info["contacts"] = list(i[5])
            return msg_info
        else:
            return None

    def fill_msg_info(self, msg_info : dict[str, list, bool, int, int, list]):
        """
        Method that shows the information which message saved in database in page_2.
        """
        self.ui.title.setText(msg_info["title"])
        for msg in msg_info["msg"]:
            self.increase_msg(msg)
        self.ui.auto_time_period_radio.setChecked(msg_info["auto_timer"])
        if msg_info["auto_timer"] == False:
            self.ui.time_period_radio.setChecked(True)
            self.ui.second.setValue(msg_info["wait_time"])
        self.ui.piece.setValue(msg_info["repetition"])
        self.ui.contacts.addItems(msg_info["contacts"])

    def increase_msg(self, msg : str):
        """
        Method that creates Text Edit for a new message.
        It inculudes just PyQt5 GUI codes.
        """
        self.message = QtWidgets.QTextEdit(self.ui.messages_area)
        self.message.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.message.setFont(font)
        self.message.setToolTip("")
        self.message.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self.message.setObjectName("message_{}".format(str(self.count)))
        self.ui.verticalLayout_5.addWidget(self.message)
        self.ui.message_scroll_area.setWidget(self.ui.messages_area)
        self.ui.gridLayout.addWidget(self.ui.message_scroll_area, 3, 1, 1, 5)
        if msg == False:
            self.message.setText("")
        else:
            self.message.setText("{}".format(msg))

    def edit_msg(self):
        """
        Method that fills the page_2 with the information of the selected message.
        """
        self.prev_button = self.sender()
        object_number = self.prev_button.objectName().replace("edit_button","")
        child = self.ui.scrollAreaWidgetContents.findChild(QtWidgets.QCheckBox, "message_box"+ object_number)
        self.open_new_msg_page()
        for i in self.ui.message_scroll_area.findChildren(QtWidgets.QTextEdit):
            i.close()
        self.fill_msg_info(self.get_msg_info(child.text()))

    def selected_msg(self) -> list | None:
        """
        Method that returns information of the selected message/messages.
        """
        titles = []
        msg_info = []
        if self.ui.stackedWidget.currentIndex() == 0:
            children = self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QCheckBox)
            for i in children:
                if i.isChecked() == True:
                    titles.append(i.text())
            if len(titles) == 0:
                return None
        elif self.ui.stackedWidget.currentIndex() == 1:
            titles.append(self.ui.title.text())
        [msg_info.append(self.get_msg_info(i)) for i in titles]
        return msg_info

    def tel_number(self, name : str) -> str:
        """
        Method that returns phone number of the person whose name we know.
        """
        tel_number = ""
        self.cur.execute('SELECT "tel_number" FROM contacts WHERE full_name = %s',(name,))
        tel_number = str("".join(self.cur.fetchone()))
        return tel_number
        
    def send_msg(self):
        """
        Method that sends msg.
        """
        messages = self.selected_msg()
        if messages == None:
            self.selected_error()
        elif self.confirmation() == True:
            for msg in messages:
                greenAPI = API.GreenAPI("idInstance", "apiTokenInstance")
                if msg["auto_timer"] == True:
                    for r in range(0, msg["repetition"]):
                        for m in msg["msg"]:
                            time.sleep(len(str(m))*0.75)
                            for p in msg["contacts"]:
                                greenAPI.sending.sendMessage("{}@c.us".format(self.tel_number(p).lstrip("+")), "{}".format(m))
                else:
                    for r in range(0, msg["repetition"]):
                        for m in msg["msg"]:
                            time.sleep(msg["wait_time"])
                            for p in msg["contacts"]:
                                greenAPI.sending.sendMessage("{}@c.us".format(self.tel_number(p).lstrip("+")), "{}".format(m))
                self.completed()

    def delete_msg(self):
        """
        Method that deletes a saved message in the database and the message frame in page_1.
        """
        children_cbox = self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QCheckBox)
        if len(children_cbox) < 1:
            self.selected_error()
        elif self.confirmation() == True:
            for i in children_cbox:
                if i.isChecked() == True:
                    self.cur.execute('DELETE FROM saved_message WHERE "title" = %s;',(i.text(),))
                    self.conn.commit()
                    object_number = i.objectName().replace("message_box", "")
                    self.ui.scrollAreaWidgetContents.findChild(QtWidgets.QFrame, "frame"+ object_number).close()
            self.completed()

    def clear_page(self):
        """
        Method that clears values in page_2.
        """
        self.ui.title.clear()
        children = self.ui.message_scroll_area.findChildren(QtWidgets.QTextEdit)
        for i in children:
            i.close()
        self.increase_msg("")
        self.ui.auto_time_period_radio.setChecked(True)
        self.ui.second.setValue(0)
        self.ui.piece.setValue(1)
        self.ui.contacts.clear()

    def increase_person(self):
        """
        Method that inserts the target contact to the list. (From Table QWidget in Contact Window to QComboBox in page_2).
        """
        person = self.contact.person()
        if self.ui.contacts.findText(person, QtCore.Qt.MatchExactly) == -1:
            if person != None:
                self.ui.contacts.addItem(person)

    def isExist(self, person : str) -> bool:
        """
        Method that returns whether the contact is included in information about the saved message.
        """
        exist = False
        self.cur.execute('SELECT contacts FROM saved_message')   
        contact_lists = self.cur.fetchall()
        for lists in contact_lists:
            for p in lists:
                if p == person:
                    exist = True
        if self.ui.contacts.findText(person, QtCore.Qt.MatchExactly) != None:
            exist = True
        return exist

    def delete_person(self):
        """
        If the person is not exist in the saved messages,
        Method that deletes person from database and contacts in Contact Window.
        """
        if self.confirmation() == True:
            current_row = self.contact.ui.contact_list.currentRow()
            col = self.contact.ui.contact_list.currentItem().column()
            person = self.contact.ui.contact_list.currentItem().text()
            exist = False
            if col == 0:
                self.cur.execute('SELECT full_name FROM contacts WHERE "tel_number" = %s;',(person,))
                person = "".join(self.cur.fetchone())
                exist = self.isExist(person)
            elif col == 1:
                exist = self.isExist(person)
            if exist == False:
                self.cur.execute('DELETE FROM contacts WHERE "full_name" = %s;',(person,))
                self.conn.commit()
                self.contact.ui.contact_list.removeRow(current_row)
            else:
                self.exist_person_error()
            
    def decrease_person(self):
        """
        Method that deletes the target contact to the list.
        """
        self.ui.contacts.removeItem(self.ui.contacts.currentIndex())

    def current_msg_info(self) -> dict[str, list, bool, int, int, list]:
        """
        Method that returns the current message information read from page_2 to save the message.
        """
        title = self.ui.title.text()
        messages = ""
        children = self.ui.message_scroll_area.findChildren(QtWidgets.QTextEdit)
        for i in children:
            messages = messages + i.toPlainText() + (',')
        messages = str('{') + messages.lstrip(",").rstrip(",") + str('}')
        auto_timer = self.ui.auto_time_period_radio.isChecked()
        wait_time = None
        if auto_timer == False:
            wait_time = self.ui.second.value()
        repetition = self.ui.piece.value()
        contacts = ""
        for i in range(0, self.ui.contacts.count()):
            contacts = contacts + self.ui.contacts.itemText(i) + (',')
        contacts = str('{') + contacts.lstrip(",").rstrip(",") + str('}')
        msg_info = {"title": title,
                    "msg": messages,
                    "auto_timer": auto_timer,
                    "wait_time": wait_time,
                    "repetition": repetition,
                    "contacts": contacts}
        return msg_info

    def save_msg(self):
        """
        Method that saves the message to database and page_1.
        If it is a new message it creates message frame.
        """
        if self.none_value() == True:
            self.none_value_error()
        elif self.confirmation() == True:
            msg_info = self.current_msg_info()
            if self.prev_button.objectName() == self.ui.new_message_button.objectName():
                if self.unique_title() == False:
                    self.unique_title_error()
                else:
                    insert_query = """INSERT INTO saved_message (title, message, auto_timer, wait_time,
                    repetition, contacts) VALUES (%s, %s, %s, %s, %s, %s);"""
                    self.cur.execute(insert_query, (msg_info["title"], msg_info["msg"], msg_info["auto_timer"], msg_info["wait_time"],
                        msg_info["repetition"], msg_info["contacts"]))
                    self.msg_frame(msg_info["title"])
                    self.conn.commit()
                    self.completed()
            else:
                update_query = """UPDATE saved_message SET title = %s, message = %s, auto_timer = %s,
                    wait_time = %s, repetition = %s, contacts = %s WHERE title = %s;"""
                self.cur.execute(update_query, (msg_info["title"], msg_info["msg"], msg_info["auto_timer"], msg_info["wait_time"],
                    msg_info["repetition"], msg_info["contacts"], msg_info["title"]))
                child = self.ui.scrollAreaWidgetContents.findChild(QtWidgets.QCheckBox, "message_box"+ self.prev_button.objectName().replace("edit_button",""))
                child.setText(msg_info["title"])
                self.conn.commit()
                self.completed()

    def update_sett(self):
        """
        Method that updates settings and saves database.
        """
        button = self.sender()
        if button.objectName() == "english_button":
            self.cur.execute("UPDATE settings_info SET language = 'english';")
            self.english()
        else:
            self.cur.execute("UPDATE settings_info SET theme = '{}';".format(button.objectName().replace("_button","")))
            self.apply_sett(button.objectName().rstrip("_button"))
        self.conn.commit()
        self.completed()

    def dark_green(self):
        """
        Method that applies dark green theme.
        """
        self.ui.stackedWidget.setStyleSheet("background-color: rgb(59, 101, 105); color: rgb(255, 255, 255);")
        self.insert_person.ui.widget.setStyleSheet("background-color: rgb(59, 101, 105); color: rgb(255, 255, 255);")
        self.contact.ui.widget.setStyleSheet("background-color: rgb(59, 101, 105); color: rgb(255, 255, 255);")
        self.insert_person.ui.insert_button.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        for i in self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QFrame):
            i.setStyleSheet("background-color: rgb(29, 71, 75); color: rgb(255, 255, 255);")

    def light_green(self):
        """
        Method that applies light green theme.
        """
        self.ui.stackedWidget.setStyleSheet("background-color: rgb(133, 158, 156);")
        self.insert_person.ui.widget.setStyleSheet("background-color: rgb(133, 158, 156);")
        self.contact.ui.widget.setStyleSheet("background-color: rgb(133, 158, 156);")
        for i in self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QFrame):
            i.setStyleSheet("background-color: rgb(103, 128, 126);")
        
    def pink(self):
        """
        Method that applies pink theme.
        """
        self.ui.stackedWidget.setStyleSheet("background-color: rgb(199, 147, 149);")
        self.insert_person.ui.widget.setStyleSheet("background-color: rgb(199, 147, 149);")
        self.contact.ui.widget.setStyleSheet("background-color: rgb(199, 147, 149);")
        for i in self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QFrame):
            i.setStyleSheet("background-color: rgb(169, 117, 119);")
        
    def grey(self):
        """
        Method that applies grey theme.
        """
        self.ui.stackedWidget.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.insert_person.ui.widget.setStyleSheet("background-color:  rgb(200, 200, 200);")
        self.contact.ui.widget.setStyleSheet("background-color:  rgba(200, 200, 200, 200);")
        for i in self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QFrame):
            i.setStyleSheet("background-color: rgb(170, 170, 170);")
        
    def brown(self):
        """
        Method that applies brown theme.
        """
        self.ui.stackedWidget.setStyleSheet("background-color: rgb(167, 149, 120);")
        self.insert_person.ui.widget.setStyleSheet("background-color: rgb(167, 149, 120);")
        self.contact.ui.widget.setStyleSheet("background-color: rgb(167, 149, 120);")
        for i in self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QFrame):
            i.setStyleSheet("background-color: rgb(137, 119, 90);")

    def beige(self):
        """
        Method that applies beige theme.
        """
        self.ui.stackedWidget.setStyleSheet("background-color: rgb(227, 213, 203);")
        self.insert_person.ui.widget.setStyleSheet("background-color: rgb(227, 213, 203);")
        self.contact.ui.widget.setStyleSheet("background-color: rgb(227, 213, 203);")
        for i in self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QFrame):
            i.setStyleSheet("background-color: rgb(197, 183, 173);")

    def english(self):
        """
        Method that applies english lang. (Method that does nothing for now.)
        """
        pass

    def open_contact_window(self):
        """
        Method that opens Contact Window.
        """
        self.contact.show()

    def info_about_app(self):
        """
        Method that opens the message box about application.
        """
        info = """Application that allows you to send the messages you have saved
        via WhatsApp with the recorded message feature."""
        QMessageBox.about(self, "About app", info)

    def previous_page(self):
        """
        Method that opens page_1.
        """
        self.ui.stackedWidget.setCurrentIndex(0)
        self.clear_page()

    def connect(self):
        """
        Method that connections PostgreSQL.
        """
        self.conn = None
        try:
            self.conn = psycopg2.connect(host = "localhost",
                                         database="wpsm",
                                         user="postgres",
                                         password="secret")
            self.cur = self.conn.cursor()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def disconnect(self):
        """
        Method that disconnections PostgreSQL
        """
        self.conn.commit()
        self.cur.close()
        if self.conn is not None:
            self.conn.close()
            
    def unique_person(self, name: str, number : str) -> bool:
        """
        Method that returns whether the entered name or number values exist in the contact book.
        """
        if (len(self.contact.ui.contact_list.findItems(name, QtCore.Qt.MatchExactly)) >= 1 or
            len(self.contact.ui.contact_list.findItems(number, QtCore.Qt.MatchExactly))) >= 1:
            return False
        else:
            return True
        
    def unique_person_error(self):
        text = """There is a person with a number or name value. Entered values must be unique."""
        QMessageBox.warning(self, "Unique Person Error", text, QMessageBox.Ok)

    def confirmation(self) -> bool:
        text = """Are you sure you want to continue?"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(text)
        msg_box.setWindowTitle("Confirmation")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setEscapeButton(QMessageBox.No)
        result = msg_box.exec_()
        if result == QMessageBox.Yes:
            return True
        else:
            return False

    def completed(self):
        text = """Congratulations, the proccess has been completed successfully."""
        QMessageBox.information(self, "completed", text, QMessageBox.Ok)

    def selected_error(self):
        text = """The selected message was not found. At least one message must be selected to continue the proccess."""
        QMessageBox.warning(self, "Selected Message Error", text, QMessageBox.Ok)

    def unique_title(self) -> bool:
        """
        Method that checks whether the current title value is unique while saving a new message.
        """
        titles = self.get_saved_title()
        for i in titles:
            if str(i) == self.ui.title.text():
                return False
        return True

    def unique_title_error(self):
        text = """The entered title value already exists, enter another one."""
        QMessageBox.warning(self, "unique title error", text, QMessageBox.Ok)

    def none_value(self) -> bool:
        """
        Method that checks whether required fields are null when saving the message.
        """
        if len(self.ui.title.text()) < 1:
            return True
        if self.ui.contacts.count() < 1:
            return True
        return False
    
    def none_value_error(self):
        text = """Required fields connat be left blank."""
        QMessageBox.warning(self, "None Value Error", text, QMessageBox.Ok)

    def exist_person_error(self):
        text = """Contact exist in saved messages or current message cannot be deleted."""
        QMessageBox.warning(self, "exist person error", text, QMessageBox.Ok)


class InsertPerson(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def clear_page(self):
        """
        Method that clears Insert Person Window.
        """
        self.ui.full_name.clear()
        self.ui.phone_number.clear()

    def none_value(self, name : str, number : str) -> bool:
        """
        Method that checks whether required fields are null when saving the person.
        """
        if len(str(name).replace(" ","")) <= 1:
            return True
        if len(str(number).replace(" ","")) <= 1:
            return True
        return False

    def valid_number(self, number : str) -> bool:
        """
        Method that checks whether the number is valid or not.\n
        Sample valid number: +country code 1234567890
        """
        if str(number).count("+") != 1:
            return False
        if str(number).startswith("+") == False:
            return False
        for i in str(number):
            if i not in "+1234567890 ":
                return False
        return True

    def valid_number_error(self):
        text = """The phone number entered is invalid. The phone number must be entered as in the example:\n
                    \tsample phone number: +1 1234567890"""
        QMessageBox.warning(self, "Invalid Number Error", text, QMessageBox.Ok)

class Contact(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def person(self) -> str:
        """
        Method that returns the current contact in the name column.
        """
        if self.ui.contact_list.currentItem().column() == 1:
            person = self.ui.contact_list.currentItem().text()
            return person
        