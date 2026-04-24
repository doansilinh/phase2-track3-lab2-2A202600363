import os
import json
import numpy as np
from typing import List, Dict, Any, Optional
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

class ShortTermMemory:
    """Manages recent message history (sliding window)."""
    def __init__(self, window_size: int = 10):
        self.messages = []
        self.window_size = window_size

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.window_size:
            self.messages = self.messages[-self.window_size:]

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages

class LongTermMemory:
    """Manages key-value pairs of user facts with conflict handling."""
    def __init__(self, storage_path: str = "data/long_term_memory.json"):
        self.storage_path = storage_path
        self.profile = self.load_profile()

    def load_profile(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_profile(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)

    def update_fact(self, key: str, value: Any):
        self.profile[key] = value
        self.save_profile()

    def get_profile(self) -> Dict[str, Any]:
        return self.profile

class EpisodicMemory:
    """Manages a log of past tasks and outcomes."""
    def __init__(self, storage_path: str = "data/episodic_memory.json"):
        self.storage_path = storage_path
        self.episodes = self.load_episodes()

    def load_episodes(self) -> List[Dict[str, Any]]:
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_episodes(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.episodes, f, ensure_ascii=False, indent=2)

    def add_episode(self, task: str, outcome: str, context: Optional[str] = None):
        self.episodes.append({
            "task": task,
            "outcome": outcome,
            "context": context,
            "timestamp": "2026-04-24T11:28:00"
        })
        self.save_episodes()

    def get_episodes(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self.episodes[-limit:]

class SemanticMemory:
    """Manages a real Vector DB (ChromaDB) for semantic search (Bonus)."""
    def __init__(self, persist_directory: str = "data/semantic_memory"):

        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="semantic_memory"
        )

    def search(self, query: str, limit: int = 3) -> List[str]:
        """Perform semantic search using vector embeddings."""
        try:
            results = self.vector_store.similarity_search(query, k=limit)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []

    def add_knowledge(self, content: str):
        """Add a single piece of knowledge to the vector store."""
        doc = Document(page_content=content)
        self.vector_store.add_documents([doc])
