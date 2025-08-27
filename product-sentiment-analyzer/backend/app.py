from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

# ✅ MongoDB connection (update with your actual URI)
client = MongoClient("your_mongodb_atlas_uri_here")
db = client["sentimentDB"]
reviews_collection = db["reviews"]

# ✅ VADER sentiment analyzer
vader = SentimentIntensityAnalyzer()

@app.route("/")
def home():
    return {"message": "✅ Product Sentiment Analyzer API running!"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    product = data.get("product")
    review = data.get("review")

    if not review:
        return jsonify({"error": "Review text required"}), 400

    # Sentiment with TextBlob + VADER
    tb_score = TextBlob(review).sentiment.polarity
    vader_score = vader.polarity_scores(review)["compound"]

    sentiment = "neutral"
    if vader_score > 0.05:
        sentiment = "positive"
    elif vader_score < -0.05:
        sentiment = "negative"

    result = {
        "product": product,
        "review": review,
        "textblob_score": tb_score,
        "vader_score": vader_score,
        "sentiment": sentiment
    }

    # ✅ Save to MongoDB
    reviews_collection.insert_one(result)

    # ✅ Return full JSON response
    return jsonify(result), 200

@app.route("/reviews/<product>", methods=["GET"])
def get_reviews(product):
    reviews = list(reviews_collection.find({"product": product}, {"_id": 0}))
    return jsonify(reviews), 200

if __name__ == "__main__":
    app.run(debug=True)
