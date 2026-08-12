import numpy as np

from app.services.similarity_service import SimilarityService

service = SimilarityService()

e1 = np.random.rand(512).astype(np.float32)
e2 = e1.copy()

print(service.cosine_similarity(e1, e2))
print(service.euclidean_distance(e1, e2))
print(service.is_same_person(e1, e2))