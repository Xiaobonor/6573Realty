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


def pad_vectors(vectors, target_dim):
    """Pad or truncate vectors to match target dimensions."""
    padded_vectors = []
    for vec in vectors:
        if len(vec) < target_dim:
            padded_vec = np.pad(vec, (0, target_dim - len(vec)), 'constant')
        else:
            padded_vec = vec[:target_dim]
        padded_vectors.append(padded_vec)
    return np.array(padded_vectors)


def calculate_similarity(bert_house_vectors, bert_user_vectors, tfidf_house_vectors, tfidf_user_vectors):
    """Calculate similarity between house tags and user tags."""
    bert_house_vectors = np.array(bert_house_vectors)
    bert_user_vectors = np.array(bert_user_vectors)
    tfidf_house_vectors = np.array(tfidf_house_vectors)
    tfidf_user_vectors = np.array(tfidf_user_vectors)

    target_dim = max(
        bert_house_vectors.shape[1] if bert_house_vectors.size > 0 else 0,
        bert_user_vectors.shape[1] if bert_user_vectors.size > 0 else 0,
        tfidf_house_vectors.shape[1] if tfidf_house_vectors.size > 0 else 0,
        tfidf_user_vectors.shape[1] if tfidf_user_vectors.size > 0 else 0
    )

    if target_dim > 0:
        # Pad vectors to the target dimension
        bert_house_vectors = pad_vectors(bert_house_vectors, target_dim)
        bert_user_vectors = pad_vectors(bert_user_vectors, target_dim)
        tfidf_house_vectors = pad_vectors(tfidf_house_vectors, target_dim)
        tfidf_user_vectors = pad_vectors(tfidf_user_vectors, target_dim)

        bert_similarities = cosine_similarity(bert_house_vectors, bert_user_vectors)
        tfidf_similarities = cosine_similarity(tfidf_house_vectors, tfidf_user_vectors)

        fused_similarities = (bert_similarities + tfidf_similarities) / 2.0
        avg_similarity = np.mean(fused_similarities)
        print(f"Average Similarity: {avg_similarity}")
    else:
        avg_similarity = 0
        print("No valid vectors found to calculate similarity.")

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
    # similarity = calculate_similarity(new_house_tags, new_user_tags)
    # print(f"Similarity: {similarity}")