import csv

import googleapiclient.discovery

# Your API Key. See readme for more info.
DEVELOPER_KEY = "YOUR_API_KEY"

# Video ID of youtube video you want to scrape
VIDEO_ID = "YOUR_ID_HERE"

api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


def top_level_info(comment: dict):
    """
    For a given comment, return dictionary of author name, comment text,
    like and reply count.
    """

    author_name = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
    comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
    like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']
    reply_count = comment['snippet']['totalReplyCount']

    return {'Author': author_name, 'Comment Text': comment_text,
            'Likes': like_count, 'Replies': reply_count}


def child_info(reply: dict):
    """
    For a given reply, return dictionary of author name, reply
    text and reply count.
    """

    reply_author = reply['snippet']['authorDisplayName']
    reply_text = reply['snippet']['textOriginal']
    reply_likes = reply['snippet']['likeCount']

    return {'Reply Author': reply_author, 'Reply Text': reply_text,
            'Reply Likes': reply_likes}


def main():
    """
    For a given youtube video, output all its comments and replies to csv file.
    """

    with open('meme.csv', mode='w') as f:
        column_names = ['Author', 'Comment Text', 'Likes', 'Replies', 'Reply Author', 'Reply Text', 'Reply Likes']
        writer = csv.DictWriter(f, fieldnames=column_names)
        writer.writeheader()

        next_page_token = ''
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=VIDEO_ID,
                pageToken=next_page_token)

            response = request.execute()
            next_page_token = response.get('nextPageToken', None)

            all_comments = response['items']
            for comment in all_comments:
                writer.writerow(top_level_info(comment))
                number_of_replies = comment['snippet']['totalReplyCount']

                if number_of_replies != 0:
                    next_reply_page = ''
                    while True:
                        request = youtube.comments().list(
                            part='snippet',
                            parentId=comment['id'],
                            pageToken=next_reply_page)

                        response = request.execute()
                        next_reply_page = response.get('nextPageToken', None)
                        replies = response['items']

                        for reply in replies:
                            writer.writerow(child_info(reply))

                        if not next_reply_page:
                            break

            if not next_page_token:
                break


if __name__ == "__main__":
    main()
