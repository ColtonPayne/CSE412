#CSE 412 Final Project

import psycopg2
import PySimpleGUI as sg

import imageManager
import songManager
import podcastManager
import reccomendationEngine


sg.theme('SandyBeach')

DB_HOST = "localhost"
DB_NAME = "DemoDb"
DB_USER = "postgres"
DB_PASS =  #Redacted


conn = psycopg2.connect(dbname = DB_NAME, user= DB_USER, password = DB_PASS, host = DB_HOST)

cur = conn.cursor()

coverPictureUrl = "https://i0.wp.com/liveforlivemusic.com/wp-content/uploads/2016/02/musicbrain.jpg?fit=610%2C439&ssl=1"
imageBox = imageManager.ImageManager.create_image(coverPictureUrl, False)

layout = [[sg.Text("CSE 412 Project: Music Reccomendation Engine")],
        [imageBox],[sg.Button("Find Songs", key = "Songs"), sg.Button("Find Podcasts", key = "Podcasts"), sg.Button("Get Reccomendations", key = "Reccomendations" )]]   

window = sg.Window('', layout,
                    ttk_theme='clam',
                    resizable=True)



while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if event == "Songs":
        songManager.SongManager.open_song_table(cur, conn)
    if event == "Podcasts":
        podcastManager.PodcastManager.open_podcast_table(cur, conn)
    if event == "Reccomendations":
        reccomendationEngine.ReccomendationEngine.open_reccomendation_window(cur, conn)
        



cur.close()

conn.close()



