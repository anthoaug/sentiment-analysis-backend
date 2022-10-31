import datetime

import googleapiclient.discovery

from dataclasses import dataclass
from datetime import datetime

youtube_api = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyC8JDdtacU4cFRLkKa2g-6S6DAaIxdxHKY")


@dataclass
class CommentData:
    text: str
    likes: int
    timestamp: datetime


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
                                timestamp=datetime.fromisoformat(timestamp[:-1])
                            )

        if "nextPageToken" not in response:
            break
        next_page_token = response["nextPageToken"]

    return comments
