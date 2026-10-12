from sentence_transformers import SentenceTransformer, util

with open("knowledge.txt", encoding="utf-8") as f:
    blocks = f.read().strip().split("\n\n")
names = [b.split("\n")[0] for b in blocks]

STOP = {"what", "is", "the", "a", "an", "of", "to", "and", "for",
        "how", "do", "i", "my", "best", "on", "in", "with"}


def keyword_search(question):
    words = [w for w in question.lower().split() if w not in STOP]
    best, best_score = None, 0
    for i, block in enumerate(blocks):
        score = sum(1 for w in words if w in block.lower())
        if score > best_score:
            best, best_score = i, score
    return names[best] if best is not None else "No match"


model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(blocks, convert_to_tensor=True)


def semantic_search(question):
    q = model.encode(question, convert_to_tensor=True)
    scores = util.cos_sim(q, vectors)[0]
    return names[int(scores.argmax())]


tests = []
with open("tests.txt", encoding="utf-8") as f:
    for line in f:
        if "|" in line:
            q, a = line.split("|")
            tests.append((q.strip(), a.strip()))

kw_ok = 0
sem_ok = 0
for q, expected in tests:
    k = keyword_search(q)
    s = semantic_search(q)
    kw_ok += k == expected
    sem_ok += s == expected  
    if k != expected or s != expected:
        print("Q:", q)
        print("  expected:", expected, "| keyword:", k, "| semantic:", s)
    
        
        
print()
print("Keyword accuracy:", kw_ok, "/", len(tests))
print("Semantic accuracy:", sem_ok, "/", len(tests))