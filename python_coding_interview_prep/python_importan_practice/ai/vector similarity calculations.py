"""
Key Features:
Multiple Similarity Metrics:
Cosine Similarity: Angle between vectors (best for text embeddings)
Euclidean Distance: Straight-line distance (good for spatial data)
Manhattan Distance: Sum of absolute differences (robust to outliers)
Dot Product: Raw projection (fast for normalized vectors)
Jaccard Similarity: Set overlap (good for binary/sparse data)
Efficient Computation:
Vectorized NumPy operations
Lazy normalization
Batch processing support
Full Similarity Matrix: Compute all pairwise similarities
Performance Benchmarking: Timing comparisons
"""
import time
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class SimilarityResult:
    """Result of similarity computation"""
    query_index: int
    similar_indices: List[int]
    similar_scores: List[float]
    method: str


class VectorSimilarity:
    """
    Comprehensive vector similarity calculator supporting multiple metrics.
    """

    def __init__(self, vectors: np.ndarray):
        """
        Initialize with a matrix of vectors.

        Args:
            vectors: 2D array of shape (n_samples, n_dimensions)
        """
        self.vectors = np.array(vectors, dtype=np.float32)
        self.n_samples = self.vectors.shape[0]
        self.n_dimensions = self.vectors.shape[1]

        # Precompute normalized vectors for cosine similarity
        self._normalized_vectors = None

    @property
    def normalized_vectors(self):
        """Lazy initialization of normalized vectors"""
        if self._normalized_vectors is None:
            norms = np.linalg.norm(self.vectors, axis=1, keepdims=True)
            # Avoid division by zero
            norms = np.where(norms == 0, 1, norms)
            self._normalized_vectors = self.vectors / norms
        return self._normalized_vectors

    def cosine_similarity(self, query_idx: int, top_k: int = 5) -> SimilarityResult:
        """
        Calculate cosine similarity between query vector and all others.

        Cosine similarity measures the cosine of the angle between vectors.
        Range: [-1, 1] where 1 means identical direction.

        Args:
            query_idx: Index of the query vector
            top_k: Number of most similar vectors to return

        Returns:
            SimilarityResult with indices and scores
        """
        query_vec = self.normalized_vectors[query_idx]

        # Compute cosine similarity with all vectors
        similarities = np.dot(self.normalized_vectors, query_vec)

        # Exclude the query itself
        similarities[query_idx] = -np.inf

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        top_scores = similarities[top_indices]

        return SimilarityResult(
            query_index=query_idx,
            similar_indices=top_indices.tolist(),
            similar_scores=top_scores.tolist(),
            method="cosine"
        )

    def euclidean_distance(self, query_idx: int, top_k: int = 5) -> SimilarityResult:
        """
        Calculate Euclidean distance between query vector and all others.

        Euclidean distance is the straight-line distance between points.
        Lower values mean more similar.

        Args:
            query_idx: Index of the query vector
            top_k: Number of most similar vectors to return

        Returns:
            SimilarityResult with indices and distances
        """
        query_vec = self.vectors[query_idx]

        # Compute Euclidean distances
        diff = self.vectors - query_vec
        distances = np.sqrt(np.sum(diff ** 2, axis=1))

        # Exclude the query itself
        distances[query_idx] = np.inf

        # Get top-k (smallest distances)
        top_indices = np.argsort(distances)[:top_k]
        top_distances = distances[top_indices]

        # Convert distances to similarity scores (1 / (1 + distance))
        top_scores = 1 / (1 + top_distances)

        return SimilarityResult(
            query_index=query_idx,
            similar_indices=top_indices.tolist(),
            similar_scores=top_scores.tolist(),
            method="euclidean"
        )

    def manhattan_distance(self, query_idx: int, top_k: int = 5) -> SimilarityResult:
        """
        Calculate Manhattan (L1) distance between query vector and all others.

        Manhattan distance is the sum of absolute differences.
        Lower values mean more similar.

        Args:
            query_idx: Index of the query vector
            top_k: Number of most similar vectors to return

        Returns:
            SimilarityResult with indices and distances
        """
        query_vec = self.vectors[query_idx]

        # Compute Manhattan distances
        distances = np.sum(np.abs(self.vectors - query_vec), axis=1)

        # Exclude the query itself
        distances[query_idx] = np.inf

        # Get top-k (smallest distances)
        top_indices = np.argsort(distances)[:top_k]
        top_distances = distances[top_indices]

        # Convert distances to similarity scores
        top_scores = 1 / (1 + top_distances)

        return SimilarityResult(
            query_index=query_idx,
            similar_indices=top_indices.tolist(),
            similar_scores=top_scores.tolist(),
            method="manhattan"
        )

    def dot_product(self, query_idx: int, top_k: int = 5) -> SimilarityResult:
        """
        Calculate dot product similarity.

        Dot product measures the projection of one vector onto another.
        Higher values mean more similar (for normalized vectors, equals cosine).

        Args:
            query_idx: Index of the query vector
            top_k: Number of most similar vectors to return

        Returns:
            SimilarityResult with indices and scores
        """
        query_vec = self.vectors[query_idx]

        # Compute dot products
        similarities = np.dot(self.vectors, query_vec)

        # Exclude the query itself
        similarities[query_idx] = -np.inf

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        top_scores = similarities[top_indices]

        return SimilarityResult(
            query_index=query_idx,
            similar_indices=top_indices.tolist(),
            similar_scores=top_scores.tolist(),
            method="dot_product"
        )

    def jaccard_similarity(self, query_idx: int, top_k: int = 5,
                           threshold: float = 0.5) -> SimilarityResult:
        """
        Calculate Jaccard similarity for binary/sparse vectors.

        Jaccard similarity measures overlap between sets.
        Range: [0, 1] where 1 means identical sets.

        Args:
            query_idx: Index of the query vector
            top_k: Number of most similar vectors to return
            threshold: Threshold to binarize vectors

        Returns:
            SimilarityResult with indices and scores
        """
        # Binarize vectors
        binary_vectors = (self.vectors > threshold).astype(int)
        query_vec = binary_vectors[query_idx]

        similarities = []
        for i in range(self.n_samples):
            if i == query_idx:
                similarities.append(-1)
                continue

            other_vec = binary_vectors[i]

            # Intersection and union
            intersection = np.sum(np.logical_and(query_vec, other_vec))
            union = np.sum(np.logical_or(query_vec, other_vec))

            # Jaccard similarity
            if union == 0:
                sim = 0
            else:
                sim = intersection / union

            similarities.append(sim)

        similarities = np.array(similarities)

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        top_scores = similarities[top_indices]

        return SimilarityResult(
            query_index=query_idx,
            similar_indices=top_indices.tolist(),
            similar_scores=top_scores.tolist(),
            method="jaccard"
        )

    def batch_cosine_similarity(self, query_indices: List[int],
                                top_k: int = 5) -> List[SimilarityResult]:
        """
        Efficiently compute cosine similarity for multiple queries.

        Args:
            query_indices: List of query vector indices
            top_k: Number of most similar vectors to return per query

        Returns:
            List of SimilarityResult objects
        """
        results = []
        for idx in query_indices:
            result = self.cosine_similarity(idx, top_k)
            results.append(result)
        return results

    def similarity_matrix(self, method: str = "cosine") -> np.ndarray:
        """
        Compute full pairwise similarity matrix.

        Args:
            method: Similarity method ('cosine', 'euclidean', 'manhattan')

        Returns:
            2D array of similarity scores
        """
        if method == "cosine":
            # Efficient matrix multiplication for cosine similarity
            sim_matrix = np.dot(self.normalized_vectors, self.normalized_vectors.T)
        elif method == "euclidean":
            # Pairwise Euclidean distances
            diff = self.vectors[:, np.newaxis, :] - self.vectors[np.newaxis, :, :]
            sim_matrix = np.sqrt(np.sum(diff ** 2, axis=2))
            # Convert to similarity
            sim_matrix = 1 / (1 + sim_matrix)
        elif method == "manhattan":
            # Pairwise Manhattan distances
            diff = np.abs(self.vectors[:, np.newaxis, :] - self.vectors[np.newaxis, :, :])
            sim_matrix = np.sum(diff, axis=2)
            # Convert to similarity
            sim_matrix = 1 / (1 + sim_matrix)
        else:
            raise ValueError(f"Unknown method: {method}")

        return sim_matrix


