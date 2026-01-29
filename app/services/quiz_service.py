class QuizService:

    def generate_quiz(self, topic: str) -> dict:
        return {
            "question": f"What is the purpose of {topic}?",
            "type": "short-answer"
        }
