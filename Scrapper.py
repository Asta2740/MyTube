from pytube import YouTube


def youtube(url):

    yt_video = YouTube(url)
    image = yt_video.thumbnail_url
    name = yt_video.title
    videos = yt_video.streams.filter(only_audio=True)
    path = videos[-1].download('static/sound')

    return [image, path, name]
