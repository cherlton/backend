from app.services.youtube_service import YouTubeService
from app.services.embedding_service import EmbeddingService
from app.services.clustering_service import ClusteringService
from app.repositories.trend_repository import TrendRepository
from app.services.llm_service import LLMService # Add this import

class TrendAgent:
    def __init__(self):
        self.youtube = YouTubeService()
        self.embedder = EmbeddingService()
        self.clusterer = ClusteringService()
        self.llm = LLMService() # Add this
        self.repo = TrendRepository()
    def run(self, topic: str, user_id: int):
        videos_data = self.youtube.search_videos(topic)
        ai_input_texts = [v['content_for_ai'] for v in videos_data]
        
        # Get AI Deep Summary
        dynamic_summary = self.llm.summarize_trends(topic, ai_input_texts)
        
        # Get Clusters
        embeddings = self.embedder.embed(ai_input_texts)
        clusters = self.clusterer.cluster(embeddings)
        
        # Save to DB
        self.repo.create(topic=topic, summary=dynamic_summary, user_id=user_id)
        return {
            "topic": topic,
            "summary": dynamic_summary,
            "clusters": clusters,
            "video_count": len(videos_data),
            "videos": [
                {
                    "id": v['id'],
                    "title": v['title'],
                    "url": v['url'],
                    "thumbnail": v['thumbnail']
                } for v in videos_data
            ]
        }