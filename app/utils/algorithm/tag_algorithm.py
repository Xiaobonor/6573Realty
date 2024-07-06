# app/utils/algorithm/tag_algorithm.py
from transformers import AutoTokenizer, AutoModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.models.tags import Tag
from app import device

tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
model = AutoModel.from_pretrained("bert-base-chinese").to(device)


def remove_hash(tags):
    """Remove hash symbol from tags."""
    return [tag.lstrip('#') for tag in tags]


def get_bert_vectors(tags):
    """Calculate BERT vectors."""
    vectors = []
    for tag in tags:
        inputs = tokenizer(tag, return_tensors='pt', padding=True, truncation=True, max_length=10).to(device)
        outputs = model(**inputs)
        # Get the vector for the [CLS] token
        vector = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()
        vectors.append(vector[0])
    return np.array(vectors)


def get_tfidf_vectors(tags):
    """Calculate TF-IDF vectors."""
    all_tags = list(Tag.get_all_related_tags("allTags"))
    if not all_tags:
        raise ValueError("No tags found in the database for TF-IDF vectorization.")

    tfidf = TfidfVectorizer()
    tfidf.fit(all_tags)  # Use all tags to fit the TF-IDF model
    vectors = tfidf.transform(tags)
    return vectors.toarray()


def calculate_similarity(house_tags, user_tags):
    """Calculate similarity between house tags and user tags."""
    house_tags = remove_hash(house_tags)
    user_tags = remove_hash(user_tags)

    bert_house_vectors = get_bert_vectors(house_tags)
    bert_user_vectors = get_bert_vectors(user_tags)

    tfidf_house_vectors = get_tfidf_vectors(house_tags)
    tfidf_user_vectors = get_tfidf_vectors(user_tags)

    bert_similarities = cosine_similarity(bert_house_vectors, bert_user_vectors)
    tfidf_similarities = cosine_similarity(tfidf_house_vectors, tfidf_user_vectors)

    # Merge BERT and TF-IDF similarities
    fused_similarities = (bert_similarities + tfidf_similarities) / 2.0

    # Calculate the average similarity
    avg_similarity = np.mean(fused_similarities)
    return avg_similarity


def analyze_similarity_results(results):
    """Analyze similarity results."""
    analysis = {}
    for house, matches in results.items():
        scores = [score for _, score in matches]
        n = len(scores)

        analysis[house] = {
            "10%": scores[:int(0.1 * n)],
            "10-25%": scores[int(0.1 * n):int(0.25 * n)],
            "25-50%": scores[int(0.25 * n):int(0.5 * n)],
            "50-75%": scores[int(0.5 * n):int(0.75 * n)],
            "75-100%": scores[int(0.75 * n):]
        }
    return analysis

# test
if __name__ == "__main__":
    new_house_tags = ["#大窗戶", "#內建櫃", "#簡約風格", "#中等臥室", "#乾淨設計", "#多功能房", "#內嵌燈", "#鏡子",
                      "#洗手台", "#磚牆", "#高樓層"]
    new_user_tags = ["#遊戲室", "#米色牆", "#排氣扇窗戶", "#低樓層"]

    # Calculate BERT vectors and TF-IDF vectors for new house tags
    new_house_bert_vectors = get_bert_vectors(remove_hash(new_house_tags))
    new_house_tfidf_vectors = get_tfidf_vectors(remove_hash(new_house_tags))

    # Calculate BERT vectors and TF-IDF vectors for new user tags
    new_user_bert_vectors = get_bert_vectors(remove_hash(new_user_tags))
    new_user_tfidf_vectors = get_tfidf_vectors(remove_hash(new_user_tags))

    print("New House BERT Vectors:")
    print(new_house_bert_vectors)
    print("New House TF-IDF Vectors:")
    print(new_house_tfidf_vectors)

    print("New User BERT Vectors:")
    print(new_user_bert_vectors)
    print("New User TF-IDF Vectors:")
    print(new_user_tfidf_vectors)

    # Calculate similarity between new house tags and new user tags
    similarity = calculate_similarity(new_house_tags, new_user_tags)
    print(f"Similarity: {similarity}")