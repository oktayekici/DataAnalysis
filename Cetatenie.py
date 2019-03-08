# This Python file uses the following encoding: utf-8
from lxml import etree
import smtplib
#cetatenie adresinden absolute xpath ile veriyi alıyoruz
parser = etree.HTMLParser()
tree = etree.parse("http://cetatenie.just.ro/index.php/ro/centru-de-presa-2/dosar-articol-11", parser)
tarih = tree.xpath('/html[1]/body[1]/section[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/p[12]/span[1]/text()')

#burada tarih kontrolu yapacak, 22.09.2019 iceriyorsa terminate edecek, yoksa incelemeye başlayacak. en son inceleme tarihi yazılmalı
if "22.02.2010" in str(tarih):
    print("değişiklik yok")
    exit
else:
    parser = etree.HTMLParser() # cetatenie adresinden absolute xpath ile veriyi alıyoruz
    tree = etree.parse("http://cetatenie.just.ro/index.php/ro/centru-de-presa-2/dosar-articol-11", parser)
    pidief = tree.xpath('//*[@id="middlecol"]/div/div[2]/p[10]/span[1]/a/@href')
    pidief = str(pidief)
    pidief = pidief.replace("[", "")
    pidief = pidief.replace("'", "")
    pidief = pidief.replace("]", "")
    pidief = 'http://cetatenie.just.ro'+pidief
    print(pidief)

 #pdf linkini alıp pdf'i indiriyor
from six.moves import urllib
urllib.request.urlretrieve(pidief, "2019.pdf")

#indirilen pdf'i alıp text'e çeviriyor, aramayı yapıyor ve sonucu veriyor
import PyPDF2
import re
def getText2PDF(pdfFileName):
    pdf_file=open(pdfFileName,'rb')
    read_pdf=PyPDF2.PdfFileReader(pdf_file)
    text=[]
    for i in range(0,read_pdf.getNumPages()):
        text.append(read_pdf.getPage(i).extractText())
    return ('\n'.join (text).replace("\n",''))

#pdf'in linkini aşağı girmek gerekiyor
metin = getText2PDF('2019.pdf')

dosyanumlist = []

#dosyanumaralarını text haline gelmiş pdf içinde arıyor, bulunca append ile listeye atıyor
def dosya(birinci, ikinci):
    m = re.search(birinci+"(.+?)"+ikinci, metin)
    if m:
        found = m.group(0)
        found = found.replace('2019', '2019   ') #tarihten sonra bitişik olmasın diye boşluk ekledim
        dosyanum = found[0:-5] #dosya numarası uzunluğuna göre -5 değiştirilmeli
        print(dosyanum)
        dosyanumlist.append(dosyanum)
dosya("12234","12237") #dosya numarası ve sonraki dosya numarası yazılmalı
dosya("25","26")

dosyanumlist = str(dosyanumlist)

#burası da mail gönderimi kısmı
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login('develoktay','!Oktay48?') #kullanici, sifre
msg = "\r\n".join([
  "From: develoktay@gmail.com",
  "To: oktayekici@me.com",
  "Subject: Cetatenie Romania",
  "",
  dosyanumlist
  ])
server.sendmail("develoktay@gmail.com", "oktayekici@me.com", msg)
server.quit()

