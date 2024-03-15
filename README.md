# WhatsApp_Saved_Message
The application, made using Python, PyQt5, PyQt5 Designer and Green API, sends the saved repeated messages via WhatsApp to the desired person(s) without requiring rewriting message(s) as many time as desired. The aim of this application is to send the repeated messages saved automatically with a single touch. The information within the application is stored in the PostgreSQL database to be read before the saved message content is sent. It is not recommended to update the information manually in the database. Sending messages is done via Green API.

Shortcomings and weakness:
1. The application works connected to a database and the user is responsible for making this connection.
2. The codes responsible for creating the database and tables required for PostgreSQL are located in the BeforeMain.py file.
3. Green API, which is used to send WhatsApp messages, is a paid API, but it also has a free plan that offers trial opportunities for developers. The user must use his/her own information in the App.py file in accordance with the intended use.

main page for beggining:  
![image](https://github.com/hnfkptn/WhatsApp_Saved_Message/assets/129584767/9f098a1d-7305-4b89-bfcd-21b9730e29c2)

insert new person:  
![image-1](https://github.com/hnfkptn/WhatsApp_Saved_Message/assets/129584767/907d16a5-2dea-4a42-9c79-ca79794af47f)

new message page:  
![image-2](https://github.com/hnfkptn/WhatsApp_Saved_Message/assets/129584767/82858317-d8b6-4466-b267-4af72c7b76bc)

insert target person:  
![image-3](https://github.com/hnfkptn/WhatsApp_Saved_Message/assets/129584767/e0621e77-3589-4959-a1ef-f5856fef9f59)

main page with saved message:  
![image-4](https://github.com/hnfkptn/WhatsApp_Saved_Message/assets/129584767/069ee721-0b77-4262-901a-3a27621e2734)

settings page:  
![image-5](https://github.com/hnfkptn/WhatsApp_Saved_Message/assets/129584767/91fe623f-fb61-490f-b623-6777a6784200)
