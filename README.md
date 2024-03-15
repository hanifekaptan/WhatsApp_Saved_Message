# WhatsApp_Saved_Message
The application, made using Python, PyQt5, PyQt5 Designer and Green API, sends the saved repeated messages via WhatsApp to the desired person(s) without requiring rewriting message(s) as many time as desired. The aim of this application is to send the repeated messages saved automatically with a single touch. The information within the application is stored in the PostgreSQL database to be read before the saved message content is sent. It is not recommended to update the information manually in the database. Sending messages is done via Green API.

Shortcomings and weakness:
1. The application works connected to a database and the user is responsible for making this connection.
2. The codes responsible for creating the database and tables required for PostgreSQL are located in the BeforeMain.py file.
3. Green API, which is used to send WhatsApp messages, is a paid API, but it also has a free plan that offers trial opportunities for developers. The user must use his/her own information in the App.py file in accordance with the intended use.
