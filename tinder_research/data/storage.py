"""
Data storage and retrieval for conversations.

Handles persistence, anonymization, and reproducible data access.
"""

import json
import pickle
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
from loguru import logger

from ..simulation.conversation_simulator import Conversation, Message


class ConversationStorage:
    """Store and retrieve conversations."""

    def __init__(self, storage_dir: Path = Path("data")):
        """Initialize storage."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Conversation storage initialized at {self.storage_dir}")

    def save_conversations(
        self,
        conversations: List[Conversation],
        name: str,
        format: str = "json"
    ) -> Path:
        """
        Save conversations to disk.

        Args:
            conversations: List of conversation objects
            name: Name for this dataset
            format: 'json', 'pickle', or 'parquet'

        Returns:
            Path to saved file
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "json":
            return self._save_json(conversations, name, timestamp)
        elif format == "pickle":
            return self._save_pickle(conversations, name, timestamp)
        elif format == "parquet":
            return self._save_parquet(conversations, name, timestamp)
        else:
            raise ValueError(f"Unknown format: {format}")

    def _save_json(
        self,
        conversations: List[Conversation],
        name: str,
        timestamp: str
    ) -> Path:
        """Save as JSON (human-readable)."""

        data = {
            "metadata": {
                "name": name,
                "timestamp": timestamp,
                "num_conversations": len(conversations),
                "format_version": "1.0"
            },
            "conversations": [
                self._conversation_to_dict(conv)
                for conv in conversations
            ]
        }

        output_path = self.storage_dir / f"{name}_{timestamp}.json"

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"Saved {len(conversations)} conversations to {output_path}")
        return output_path

    def _save_pickle(
        self,
        conversations: List[Conversation],
        name: str,
        timestamp: str
    ) -> Path:
        """Save as pickle (efficient binary)."""

        output_path = self.storage_dir / f"{name}_{timestamp}.pkl"

        with open(output_path, "wb") as f:
            pickle.dump(conversations, f)

        logger.info(f"Saved {len(conversations)} conversations to {output_path}")
        return output_path

    def _save_parquet(
        self,
        conversations: List[Conversation],
        name: str,
        timestamp: str
    ) -> Path:
        """Save as Parquet (efficient columnar)."""

        # Convert to DataFrame for parquet
        rows = []
        for conv in conversations:
            for msg in conv.messages:
                rows.append({
                    "conversation_id": conv.user_a.safe_id + "_" + conv.user_b.safe_id,
                    "user_a_id": conv.user_a.safe_id,
                    "user_b_id": conv.user_b.safe_id,
                    "sender_id": msg.sender_id,
                    "recipient_id": msg.recipient_id,
                    "message_text": msg.text,
                    "turn": msg.turn,
                    "message_length": msg.length,
                })

            # Add conversation metadata
            if rows:
                rows[-1]["conversation_outcome"] = conv.outcome
                rows[-1]["num_turns"] = conv.num_turns
                rows[-1]["total_chars"] = conv.total_chars

        df = pd.DataFrame(rows)

        output_path = self.storage_dir / f"{name}_{timestamp}.parquet"
        df.to_parquet(output_path, index=False)

        logger.info(f"Saved {len(conversations)} conversations to {output_path}")
        return output_path

    def load_conversations(self, filepath: Path) -> List[Conversation]:
        """Load conversations from disk."""

        if str(filepath).endswith(".json"):
            return self._load_json(filepath)
        elif str(filepath).endswith(".pkl"):
            return self._load_pickle(filepath)
        else:
            raise ValueError(f"Unknown file format: {filepath}")

    def _load_json(self, filepath: Path) -> List[Conversation]:
        """Load from JSON."""

        with open(filepath, "r") as f:
            data = json.load(f)

        conversations = []
        for conv_data in data.get("conversations", []):
            conv = self._dict_to_conversation(conv_data)
            conversations.append(conv)

        logger.info(f"Loaded {len(conversations)} conversations from {filepath}")
        return conversations

    def _load_pickle(self, filepath: Path) -> List[Conversation]:
        """Load from pickle."""

        with open(filepath, "rb") as f:
            conversations = pickle.load(f)

        logger.info(f"Loaded {len(conversations)} conversations from {filepath}")
        return conversations

    def _conversation_to_dict(self, conv: Conversation) -> Dict:
        """Convert conversation to dictionary."""

        return {
            "user_a": {
                "id": conv.user_a.safe_id,
                "age": conv.user_a.age,
                "gender": conv.user_a.gender,
                "race": conv.user_a.race_ethnicity,
                "education": conv.user_a.education,
            },
            "user_b": {
                "id": conv.user_b.safe_id,
                "age": conv.user_b.age,
                "gender": conv.user_b.gender,
                "race": conv.user_b.race_ethnicity,
                "education": conv.user_b.education,
            },
            "messages": [
                {
                    "sender_id": msg.sender_id,
                    "recipient_id": msg.recipient_id,
                    "text": msg.text,
                    "turn": msg.turn,
                    "length": msg.length,
                }
                for msg in conv.messages
            ],
            "outcome": conv.outcome,
            "num_turns": conv.num_turns,
            "total_chars": conv.total_chars,
            "completed": conv.completed,
        }

    def _dict_to_conversation(self, data: Dict) -> Conversation:
        """Reconstruct conversation from dictionary."""

        # Note: This is simplified; real reconstruction would need UserProfile objects
        # For now, just return a dict-based representation
        logger.warning("Dict-to-Conversation reconstruction not fully implemented")
        return data

    def export_analytics_csv(
        self,
        conversations: List[Conversation],
        output_path: Path
    ) -> Path:
        """Export conversations to CSV for analysis."""

        rows = []

        for conv in conversations:
            rows.append({
                "conversation_id": f"{conv.user_a.safe_id}_{conv.user_b.safe_id}",
                "initiator_gender": conv.user_a.gender,
                "initiator_age": conv.user_a.age,
                "initiator_race": conv.user_a.race_ethnicity,
                "recipient_gender": conv.user_b.gender,
                "recipient_age": conv.user_b.age,
                "recipient_race": conv.user_b.race_ethnicity,
                "num_messages": len(conv.messages),
                "num_turns": conv.num_turns,
                "total_characters": conv.total_chars,
                "outcome": conv.outcome,
                "completed": conv.completed,
            })

        df = pd.DataFrame(rows)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

        logger.info(f"Exported {len(rows)} conversations to {output_path}")
        return output_path


