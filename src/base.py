from src.models import InferenceRequest

from fastapi import APIRouter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

base_router = APIRouter(tags=["sentiment-analyzer"])
analyzer = SentimentIntensityAnalyzer()


@base_router.get("/ping")
async def root():
    return {
        "message": "inference API is healthy, and running",
        "data": {
            "name": "sentiment-analyzer",
            "version": "0.1.0",
        },
    }


async def decide(score: float) -> str:
    if score > 0.05:
        return "positive"
    elif score < -0.05:
        return "negative"
    else:
        return "neutral"


@base_router.post("/invocations")
async def predict(request: InferenceRequest):
    if isinstance(request.data, str):
        vs = analyzer.polarity_scores(request.data)
        label = await decide(vs["compound"])
        return {
            "message": "model produced the prediction successfully",
            "sentiment": label
        }
    else:
        labels = []
        for sentence in request.data:
            vs = analyzer.polarity_scores(sentence)
            label = await decide(vs["compound"])
            labels.append(label)
        return {
            "message": "model produced the prediction successfully",
            "sentiment": labels
        }