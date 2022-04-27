import spotifyAPI 
import imageManager
import reccomendationEngine


import PySimpleGUI as sg
import webbrowser

class SongManager:


    def __init__(self) -> None:
        pass

    global songDict
    global songTable
    global songHeaders

    songDict = { }

    songHeaders = ["ID", "Name", "Artist", "Genre"]


    songTable =  [[]]

    # add table to data


    def open_song_like_window(a_id, a_name, cur, conn):

        
        #Get the url of the song's spotify link and album cover
        songUrl = spotifyAPI.spotify.get_Song(a_name)
        imageUrl = spotifyAPI.spotify.get_image(a_name)

        img_box = imageManager.ImageManager.create_image(imageUrl, False)
        
        layout = [
        [img_box], 
        [sg.Button("Play Song", key="Url")],
        [sg.Button('Like'), sg.Button('Dislike')]]

        window = sg.Window(str(a_id), layout, modal=True)
        choice = None
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "Url":
                webbrowser.open(songUrl)
            if event == "Like":
                reccomendationEngine.ReccomendationEngine.update_likes(cur, conn, a_id, False)
            if event == "Dislike":
                reccomendationEngine.ReccomendationEngine.update_dislikes(cur, conn, a_id, True) 
                
            
        window.close()

   
    def open_song_table(cur, conn):

        #   Create table of songs
        cur.execute('SELECT a_id from "Song" ORDER BY a_id')

        counter = 0
        for a in cur:

            song = []
            songTable.append(song)


            songTable[counter].append(a)

            # Create a mapping of the row number and song ID: Allows us to know which song the user selected when interacting with table element
            # Counter will serve as the row number in our table, from which we can find the audio ID
            songDict[counter] = a[0]

            counter = counter + 1


        cur.execute('SELECT a_name from "Song" ORDER BY a_id')
        counter = 0
        for a in cur:
            songTable[counter].append(a)

            #b = 'SELECT cr.c_name FROM "Creator" cr, "CreatedBy" cb, "Song" s WHERE cb.c_id = cr.c_id AND s.a_id= cb.a_id AND s.a_id='
            #b = b + str(counter)
            #cur1.execute(b)
            #for b in cur1:
            #   songTable[counter].append(b)

            counter = counter + 1


        
        cur.execute('SELECT cr.c_name FROM "Creator" cr, "CreatedBy" cb, "Song" s WHERE cb.c_id = cr.c_id AND s.a_id= cb.a_id ORDER BY s.a_id')
        counter = 0
        for a in cur:
            songTable[counter].append(a)
            counter = counter + 1
        

        
        cur.execute('SELECT s_genre from "Song" ORDER BY a_id')
        counter = 0
        for a in cur:
            songTable[counter].append(a)
            counter = counter + 1


        data = songTable
        headings = songHeaders



        # ------ Window Layout ------
        layout = [
                #[sg.Text("Filter By Genre"), sg.Text("                                Filter by Artist")],
                #[sg.Listbox(values = genres, size = (25,6)),
                #sg.Listbox(values = artists, size = (25,6))],
                [sg.Table(values=data[0:][:], headings=headings, max_col_width=25,
                            auto_size_columns=True,
                            display_row_numbers=False,
                            justification='right',
                            num_rows=len(songTable)/2,
                            alternating_row_color='lightyellow',
                            key='-TABLE-',
                            selected_row_colors='red on yellow',
                            enable_events=True,
                            expand_x=True,
                            expand_y=True,
                            enable_click_events=True)],
                #[sg.Button('Read'), sg.Button('Double'), sg.Button('Change Colors')],
                [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')],
                ]

        # ------ Create Window ------
        window = sg.Window('Song List', layout,
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
            

                    update_string = 'SELECT a_name FROM "Song" WHERE a_id='
                    update_string = update_string + str(audio_id)
                    cur.execute(update_string)
                    name_tuple = cur.fetchone()
                    audio_name = name_tuple[0]
    


                    SongManager.open_song_like_window(audio_id, audio_name, cur, conn)
        window.close()
