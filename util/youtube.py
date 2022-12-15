import googleapiclient.discovery
import pandas

from credentials import GOOGLE_API_KEY
from util.util import CommentData

youtube_api = googleapiclient.discovery.build("youtube", "v3", developerKey=GOOGLE_API_KEY)


def get_youtube_comments(video_id: str) -> dict:
    """
    @param video_id: ID of the YouTube video to retrieve comments from.
    @return: Dictionary of comment ID to a 2-tuple of the original text of the comment and its like count.
    """
    comments: dict = {}

    next_page_token = None
    while True:
        request = youtube_api.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat="plainText"
        )
        response = request.execute()

        if "items" in response:
            for item in response["items"]:
                comment_id: str = str(item["id"])
                comment_text: str = str(item["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
                like_count: int = int(item["snippet"]["topLevelComment"]["snippet"]["likeCount"])
                timestamp: str = str(item["snippet"]["topLevelComment"]["snippet"]["publishedAt"])

                comments[comment_id] = CommentData(
                    text=comment_text,
                    likes=like_count,
                    timestamp=pandas.to_datetime(timestamp)
                )

        if "nextPageToken" not in response:
            break
        next_page_token = response["nextPageToken"]

    return comments


def get_channel_id(username: str):
    request = youtube_api.channels().list(
        part="contentDetails",
        forUsername=username
    )
    response = request.execute()

    if "items" in response:
        return str(response["items"]["id"])

    return None


def get_videos(channel_id: str):
    upload_playlist = "UU" + channel_id[2:]
    print(upload_playlist)

    request = youtube_api.playlists().list(
        part="snippet",
        id=upload_playlist
    )
    response = request.execute()

    print(response)
