from pathlib import Path
from typing import List

from crewai.knowledge.embedder.base_embedder import BaseEmbedder
from crewai.knowledge.source.base_knowledge_source import BaseKnowledgeSource


class TextFileKnowledgeSource(BaseKnowledgeSource):
    """A knowledge source that stores and queries text file content using embeddings."""

    def __init__(
        self,
        file_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        super().__init__(chunk_size, chunk_overlap)
        self.file_path = Path(file_path)
        self.content = self.load_content()

    def load_content(self) -> str:
        """Load and preprocess text file content."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if not self.file_path.is_file():
            raise ValueError(f"Path is not a file: {self.file_path}")

        with self.file_path.open("r", encoding="utf-8") as f:
            return f.read()

    def add(self, embedder: BaseEmbedder) -> None:
        """
        Add text file content to the knowledge source, chunk it, compute embeddings,
        and save the embeddings.
        """
        new_chunks = self._chunk_text(self.content)
        self.chunks.extend(new_chunks)
        # Compute embeddings for the new chunks
        new_embeddings = embedder.embed_chunks(new_chunks)
        # Save the embeddings
        self.chunk_embeddings.extend(new_embeddings)

    def _chunk_text(self, text: str) -> List[str]:
        """Utility method to split text into chunks."""
        return [
            text[i : i + self.chunk_size]
            for i in range(0, len(text), self.chunk_size - self.chunk_overlap)
        ]
