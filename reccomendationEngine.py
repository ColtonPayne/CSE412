# Colton Payne

import webbrowser
import PySimpleGUI as sg
import imageManager
import spotifyAPI 


class ReccomendationEngine:

    global imgArray 
    imgArray = []
    global nameList
    nameList = []
    global typeList
    typeList = []
    global urlList
    urlList = []

    def __init__(self) -> None:
            pass

    def update_likes(cur, conn, a_id, isPodcast):

        # Set the like score to 1000 if a song is liked- prevents the system from reccomending a song the user has already liked
        update_string = 'UPDATE "Audio" SET "a_likeDislike" = -10000 WHERE a_id='
        update_string = update_string + str(a_id)

        cur.execute(update_string)
        conn.commit()

        # Add 30 points to the like score if a song or podcast of the same genre is liked
        if(isPodcast):
            update_string = 'Update "Podcast" SET "a_likeDislike" = "a_likeDislike" + 30 WHERE p_genre = (SELECT p_genre FROM "Podcast" where a_id = '
            update_string = update_string + str(a_id)
            update_string = update_string + ')'
        else:
            update_string = 'Update "Song" SET "a_likeDislike" = "a_likeDislike" + 30 WHERE s_genre = (SELECT s_genre FROM "Song" where a_id = '
            update_string = update_string + str(a_id)
            update_string = update_string + ')'

        cur.execute(update_string)
        conn.commit()

        # Add 60 points to the like score if a song or podcast by the same creator is liked

        # Fetch a list of a_id's by the artist who has made this piece of auido
        update_string = 'SELECT s.a_id FROM "Audio" s, "CreatedBy" cb, "Creator" cr WHERE s.a_id= cb.a_id AND cb.c_id = cr.c_id AND c_name = (SELECT cr.c_name FROM "Creator" cr, "Audio" au,  "CreatedBy" cB WHERE cr.c_id = cb.c_id AND cb.a_id = au.a_id AND AU.A_ID = '
        update_string = update_string + str(a_id)
        update_string = update_string + ')'

        cur.execute(update_string)
        audioList = cur.fetchall()
   
        # Add 60 like points to the matching a_id's
        for a in audioList:
           
            new_update_string = 'Update "Audio" SET "a_likeDislike" = "a_likeDislike" + 60 WHERE a_id = '
            new_update_string = new_update_string + str(a[0])
            cur.execute(new_update_string)
            conn.commit()   

    def update_dislikes(cur, conn, a_id, isPodcast):
    # Set the like score to 1000 if a song is liked- prevents the system from reccomending a song the user has already liked
        update_string = 'UPDATE "Audio" SET "a_likeDislike" = -10000 WHERE a_id='
        update_string = update_string + str(a_id)

        cur.execute(update_string)
        conn.commit()

        # Add 30 points to the like score if a song or podcast of the same genre is liked
        if(isPodcast):
            update_string = 'Update "Podcast" SET "a_likeDislike" = "a_likeDislike" - 30 WHERE p_genre = (SELECT p_genre FROM "Podcast" where a_id = '
            update_string = update_string + str(a_id)
            update_string = update_string + ')'
        else:
            update_string = 'Update "Song" SET "a_likeDislike" = "a_likeDislike" - 30 WHERE s_genre = (SELECT p_genre FROM "Podcast" where a_id = '
            update_string = update_string + str(a_id)
            update_string = update_string + ')'

        cur.execute(update_string)
        conn.commit()

        # Add 60 points to the like score if a song or podcast by the same creator is liked

        # Fetch a list of a_id's by the artist who has made this piece of auido
        update_string = 'SELECT s.a_id FROM "Audio" s, "CreatedBy" cb, "Creator" cr WHERE s.a_id= cb.a_id AND cb.c_id = cr.c_id AND c_name = (SELECT cr.c_name FROM "Creator" cr, "Audio" au,  "CreatedBy" cB WHERE cr.c_id = cb.c_id AND cb.a_id = au.a_id AND AU.A_ID = '
        update_string = update_string + str(a_id)
        update_string = update_string + ')'

        cur.execute(update_string)
        audioList = cur.fetchall()
   
        # Add 60 like points to the matching a_id's
        for a in audioList:
            new_update_string = 'Update "Audio" SET "a_likeDislike" = "a_likeDislike" - 60 WHERE a_id = '
            new_update_string = new_update_string + str(a[0])
            cur.execute(new_update_string)
            conn.commit()   
        print("Disliked")

    def open_reccomendation_window(cur, conn):
   
            #   Create five images

            

            cur.execute('SELECT a_name from "Audio" ORDER BY "a_likeDislike" desc limit 6')
            for a in cur:
                nameList.append(a[0])

            cur.execute('SELECT a_rating from "Audio" ORDER BY "a_likeDislike" desc limit 6')
            for a in cur:
                typeList.append(a[0])

            counter = 0            
            for a in typeList:
                # Audio is a song
                if(typeList[a] == 1):
                    # create image from song name
                    imgUrl = spotifyAPI.spotify.get_image(nameList[counter])
                    imageBox = imageManager.ImageManager.create_image(imgUrl, False)
                    imgArray.append(imageBox)

                    

                    # get link to song
                    songUrl = spotifyAPI.spotify.get_Song(nameList[counter])
                    urlList.append(songUrl)
                    
                else:
                    # create image from podcast name
                    imgUrl = spotifyAPI.spotify.get_podcastImage(nameList[counter])
                    imageBox = imageManager.ImageManager.create_image(imgUrl, False)
                    imgArray.append(imageBox)

                    # get link to podcast
                    podcastUrl = spotifyAPI.spotify.get_podcastURL(nameList[counter])
                    urlList.append(podcastUrl)
                counter = counter + 1

                print(nameList)
        

            # ------ Window Layout ------
            layout = [
                        [imgArray[0], imgArray[1]],
                        [imgArray[2], imgArray[3]],
                        [imgArray[4], imgArray[5]]
                    ]

            

            # ------ Create Window ------
            window = sg.Window('Reccomendations', layout,
                            ttk_theme='clam',
                            resizable=True)


            # ------ Event Loop ------
            while True:
                event, values = window.read()
                print(event, values)
                if event == sg.WIN_CLOSED:
                    break
                if event == 0:
                    webbrowser.open(urlList[0])
                if event == 1:
                    webbrowser.open(urlList[1])
                if event == 2:
                    webbrowser.open(urlList[2])
                if event == 3:
                    webbrowser.open(urlList[3])
                if event == 4:
                    webbrowser.open(urlList[4])
                if event == 5:
                    webbrowser.open(urlList[5])
  






    