from pytube import YouTube, Playlist
from pytube import Playlist


def youtube(url):
    yt_video = YouTube(url)
    image = yt_video.thumbnail_url
    name = yt_video.title
    videos = yt_video.streams.filter(only_audio=True)
    path = videos[-1].download('static/sound')

    return [image, path, name]


def Youtube_list(url):
    playlist = Playlist(url)
    Collection = []
    for video_url in playlist.video_urls:
        List = youtube(video_url)
        Collection.append(List)
    print(Collection)
    for x in Collection:
        print(x[0])
    return Collection
