from socket import socket,AF_INET,SOCK_STREAM
from tkinter import *
from random import randint,choice
from tkinter import filedialog,messagebox
import threading,os,keyboard
import requests
from bs4 import BeautifulSoup
try:
    os.mkdir(f"C:/Users/{os.getlogin()}/Desktop/Online_Mesajlaşma_Uyg_Gelen_Fotolar")
except:pass

def klasor_ac():
    yol = f"C:/Users/{os.getlogin()}/Desktop/Online_Mesajlaşma_Uyg_Gelen_Fotolar"
    os.startfile(yol)
    
def dosyaadi_uret():
    uzanti = ''.join(choice(str(randint(0,11))) for i in range(6))
    return uzanti

def foto_sec():
    try:
        a = filedialog.askopenfile(initialdir = "/")
        dosya = open(a.name,"rb")
        veriler = dosya.read()
        if len(veriler)>5242880:
            messagebox.showerror('Fotoğraf Gönderim Hatası', '5 Mbdan büyük fotoğraf gönderemezsin ')
            int("a")            
            
        veri.send(veriler)
        dosya.close()
    except:pass

def tiklama_al(e):
    tiklama = ', '.join(str(code) for code in keyboard._pressed_events)
    if tiklama == "28":
        mesaj_gonder()
    if tiklama == "60":
        foto_sec()

def yetkilendirme_istegi():
    veri.send(bytes("/yetki_ver","utf-8"))

def mesaj_gonder():
    bilgilendir['text']="Mesaj Giriniz --->"
    mesaj = mesaj_gir.get()
    veri.send(bytes(mesaj,"utf-8"))
    mesaj_gir.delete(0,'end')
    
def mesaj_al():
    while True:
        mesaj = veri.recv(5242880)
        try:
            mesaj = mesaj.decode("utf-8")
            gelen_mesaj.insert('end',mesaj+"\n")
            
        except:
            dsy_adi = dosyaadi_uret()
            foto = open(f"C:/Users/{os.getlogin()}/Desktop/Online_Mesajlaşma_Uyg_Gelen_Fotolar/ENYENİ_FOTO_{dsy_adi}.png","wb")
            try:
                foto.write(mesaj)
                gelen_mesaj.insert('end',"Bir Fotoğraf Geldi Klasörü Kontrol Et"+"\n")
                
            except:pass
            
            foto.close()
            continue
x,y = 0, 0
art,arty = 3,4
def hareket():
    global x,y,art,arty,veri,bilgilendir,mesaj_gir,gelen_mesaj
    
    try:
        
        sunucu = requests.get("https://justpaste.it/mesajlasma").content
        kaynak = BeautifulSoup(sunucu,"html.parser")
    
        for i in kaynak.find_all("p"):
            sunucu = i.text.split(":")

        host = sunucu[0]
        port = sunucu[1]
        
        veri = socket(AF_INET,SOCK_STREAM)
        veri.connect((host,int(port)))
        
        gelen_mesaj = Text(pencere,height=10,width=50,fg="black",bg="White")
        gelen_mesaj.place(x=0,y=0)
        gelen_mesaj.config(state="normal")

        bilgilendir = Label(text="Adını Gir -->")
        bilgilendir.place(x=40,y=280)

        mesaj_gir = Entry()
        mesaj_gir.place(x=150,y=280)

        klasor = Button(text="Foto Klasörünü Aç",bg="Blue",fg="white")
        klasor.configure(command=klasor_ac)
        klasor.place(x=70,y=320)

        yetki = Button(text="Admin'e Yetki İsteği At",fg="white",bg="gray")
        yetki.configure(command = yetkilendirme_istegi)
        yetki.place(x=210,y=320)
        
        gonder = Button(text="Mesaj Gönder (Enter)",bg="Blue",fg="white")
        gonder.configure(command=mesaj_gonder)
        gonder.place(x=90,y=370)

        foto_gonder = Button(text="Foto Gönder (F2)",bg="gray",fg="white")
        foto_gonder.configure(command=foto_sec)
        foto_gonder.place(x=230,y=370)

        keyboard.hook(tiklama_al)
        threading.Thread(target=mesaj_al).start()

    except:
        x+=art
        y+=arty
        kontrol['text']="Sunucu İle Bağlantı Kurulamadı!"
        kontrol.place(x=x,y=y)

        if x>230 or y>350:
            art,arty = -3,-4
        if x<0 or y<0:
            art,arty = 3, 4
        pencere.after(10,hareket)
        
pencere = Tk()
pencere.resizable(width=False, height=False)
pencere.title("C4nUstun Sohbet Uygulaması Versiyon 0.4")
pencere.geometry("400x400")

kontrol = Label(height=3,fg="white",bg="gray",font="Arial")
kontrol.place(x=x,y=y)

hareket()

pencere.mainloop()
veri.close()
