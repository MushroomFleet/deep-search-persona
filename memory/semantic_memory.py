"""
Semantic memory using embeddings for similarity search
Integrates with OpenAI embeddings API for production-quality vector search
"""
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from dataclasses import dataclass
import pickle
import os
from pathlib import Path


@dataclass
class SemanticItem:
    """Item stored in semantic memory"""
    id: str
    content: str
    embedding: np.ndarray
    metadata: Dict[str, Any]
    timestamp: float


class SemanticMemory:
    """
    Semantic memory using vector embeddings for similarity search
    
    Uses OpenAI embeddings API for production-quality vector search
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        model: str = "text-embedding-3-small",
        dimensions: int = 1536,
        cache_enabled: bool = True,
        max_cache_size: int = 10000
    ):
        """
        Initialize semantic memory
        
        Args:
            openai_api_key: OpenAI API key for embeddings
            model: Embedding model to use
            dimensions: Embedding dimensions (1536 for text-embedding-3-small)
            cache_enabled: Enable embedding caching
            max_cache_size: Maximum number of cached embeddings
        """
        self.openai_api_key = openai_api_key
        self.model = model
        self.dimensions = dimensions
        self.cache_enabled = cache_enabled
        self.max_cache_size = max_cache_size
        
        self.items = []  # List of SemanticItems
        self.embeddings_cache = {}  # text -> embedding
        
        # Initialize OpenAI client if API key provided
        self.openai_client = None
        if openai_api_key:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=openai_api_key)
            except ImportError:
                print("Warning: openai package not installed. Install with: pip install openai")
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
    
    def store(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Store content with semantic embedding"""
        import time
        
        # Generate embedding
        embedding = self._get_embedding(content)
        
        # Create item
        item_id = f"sem_{int(time.time() * 1000)}_{len(self.items)}"
        item = SemanticItem(
            id=item_id,
            content=content,
            embedding=embedding,
            metadata=metadata or {},
            timestamp=time.time()
        )
        
        self.items.append(item)
        return item_id
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.7) -> List[Tuple[SemanticItem, float]]:
        """
        Semantic similarity search
        
        Returns items most similar to query with similarity scores
        """
        if not self.items:
            return []
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Calculate similarities
        similarities = []
        for item in self.items:
            similarity = self._cosine_similarity(query_embedding, item.embedding)
            if similarity >= threshold:
                similarities.append((item, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def find_related(self, item_id: str, top_k: int = 5) -> List[Tuple[SemanticItem, float]]:
        """Find items related to a specific item"""
        # Find item
        item = next((i for i in self.items if i.id == item_id), None)
        if not item:
            return []
        
        # Search using item content
        results = self.search(item.content, top_k=top_k + 1)
        # Filter out self
        return [(i, s) for i, s in results if i.id != item_id][:top_k]
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding for text using OpenAI API or fallback
        """
        # Check cache first
        if self.cache_enabled and text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        # Try OpenAI API
        if self.openai_client:
            try:
                embedding = self._get_embedding_from_openai(text)
            except Exception as e:
                print(f"Warning: OpenAI embedding failed: {e}. Using fallback.")
                embedding = self._get_fallback_embedding(text)
        else:
            # Use fallback if no API client
            embedding = self._get_fallback_embedding(text)
        
        # Cache embedding
        if self.cache_enabled:
            # Manage cache size
            if len(self.embeddings_cache) >= self.max_cache_size:
                # Remove oldest entry (simple FIFO)
                first_key = next(iter(self.embeddings_cache))
                del self.embeddings_cache[first_key]
            
            self.embeddings_cache[text] = embedding
        
        return embedding
    
    def _get_embedding_from_openai(self, text: str) -> np.ndarray:
        """Get embedding from OpenAI API"""
        response = self.openai_client.embeddings.create(
            input=text,
            model=self.model
        )
        
        # Extract embedding vector
        embedding = np.array(response.data[0].embedding, dtype=np.float32)
        
        return embedding
    
    def _get_fallback_embedding(self, text: str) -> np.ndarray:
        """
        Fallback embedding using simple text features
        Used when OpenAI API is not available
        """
        # Simple word frequency-based embedding
        words = text.lower().split()
        embedding = np.zeros(self.dimensions, dtype=np.float32)
        
        # Distribute word hashes across dimensions
        for word in words:
            idx = hash(word) % self.dimensions
            embedding[idx] += 1
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return float(dot_product / (norm_a * norm_b))
    
    def cluster_items(self, num_clusters: int = 5) -> Dict[int, List[SemanticItem]]:
        """
        Cluster items by semantic similarity
        
        Useful for identifying themes in research
        """
        if len(self.items) < num_clusters:
            return {0: self.items}
        
        # Simple k-means-like clustering
        import random
        
        # Initialize random centroids
        centroids_items = random.sample(self.items, num_clusters)
        centroids = [item.embedding for item in centroids_items]
        
        # Iterate to refine clusters
        for iteration in range(10):  # Max 10 iterations
            # Assign items to clusters
            clusters = {i: [] for i in range(num_clusters)}
            
            for item in self.items:
                # Find closest centroid
                distances = [
                    1 - self._cosine_similarity(item.embedding, centroid)
                    for centroid in centroids
                ]
                closest = distances.index(min(distances))
                clusters[closest].append(item)
            
            # Update centroids
            new_centroids = []
            for i in range(num_clusters):
                if clusters[i]:
                    # Average embeddings in cluster
                    cluster_embeddings = np.array([item.embedding for item in clusters[i]])
                    new_centroid = np.mean(cluster_embeddings, axis=0)
                    # Normalize
                    norm = np.linalg.norm(new_centroid)
                    if norm > 0:
                        new_centroid = new_centroid / norm
                    new_centroids.append(new_centroid)
                else:
                    # Keep old centroid if cluster is empty
                    new_centroids.append(centroids[i])
            
            centroids = new_centroids
        
        return clusters
    
    def save_to_disk(self, filepath: str):
        """Persist semantic memory to disk using pickle"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'items': self.items,
            'cache': self.embeddings_cache,
            'model': self.model,
            'dimensions': self.dimensions
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load_from_disk(self, filepath: str):
        """Load semantic memory from disk"""
        if not os.path.exists(filepath):
            print(f"Warning: File {filepath} does not exist")
            return
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.items = data.get('items', [])
        self.embeddings_cache = data.get('cache', {})
        
        # Verify model compatibility
        if data.get('model') != self.model:
            print(f"Warning: Loaded model {data.get('model')} differs from current {self.model}")
        if data.get('dimensions') != self.dimensions:
            print(f"Warning: Loaded dimensions {data.get('dimensions')} differs from current {self.dimensions}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_items": len(self.items),
            "cache_size": len(self.embeddings_cache),
            "model": self.model,
            "dimensions": self.dimensions,
            "cache_enabled": self.cache_enabled,
            "using_openai": self.openai_client is not None
        }
    
    def clear(self):
        """Clear all items and cache"""
        self.items = []
        self.embeddings_cache = {}
