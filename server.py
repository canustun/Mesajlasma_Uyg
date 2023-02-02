from socket import socket,AF_INET,SOCK_STREAM
import threading,time
from datetime import datetime
from tkinter import *
import time
# Sunucumuzu açalım :D
#Yaşasın açık kaynaklı kod :))
###############################
#     Mesajlaşma Serveri      #
#      Tt : @canustun__       #
#      İg : @canustun.py      #
#      Tg : @canustunn        #
###############################

host = "localhost"
port = 80
veri = socket(AF_INET,SOCK_STREAM)

veri.bind((host,port))
veri.listen(25)

gonderme_onayi = False

banli_ipler = []

kullanicilar,normal_ipler = [],[]
kullanici_adlari = []
yetkililer = []

"""
def aktif_kullanici_adlar():
    global kullanicilar,kullanici_adlari
    while True:
        adlar = ""
        for i in kullanici_adlari:
            adlar += i+"\n"
        for a in kullanicilar:
            try:
                a.send(bytes(f"Qaktif-kul_ism?{adlar}","utf8"))
            except:pass
        time.sleep(1.7)

def aktif_kullanici():
    global kullanicilar
    while True:
        for i in kullanicilar:
            try:
                i.send(bytes(f"ASAkullanici_adet: {len(kullanicilar)}","utf8"))
            except:
                pass
        time.sleep(1.7)
"""      
def veri_al(kullanici_bilgisi,kullanici_ad):
    global kullanicilar,kullanici_adlari#,yetkililer
    
    while True:
        zaman = datetime.now()
        saat = str(zaman.hour)
        dk = str(zaman.minute)
        saat_dk = saat+":"+dk+" "    

        try:
            mesaj = kullanici_bilgisi.recv(5242880)
            
            try:
                mesaj = mesaj.decode("utf-8")
                if mesaj=="" or mesaj == " " or mesaj == len(mesaj)*" ":
                    continue

            except:
                for i in kullanicilar:
                    if i!=kullanici_bilgisi:
                        i.send(mesaj)
                    else:
                        i.send(bytes("Fotoğraf gönderildi","utf8"))
                continue
                
            if len(mesaj)>200:
                kullanici_bilgisi.send(bytes("200 Karakter Sınırı Aşıldı !","utf8"))
                continue
            
            elif mesaj != len(mesaj)*" " and mesaj != "":
                for i in kullanicilar:
                    if i!=kullanici_bilgisi:
                        i.send(bytes(saat_dk+kullanici_ad+" : "+mesaj,"utf8"))
                    else:
                        i.send(bytes(saat_dk+"Siz : "+mesaj,"utf8"))
                        
            elif mesaj == "/yetki_ver" or mesaj == "yetki_ver" or mesaj == "yetki ver":
                for i in kullanicilar:
                    i.send(bytes("I CAN(server botu) : Yetki sistemi bir süreliğine kapatılmıştır.","utf8"))

                """yetki_ver['text'] = f"{kullanici_ad} adlı kullanıcı yetki istiyor."
                threading.Thread(target = yetkilendirme, args=(kullanici_ad,)).start()

            elif len(mesaj) > 4 and mesaj[:4] == "/ban":
                for i in yetkililer:
                    if kullanici_ad == i and not mesaj[5:] in yetkililer:
                        ban_atma(mesaj[5:],kullanici_ad)"""
        except:
            try:
                kullanicilar.remove(kullanici_bilgisi)
                kullanici_adlari.remove(kullanici_ad)
            except:pass
            
            break


"""def yetkilendirme(kullanici_adi):
    global yetkililer,gonderme_onayi
    
    if gonderme_onayi:
            yetki = yetki_onayla.get()
            if yetki == "E" or yetki == "e":
                for i in kullanicilar:
                    i.send(bytes(kullanici_adi+" 'I CAN' Tarafından Yetkilendirildi.","utf8"))
                yetkililer.append(kullanici_adi)
                
            else:
                for i in kullanicilar:
                    i.send(bytes(kullanici_adi+" Kullanıcının Yetki İsteği Reddedildi!","utf8"))
                
            gonderme_onayi = False
            yetki_ver['text'] = "Şuanlık yetki isteği yok !"
            yetki_onayla.delete(0,'end')"""


def isim_alma(kullanici_bilgisi2,ip):
    global kullanicilar,kullanici_adlari
    try:
        while True:
            ad = kullanici_bilgisi2.recv(1024).decode("utf8")
            if len(ad)>1 and ad != "I C4N" and ad != "I CAN" and ad != "l C4N" and len(ad)<17 and ad!="" and ad!=" " and ad != len(ad)*" " and not ad in kullanici_adlari:
                for i in kullanicilar:
                    i.send(bytes(f"{ad} Adlı Kullanıcı Sohbete Katıldı !","utf8"))

                kullanici_adlari.append(ad)
                kullanicilar.append(kullanici_bilgisi2)
                kullanici_bilgisi2.send(bytes(f"Sohbete Katıldın !","utf8"))

                print(f"{ad} : {ip}  Toplam:{len(kullanicilar)} ")
                threading.Thread(target=veri_al, args=(kullanici_bilgisi2,ad)).start()
                break
            else:
                kullanici_bilgisi2.send(bytes("İsmini tekrar gir !","utf8"))

    except:pass
    
def ban_atma(banlanacak,banlayan):
    global kullanicilar,kullanici_adlari,banli_ipler,normal_ipler
    try:
        indexi = kullanici_adlari.index(banlanacak)
        kullanici_adlari.remove(banlanacak)
        banli_ipler.append(normal_ipler[indexi])
        normal_ipler.remove(normal_ipler[indexi])
        kullanicilar[indexi].send(bytes(f"{banlayan} Tarafından Banlandın!","utf8"))
        kullanicilar[indexi].close()
        kullanicilar.remove(kullanicilar[indexi])
        for i in kullanicilar:
            i.send(bytes(f"{banlanacak} Adlı Kullanıcı {banlayan} Tarafından Banlandı!","utf8"))
    except:pass

def ban_atma_ceo():
    banlanacak = banla.get()
    banla.delete(0,'end')
    
    ban_atma(banlanacak,"I CAN")

"""def gonder_cevap():
    global gonderme_onayi
    gonderme_onayi = True"""
    
def onayla():
    global banli_ipler,normal_ipler
    
    while True:
        kullanici,adres = veri.accept()
        try:
            ip = kullanici.recv(1024).decode("utf8")
        except:
            continue
        if ip in banli_ipler:
            kullanici.send(bytes("Banlı kullanıcılar giriş yapamaz!","utf8"))
            continue
        normal_ipler.append(ip)
        
        threading.Thread(target=isim_alma,args=(kullanici,ip)).start()
        
pencere = Tk()
pencere.geometry("150x150")

banla = Entry()
banla.place(x=10,y=50)

banla_butonu = Button(text="Banla",bg="red")
banla_butonu.config(command = ban_atma_ceo)
banla_butonu.place(x=10,y=70)

"""
yetki_ver = Label(text="Şuanlık yetki isteği yok !")
yetki_ver.place(x=10,y=100)

yetki_onayla = Entry()
yetki_onayla.place(x=10,y=120)

yetki_onayla_butonu = Button(text="Cevabı Gönder",bg="green")
yetki_onayla_butonu.configure(command = gonder_cevap)
yetki_onayla_butonu.place(x=10,y=150)
"""
threading.Thread(target=onayla).start()
pencere.mainloop()
# orda minik bir hata vardı D
# serveri açalım :D
