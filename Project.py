#CSE 412 

import psycopg2
import PySimpleGUI as sg

import random
import string
import operator

from PIL import Image
import requests
from io import BytesIO

sg.theme('SandyBeach')

DB_HOST = "localhost"
DB_NAME = "DemoDb"
DB_USER = "postgres"
DB_PASS = "13Mike?LimaKilo"


conn = psycopg2.connect(dbname = DB_NAME, user= DB_USER, password = DB_PASS, host = DB_HOST)

cur = conn.cursor()


#Create a set of genres for filtering
genres = set()

#Create a set of artists for filtering
artists = set()

songHeaders = ["ID", "Name", "Genre", "Url" ]
songTable = [[]]

songDict = { }



# add table to data
data = songTable

headings = songHeaders

# Code to convert a URL to image data was taken form this help tread: https://github.com/PySimpleGUI/PySimpleGUI/issues/2941
def image_to_data(im):
    """
    Image object to bytes object.
    : Parameters
      im - Image object
    : Return
      bytes object.
    """
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

def open_window(a_id):

    url = "https://picsum.photos/200/300"
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    img = Image.open(response.raw)
    data = image_to_data(img)
    img_box = sg.Image(data=data)  

    layout = [[sg.Text("New Window", key="new")],
    [img_box], [sg.Button('Like')], [sg.Button('Dislike')]]
    window = sg.Window(str(audio_id), layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Like":
            # If a user likes a so
            update_string = 'UPDATE "Song" SET "a_likeDislike" = 100 WHERE a_id='
            update_string = update_string + str(a_id)
        
            cur.execute(update_string)
            conn.commit()
            print(update_string)
            print("Liked")
        
    window.close()





# Create an array of unique genres
cur.execute('SELECT s_genre from "Song"')
for name in cur:
        genres.add(name)


# Create an array of unique artists
cur.execute('SELECT c_name from "Creator"')
for name in cur:
        artists.add(name)

# Create table of songs
cur.execute('SELECT a_id from "Song"')

counter = 0
for a in cur:

    song = []
    songTable.append(song)


    songTable[counter].append(a)

    # Create a mapping of the row number and song ID: Allows us to know which song the user selected when interacting with table element
    # Counter will serve as the row number in our table, from which we can find the audio ID
    songDict[counter] = a[0]

    counter = counter + 1

  

cur.execute('SELECT a_name from "Song"')
counter = 0
for a in cur:
    songTable[counter].append(a)
    counter = counter + 1

cur.execute('SELECT s_genre from "Song"')
counter = 0
for a in cur:
    songTable[counter].append(a)
    counter = counter + 1


cur.execute('SELECT s_url from "Song"')
counter = 0
for a in cur:
    songTable[counter].append(a)
    counter = counter + 1




#, [sg.Listbox(values = genres, size = (30,6))], 




# ------ Window Layout ------
layout = [
        [sg.Listbox(values = genres, size = (30,6))],
        [sg.Listbox(values = artists, size = (30,6))],
        [sg.Table(values=data[0:][:], headings=headings, max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification='right',
                    num_rows=len(songTable),
                    alternating_row_color='lightyellow',
                    key='-TABLE-',
                    selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='This is a table')],
          #[sg.Button('Read'), sg.Button('Double'), sg.Button('Change Colors')],
          [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')],
           #[sg.Text('Read = read which rows are selected')],
          #[sg.Text('Double = double the amount of data in the table')],
          #[sg.Text('Change Colors = Changes the colors of rows 8 and 9'), sg.Sizegrip()]
          ]

# ------ Create Window ------
window = sg.Window('The Table Element', layout,
                   ttk_theme='clam',
                   resizable=True)


# ------ Event Loop ------
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if isinstance(event, tuple):
        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
        if event[0] == '-TABLE-':
            row_num_clicked = event[2][0]
            window['-CLICKED-'].update(f'{event[2][0]},{event[2][1]}')
            audio_id = songDict.get(event[2][0])
            open_window(audio_id);
window.close()




cur.close()

conn.close()



