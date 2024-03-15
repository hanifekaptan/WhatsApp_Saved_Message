# Author: Hanife Kaptan

# Description: It is an application that sends saved repeated messages via WhatsApp
# to the desired person/persons without requiring rewriting.

# Version: psycopg2 (2.9.6), PyQt5 (5.15.10), PyQt5Designer (5.14.1), whatsapp-api-client-python (0.0.44), python (3.11.2)

from PyQt5.QtWidgets import QApplication
from App import App

app = QApplication([])
window = App()
window.show()
app.exec_()
window.disconnect()
