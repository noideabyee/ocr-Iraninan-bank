import pytesseract
from PIL import Image
import sqlite3
from colorama import Fore
import pathlib

try:
    pytesseract.pytesseract.tesseract_cmd=r"C:\Users\Zahra\Tesseract-OCR\tesseract.exe"
    print('start..')

    img = Image.open('card5.jpeg')
    thresh=55
    fn = lambda x : 255 if x > thresh else 0 
    r = img.convert('L').point(fn, mode='1')
    r.save('convert.png')
    r.show()
    image=r"C:\Users\Zahra\convert.png"
    text=pytesseract.image_to_string(Image.open(image))

    text=str(text)
    text=text.replace(';','')
    text=text.replace(':','')
    text=text.replace(' ','')
    text=text.split('\n')

    for i in text:
        if i.isalnum():
            card_number=i[-16:] #16 raghame cart be dast miayad
    bank_id=card_number[:6] #6 ragham har bank
    # print(bank_id)
    file=pathlib.Path('customer.db')

    if not file.exists():
        conn= sqlite3.connect('customer.db')
        c=conn.cursor()
        c.execute("""CREATE TABLE bank(
            bank_name text,
            num_id integer
            )""")

        many_bank=[
            ('Melli Iran','603799'),
            ('Sepah','589210'),
            ('Saderat','627648'),
            ('Keshavarzi','603770'),
            ('Maskan','628023'),
            ('Tosee taavon','502908'),
            ('Eghtesad novin','627412'),
            ('Parsian','622106'),
            ('Pasargad','639347'),
            ('Kar Afarin','627488'),
            ('Saman','621988'),
            ('Sina','639366'),
            ('Sarmaye','639607'),
            ('Shahr','502806'),
            ('Dey','502938'),
            ('Saaderat','603769'),
            ('Mellat','610433'),
            ('Tejarat','627353'),
            ('Refah,','589463'),
            ('Ansar','627381')]
        c.executemany("INSERT INTO bank VALUES(?,?)",many_bank)
        print('updating')
    else:
        conn= sqlite3.connect('customer.db')
        c=conn.cursor()

    c.execute("SELECT * FROM bank WHERE num_id=?",(bank_id,))
    print(Fore.LIGHTBLUE_EX+'bank of your card is:'+c.fetchmany()[0][0])

    conn.commit()
    conn.close()
    print(Fore.LIGHTGREEN_EX+'its work succesfully') 
except:
    print(Fore.RED+'try to get better image \nprogram cant exactly work')
