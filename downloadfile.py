# Muhammad Momin
# Jason Paul
import time
import youtube_dl
import sqlite3
from datetime import date
import copy
import os
import sys
import webbrowser
from youtube_dl.utils import args_to_str


connection = sqlite3.connect("DownloadHistory.db")
c = connection.cursor()
def create_table_db():
    # command to check if there is already a table named 'history'
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='history' ''')
    if c.fetchone()[0]==1 :
        # Table already exists
        return None
    else:
        c.execute('''CREATE TABLE history (
            name TEXT NOT NULL,
            format VARCHAR(5) NOT NULL,
            file_location TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        connection.commit()
def insert_record(title,format,file_location):
    c.execute("INSERT INTO history (name, format,file_location) VALUES (?,?,?)",(title,format,file_location,))
    connection.commit()

def show_history():
    create_table_db()
    print("*"*10 + " History " + "*"*10)
    for row in c.execute("SELECT * FROM history"):
       print(row)

def open_in_webbrowser(path,format):
    f = open('downloadedFile.html','w')
    message = """<html>
    <head>
    <title>Lets Download It</title>
    </head>
    <body>
    <h2>Click play button to play """+format+"""</h2>
    <"""+format+""" controls style="width:100%">
        <source  src="""+path+""">
    </"""+format+""">
    </body>
    </html>"""
    f.write(message)
    f.close()
    filename = 'file:///'+os.getcwd()+'/' + 'downloadedFile.html'
    webbrowser.open_new_tab(filename)

def download_video(link):
   ydl_opts = {
       'format': 'mp4',
       'outtmpl': "./downloads/%(title)s.%(ext)s",
   }
   _id = link.strip()
   meta = youtube_dl.YoutubeDL(ydl_opts).extract_info(_id)
   save_location = meta['title'] + ".mp4"
   title = meta['title']
   format = 'video'
   path = os.path.join(os.path.abspath(os.getcwd()),'downloads',save_location)
   path = path.replace(' ','%20')
   path = path.replace('|','_')

   print('Saving it to History database... ')
   create_table_db()
   insert_record(title=title,format=format,file_location=path)

   print(f'Title: {title}     Location: {path}      Format: {format}')
   
   open_in_webbrowser(path=path, format=format)
   return save_location

def download_audio(link):
   ydl_opts = {
       'format': 'bestaudio/best',
       'postprocessors': [{
           'key': 'FFmpegExtractAudio',
           'preferredcodec': 'mp3',
           'preferredquality': '192',
       }],
       'ffmpeg-location': str(os.path.join(os.path.abspath(os.getcwd()),'')),
       'outtmpl': str(os.path.join(os.path.abspath(os.getcwd()),"downloads","%(title)s.%(ext)s")),
    #    'outtmpl': "./downloads/%(title)s.%(ext)s",
   }
   _id = link.strip()
   meta = youtube_dl.YoutubeDL(ydl_opts).extract_info(_id)
   save_location = meta['title'] + ".mp3"
   title = meta['title']
   format = 'audio'
   path = os.path.join(os.path.abspath(os.getcwd()),'downloads',save_location)
   path = path.replace(' ','%20')
   path = path.replace('|','_')
   print('Saving it to History database... ')
   create_table_db()
   insert_record(title=title,format=format,file_location=path)

   print(f'Title: {title}     Location: {path}      Format: {format}')
   open_in_webbrowser(path=path, format=format)
   return save_location

def __main__(url,choice):
    nurl = copy.deepcopy(url) 
    nurl = nurl.replace(' ','')
    if choice == 'v':
        download_video(nurl)
    if choice == 'a':
        download_audio(nurl)
    if choice == 'h':
        show_history()

__main__(sys.argv[1],sys.argv[2])