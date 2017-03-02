import sqlite3
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def InitTable():
    db = sqlite3.connect('Dad_app.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS 'historico' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'lancha' TEXT NOT NULL,
    'servico' TEXT NOT NULL,
    'data' DATE,
    'comentario' TEXT
    )''')
    db.close()

def InsertEntry (lancha, servico, data, comentario):
    db = sqlite3.connect('Dad_app.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO historico (lancha, servico, data, comentario)
        VALUES (?, ?, ?, ?)''',
        (lancha, servico, data, comentario))
    db.commit()
    db.close()

def SendEmail(msg_text):
    fromaddr = "jzerenato@gmail.com"
    toaddr = "jzerenato@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Python Email"
    body = msg_text
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, "lucas015")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

#ideia: enviar text pro email
def SendToEmail():
    today = datetime.date.today()
    db = sqlite3.connect('Dad_app.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = db.cursor()
    cursor.execute(
        '''SELECT lancha, servico, data, comentario FROM historico WHERE data < ?''', (today - datetime.timedelta(weeks=1),)
    )
    text = ''
    entradas = cursor.fetchall()
    db.close()
    for entrada in entradas:
        text = text+'Lancha: '+entrada[0]+'\n'+'Servico: '+entrada[1]+'\n'+'Data: '+str(entrada[2])+'\n'+'Comentario: '+entrada[3]+'\n\n'
    SendEmail(text)

def DeleteAfterLimit():
    today = datetime.date.today()
    db = sqlite3.connect('Dad_app.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = db.cursor()
    cursor.execute(
        '''DELETE FROM historico WHERE data < ?''', (today - datetime.timedelta(weeks=1),)
    )
    db.commit()
    db.close()

def SearchDate(dia, mes, ano):
    date = datetime.date(day=dia, month=mes, year=ano)
    db = sqlite3.connect('Dad_app.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = db.cursor()
    cursor.execute(
        '''SELECT lancha, servico, data, comentario FROM historico WHERE data = ?''', (date,)
    )
    entradas = cursor.fetchall()
    db.close()
    return entradas

def SearchLancha(nome):
    db = sqlite3.connect('Dad_app.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = db.cursor()
    cursor.execute(
        '''SELECT lancha, servico, data, comentario FROM historico WHERE lancha LIKE ?''', ('%'+nome+'%',)
    )
    entradas = cursor.fetchall()
    db.close()
    return entradas

def DeleteEntry(nome, data):
    db = sqlite3.connect('Dad_app.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = db.cursor()
    cursor.execute(
        '''DELETE FROM historico WHERE data = ? and lancha = ?''', (data, nome)
    )
    db.commit()
    db.close()
