import googleapiclient.discovery

youtube_api = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyC8JDdtacU4cFRLkKa2g-6S6DAaIxdxHKY")


def get_youtube_comments(video_id: str) -> dict[str, tuple[str, int]]:
    """
    @param video_id: ID of the YouTube video to retrieve comments from.
    @return: Dictionary of comment ID to a 2-tuple of the original text of the comment and its like count.
    """
    comments: dict[str, tuple[str, int]] = {}

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
                                        "likeCount": int(like_count)
                                    }
                                }
                            }
                        }:
                            comments[comment_id] = (comment_text, like_count)

        if "nextPageToken" not in response:
            break
        next_page_token = response["nextPageToken"]

    return comments