def generate_sample_data(n_samples: int = 100, n_dimensions: int = 128,
                         n_clusters: int = 5) -> np.ndarray:
    """
    Generate sample clustered data for testing.

    Args:
        n_samples: Number of vectors
        n_dimensions: Dimensionality of vectors
        n_clusters: Number of clusters

    Returns:
        Array of shape (n_samples, n_dimensions)
    """
    np.random.seed(42)

    # Generate cluster centers
    centers = np.random.randn(n_clusters, n_dimensions) * 5

    # Assign samples to clusters
    vectors = []
    samples_per_cluster = n_samples // n_clusters

    for i in range(n_clusters):
        # Generate samples around each center
        cluster_samples = centers[i] + np.random.randn(samples_per_cluster, n_dimensions)
        vectors.append(cluster_samples)

    # Add remaining samples
    remaining = n_samples - (samples_per_cluster * n_clusters)
    if remaining > 0:
        extra_samples = centers[0] + np.random.randn(remaining, n_dimensions)
        vectors.append(extra_samples)

    return np.vstack(vectors)


def demonstrate_similarity():
    """Demonstrate different similarity methods"""

    print("=" * 70)
    print("VECTOR SIMILARITY DEMONSTRATION")
    print("=" * 70)

    # Generate sample data
    print("\nGenerating sample data...")
    vectors = generate_sample_data(n_samples=100, n_dimensions=128, n_clusters=5)
    print(f"Generated {vectors.shape[0]} vectors with {vectors.shape[1]} dimensions")

    # Initialize similarity calculator
    vs = VectorSimilarity(vectors)

    # Test query
    query_idx = 0

    print(f"\nQuery vector index: {query_idx}")
    print("-" * 70)

    # Test different similarity methods
    methods = [
        ("Cosine Similarity", vs.cosine_similarity),
        ("Euclidean Distance", vs.euclidean_distance),
        ("Manhattan Distance", vs.manhattan_distance),
        ("Dot Product", vs.dot_product),
    ]

    for method_name, method_func in methods:
        print(f"\n{method_name}:")
        print("-" * 70)

        start_time = time.time()
        result = method_func(query_idx, top_k=5)
        elapsed = time.time() - start_time

        print(f"Computation time: {elapsed * 1000:.2f} ms")
        print(f"\nTop 5 most similar vectors:")
        print(f"{'Rank':<6} {'Index':<8} {'Score':<12}")
        print("-" * 70)

        for rank, (idx, score) in enumerate(zip(result.similar_indices,
                                                result.similar_scores), 1):
            print(f"{rank:<6} {idx:<8} {score:<12.6f}")

    # Jaccard similarity (requires binary data)
    print(f"\nJaccard Similarity (binary):")
    print("-" * 70)

    # Create binary vectors for Jaccard
    binary_vectors = (vectors > 0).astype(float)
    vs_binary = VectorSimilarity(binary_vectors)

    result = vs_binary.jaccard_similarity(query_idx, top_k=5)

    print(f"Top 5 most similar vectors:")
    print(f"{'Rank':<6} {'Index':<8} {'Score':<12}")
    print("-" * 70)

    for rank, (idx, score) in enumerate(zip(result.similar_indices,
                                            result.similar_scores), 1):
        print(f"{rank:<6} {idx:<8} {score:<12.6f}")

    # Full similarity matrix
    print(f"\n\nComputing full similarity matrix...")
    print("-" * 70)

    start_time = time.time()
    sim_matrix = vs.similarity_matrix(method="cosine")
    elapsed = time.time() - start_time

    print(f"Matrix shape: {sim_matrix.shape}")
    print(f"Computation time: {elapsed * 1000:.2f} ms")
    print(f"Min similarity: {sim_matrix.min():.6f}")
    print(f"Max similarity: {sim_matrix.max():.6f}")
    print(f"Mean similarity: {sim_matrix.mean():.6f}")

    # Batch processing
    print(f"\n\nBatch processing (10 queries)...")
    print("-" * 70)

    query_indices = list(range(10))

    start_time = time.time()
    results = vs.batch_cosine_similarity(query_indices, top_k=3)
    elapsed = time.time() - start_time

    print(f"Total time: {elapsed * 1000:.2f} ms")
    print(f"Average time per query: {elapsed * 1000 / len(query_indices):.2f} ms")

    print("\nSample results:")
    for result in results[:3]:
        print(f"Query {result.query_index}: Top matches at indices {result.similar_indices[:3]}")


