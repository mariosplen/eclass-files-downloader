from re import findall
import requests
import sys
if  len(sys.argv)<3:
    sys.exit("To use tool execute execute like: py"+sys.argv[0]+" username password")
payload={'next': '/main/my_courses.php','uname': sys.argv[1],'pass': sys.argv[2],'submit': 'Είσοδος'}
url = "https://eclass.duth.gr/"
def download(num):
    from datetime import date
    from os import path
    from os import remove
    from os import makedirs
    from shutil import move
    from random import randint
    from filecmp import cmp
    today = date.today()
    date = today.strftime("%d-%m-%Y")
    global Names,payload,url
    download_link="https://eclass.duth.gr/modules/document/index.php?course="+num+"&download=/"
    for i in range(len(Nums)):
        if num == Nums[i]:
            loc=i
    dir=path.join(path.expandvars("%userprofile%"),"Documents\\eclass\\"+Names[loc])
    if not path.exists(dir):
        makedirs(dir)
    if not path.exists(dir+"\\"+date+"\\"):
        makedirs(dir+"\\"+date+"\\")
    with requests.Session() as d:
        d.get(url)
        d.post(url, data=payload)
        data = d.get(download_link)
    if path.exists(dir+"\\saved.txt"):
        saved = open(dir+"\\saved.txt","r",encoding='utf8')
        notInside=True
        temp = open(dir+'\\'+num+'.zip',"wb")
        temp.write(data.content)
        temp.close()
        size=path.getsize(dir+'\\'+num+'.zip')
        for line in saved:
            keysize=path.getsize(line.rstrip('\n'))
            if size==keysize:
                notInside=False
        saved.close()
        if notInside:
            rand=str(randint(100, 999))
            move(dir+'\\'+num+'.zip',dir+"\\"+date+"\\"+num+rand+".zip")
            saved2 = open(dir+"\\saved.txt","a", encoding='utf8')
            saved2.write(dir+"\\"+date+"\\"+num+rand+".zip\n")
            saved2.close()
        else:
            remove(dir+'\\'+num+'.zip')
    else:
        final = open(dir+"\\"+date+"\\"+num+".zip","wb")
        final.write(data.content)
        final.close()
        saved = open(dir+"\\saved.txt","a", encoding='utf8')
        saved.write(dir+"\\"+date+"\\"+num+".zip\n")
        saved.close()
with requests.Session() as s:
    s.get(url)
    r = s.post(url, data=payload)
temptxt = (r.text)
Names=findall("'>(.*?)</a></strong>",temptxt)
Links=findall("<strong><a href='(.*?)'>",temptxt)
Nums=[]
for text in Links:
    num="".join(findall("courses/(.*)",text))
    Nums.append(num)

for i in range(len(Nums)):
    print("downloading "+Names[i]+"...")
    download(Nums[i])
    print(Names[i]," Done ",i+1," out of ",len(Nums))
print("Finished !")
