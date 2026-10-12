from sentence_transformers import SentenceTransformer, util

with open("knowledge.txt", encoding="utf-8") as f:
    blocks = f.read().strip().split("\n\n")

model = SentenceTransformer("all-MiniLM-L6-v2")
block_vectors = model.encode(blocks, convert_to_tensor=True)


def search(question):
    q_vec = model.encode(question, convert_to_tensor=True)
    scores = util.cos_sim(q_vec, block_vectors)[0]
    best = int(scores.argmax())
    return best, float(scores[best])


while True:
    q = input("Ask (or type quit): ")
    if q == "quit":
        break
    i, score = search(q)
    print(blocks[i])
    print("Score:", round(score, 2))
    print()