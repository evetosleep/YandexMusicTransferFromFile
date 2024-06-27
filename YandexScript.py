import os
from mutagen.id3 import ID3
from yandex_music import Client

# токены и id ищите сами. В инете куча инфы.
token = ""
client = Client(token).init()
user = 

# Очищаем файл для логов ошибок
with open("C:\\Users\\Radius\\Desktop\\notadded.txt", "w") as my_file:
    my_file.write("")

existing = client.users_playlists_list(user)
for i in range(len(existing)):
    r = existing[i].kind
    client.users_playlists_delete(r, user)
    print("плейлист удален")

folder = "C:\\Users\\Radius\\Desktop\\song\\nodigits"
for root, dirs, files in os.walk(folder):
    for dir in dirs:
        path = os.path.join(root, dir)
        folder = os.path.dirname(path)
        playlist_name = os.path.basename(folder)
        client.users_playlists_create(dir, 'public', user)
        print("плейлист добавлен " + dir)

d = client.users_playlists_list(user)

songs = "C:\\Users\\Radius\\Desktop\\song\\nodigits"
for root, dirs, files in os.walk(songs):
    for file in files:
        path = os.path.join(root, file)
        folder = os.path.dirname(path)
        playlist_name = os.path.basename(folder)
        
        #читает ID3 из файла
        try:
            r = ID3(path)
            query = f"{r['TPE1'].text[0]} {r['TIT2'].text[0]} {r['TALB'].text[0]}"
        except Exception as e:
            print(f"Ошибка чтения ID3 из {file}: {e}")
            continue
            
            #Поиск в ЯМ
        search_result = client.search(query)
        if search_result.tracks:
            track_id = search_result.tracks.results[0].id
            album_id = search_result.tracks.results[0].albums[0].id

            for i in range(len(d)):
                if d[i].title == playlist_name:
                    try:
                        playlist = client.users_playlists(d[i].kind)
                        rev = playlist.revision
                        
                        client.users_playlists_insert_track(d[i].kind, track_id, album_id, at=0, revision=rev)
                        print(f"Песня {query} добавлена в плейлист {playlist_name}")
                        
                        d = client.users_playlists_list(user)
                        
                    except Exception as e:
                        print(f"Ошибка добавления {query} в плейлист {playlist_name} при первой попытки: {e}")
                        try:
                            playlist = client.users_playlists(d[i].kind)
                            rev = playlist.revision
                            
                            client.users_playlists_insert_track(d[i].kind, track_id, album_id, at=0, revision=rev)
                            print(f"Песня {query} добавления в плейлист {playlist_name} при второй попытке")
                            
                            d = client.users_playlists_list(user)
                            
                        except Exception as e2:
                            print(f"Ошибка добавления {query} в плейлист {playlist_name} при второй попытке: {e2}")
                            with open("C:\\Users\\Radius\\Desktop\\notadded.txt", 'a') as f:
                                f.write(f"{query} in {playlist_name}\n")
        else:
            with open("C:\\Users\\Radius\\Desktop\\notadded.txt", 'a') as f:
                f.write(f"{query} in {playlist_name}\n")
            print("Песня не добавлена " + query + " in " + playlist_name)