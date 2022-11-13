import googleapiclient.discovery
import pandas

from credentials import GOOGLE_API_KEY
from util.util import CommentData

youtube_api = googleapiclient.discovery.build("youtube", "v3", developerKey=GOOGLE_API_KEY)


def get_youtube_comments(video_id: str) -> dict[str, CommentData]:
    """
    @param video_id: ID of the YouTube video to retrieve comments from.
    @return: Dictionary of comment ID to a 2-tuple of the original text of the comment and its like count.
    """
    comments: dict[str, CommentData] = {}

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

        match response:
            case {
                "items": list(items)
            }:
                for item in items:
                    match item:
                        case {
                            "id": str(comment_id),
                            "snippet": {
                                "topLevelComment": {
                                    "snippet": {
                                        "textOriginal": str(comment_text),
                                        "likeCount": int(like_count),
                                        "publishedAt": str(timestamp)
                                    }
                                }
                            }
                        }:
                            comments[comment_id] = CommentData(
                                text=comment_text,
                                likes=like_count,
                                timestamp=pandas.to_datetime(timestamp)
                            )

        if "nextPageToken" not in response:
            break
        next_page_token = response["nextPageToken"]

    return comments