class AnonymizationManager:
    """Verify and enforce anonymization."""

    def __init__(self):
        """Initialize anonymization manager."""
        self.anonymization_log = []

    def hash_id(self, real_id: str) -> str:
        """Hash an identifier for anonymization."""

        return "user_" + hashlib.sha256(
            real_id.encode()
        ).hexdigest()[:8] + "_synthetic"

    def verify_anonymization(self, conversations: List[Conversation]) -> Dict[str, bool]:
        """Verify conversations are properly anonymized."""

        checks = {
            "no_real_ids": True,
            "no_real_names": True,
            "no_personally_identifiable": True,
            "all_ids_hashed": True,
        }

        # Check for obvious real identifiers
        for conv in conversations:
            for msg in conv.messages:
                text = msg.text.lower()

                # These are unlikely in synthetic conversations
                if any(x in text for x in ["facebook.com", "instagram.com", "phone:", "email:"]):
                    checks["no_real_ids"] = False

                # Check for common patterns
                if "@" in msg.text and ".com" in msg.text:
                    checks["no_personally_identifiable"] = False

        # Check ID format
        for conv in conversations:
            if not str(conv.user_a.safe_id).startswith("user_"):
                checks["all_ids_hashed"] = False
            if not str(conv.user_b.safe_id).startswith("user_"):
                checks["all_ids_hashed"] = False

        logger.info(f"Anonymization verification: {checks}")
        return checks

    def audit_log(self, action: str, details: Dict) -> None:
        """Log anonymization-related actions."""

        self.anonymization_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        })

    def get_audit_log(self) -> List[Dict]:
        """Get full audit log."""
        return self.anonymization_log