def compare_with_sklearn():
    """Compare our implementation with sklearn"""
    try:
        from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

        print("\n" + "=" * 70)
        print("COMPARISON WITH SKLEARN")
        print("=" * 70)

        # Generate small dataset
        vectors = generate_sample_data(n_samples=50, n_dimensions=64)

        # Our implementation
        vs = VectorSimilarity(vectors)

        # Cosine similarity comparison
        print("\nCosine Similarity Comparison:")
        print("-" * 70)

        our_result = vs.cosine_similarity(0, top_k=5)
        sklearn_sim = cosine_similarity(vectors)

        # Get sklearn top-5 for query 0
        sklearn_sim[0, 0] = -np.inf
        sklearn_top_idx = np.argsort(sklearn_sim[0])[::-1][:5]
        sklearn_top_scores = sklearn_sim[0, sklearn_top_idx]

        print(f"Our implementation:      {our_result.similar_scores}")
        print(f"Sklearn implementation:  {sklearn_top_scores.tolist()}")
        print(f"Match: {np.allclose(our_result.similar_scores, sklearn_top_scores)}")

        # Euclidean distance comparison
        print("\nEuclidean Distance Comparison:")
        print("-" * 70)

        our_result = vs.euclidean_distance(0, top_k=5)
        sklearn_dist = euclidean_distances(vectors)

        sklearn_dist[0, 0] = np.inf
        sklearn_top_idx = np.argsort(sklearn_dist[0])[:5]
        sklearn_top_dists = sklearn_dist[0, sklearn_top_idx]
        sklearn_top_scores = 1 / (1 + sklearn_top_dists)

        print(f"Our implementation:      {our_result.similar_scores}")
        print(f"Sklearn implementation:  {sklearn_top_scores.tolist()}")
        print(f"Match: {np.allclose(our_result.similar_scores, sklearn_top_scores)}")

    except ImportError:
        print("\nSklearn not installed. Install with: pip install scikit-learn")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_similarity()
    compare_with_sklearn()

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
