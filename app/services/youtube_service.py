import os
from googleapiclient.discovery import build

class YouTubeService:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def search_videos(self, topic: str) -> list[dict]:
        request = self.youtube.search().list(
            q=topic,
            part='snippet',
            maxResults=50,  # Increased from 10 to 50
            type='video',
            order='relevance' # Ensures you get the most relevant dynamic results
        )
        response = request.execute()
        
        videos = []
        for item in response.get('items', []):
            videos.append({
                "id": item['id']['videoId'],
                "title": item['snippet']['title'],
                "description": item['snippet']['description'],
                "thumbnail": item['snippet']['thumbnails']['high']['url'],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "content_for_ai": f"{item['snippet']['title']}: {item['snippet']['description']}"
            })
        return videos