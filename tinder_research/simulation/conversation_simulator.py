"""
Simulates conversations between synthetic users.

Each conversation is a turn-based exchange where both users are
LLM agents responding based on their profiles and strategies.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import numpy as np
from loguru import logger

from .user_generator import UserProfile


@dataclass
class Message:
    """Single message in a conversation."""

    sender_id: str
    recipient_id: str
    text: str
    turn: int
    timestamp: datetime
    length: int = field(init=False)

    def __post_init__(self):
        self.length = len(self.text)


@dataclass
class Conversation:
    """Complete conversation between two users."""

    user_a: UserProfile
    user_b: UserProfile
    messages: List[Message] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    # Outcome tracking
    completed: bool = False
    outcome: Optional[str] = None  # "continued", "rejected", "met"
    num_turns: int = 0
    total_chars: int = 0

    @property
    def conversation_text(self) -> str:
        """Full conversation as text."""
        return "\n".join(f"{m.sender_id}: {m.text}" for m in self.messages)

    @property
    def duration_minutes(self) -> float:
        """Approximate duration in minutes."""
        if not self.messages:
            return 0
        return (self.messages[-1].timestamp - self.messages[0].timestamp).total_seconds() / 60


class ConversationSimulator:
    """Simulates conversations between users."""

    def __init__(self, llm_client, config):
        """
        Initialize simulator.

        Args:
            llm_client: LLM API client (OpenAI or Anthropic)
            config: Configuration object
        """
        self.llm = llm_client
        self.config = config
        self.max_turns = config.get("max_turns_per_conversation", 25)
        self.temperature = config.get("temperature", 0.7)

    def simulate_match(
        self,
        user_a: UserProfile,
        user_b: UserProfile,
        homophily_strength: float = 0.6
    ) -> Tuple[bool, float]:
        """
        Determine if two users match based on homophily.

        Args:
            user_a: First user
            user_b: Second user
            homophily_strength: How much homophily affects matching (0-1)

        Returns:
            (does_match: bool, match_probability: float)
        """

        # Calculate similarity metrics
        age_similarity = 1.0 - (abs(user_a.age - user_b.age) / 30)  # Normalized

        race_match = user_b.race_ethnicity in user_a.race_preference_weights
        race_pref = user_a.race_preference_weights.get(user_b.race_ethnicity, 0.1)

        education_match = user_a.education == user_b.education
        education_sim = 0.7 if education_match else 0.3

        # Combined match probability
        base_match = (
            0.3 * age_similarity +
            0.4 * race_pref +
            0.3 * education_sim
        )

        # Apply homophily strength
        match_prob = homophily_strength * base_match + (1 - homophily_strength) * 0.5

        # Add randomness
        match_prob = np.clip(match_prob + np.random.normal(0, 0.1), 0, 1)

        matches = np.random.random() < match_prob

        return matches, match_prob

    def simulate_conversation(
        self,
        user_a: UserProfile,
        user_b: UserProfile,
    ) -> Conversation:
        """
        Simulate a complete conversation.

        Args:
            user_a: Initiating user
            user_b: Receiving user

        Returns:
            Conversation object with full message history
        """

        conversation = Conversation(user_a=user_a, user_b=user_b)

        logger.debug(
            f"Starting conversation: {user_a.safe_id} → {user_b.safe_id}"
        )

        # User A opens
        try:
            opener = self._generate_opener(user_a, user_b)
            if not opener:
                conversation.outcome = "no_opener"
                return conversation

            msg1 = Message(
                sender_id=user_a.safe_id,
                recipient_id=user_b.safe_id,
                text=opener,
                turn=1,
                timestamp=datetime.now()
            )
            conversation.messages.append(msg1)

        except Exception as e:
            logger.warning(f"Failed to generate opener: {e}")
            conversation.outcome = "error"
            return conversation

        # Conversation loop
        current_turn = 2
        while current_turn <= self.max_turns:
            # Determine speaker
            if current_turn % 2 == 0:
                speaker, recipient = user_b, user_a
            else:
                speaker, recipient = user_a, user_b

            # Check if speaker is interested
            if not np.random.random() < speaker.response_threshold:
                conversation.outcome = "dropped"
                break

            # Generate response
            try:
                response = self._generate_response(
                    speaker, recipient, conversation.messages
                )

                if not response:
                    conversation.outcome = "empty_response"
                    break

                msg = Message(
                    sender_id=speaker.safe_id,
                    recipient_id=recipient.safe_id,
                    text=response,
                    turn=current_turn,
                    timestamp=datetime.now()
                )
                conversation.messages.append(msg)

            except Exception as e:
                logger.warning(f"Failed to generate response at turn {current_turn}: {e}")
                break

            current_turn += 1

            # Check for natural conclusion
            if current_turn > 3 and self._should_conclude(conversation.messages[-1].text):
                conversation.outcome = "concluded"
                break

        # Set final state
        conversation.completed = len(conversation.messages) > 1
        conversation.num_turns = len(conversation.messages)
        conversation.total_chars = sum(m.length for m in conversation.messages)

        if not conversation.outcome:
            conversation.outcome = "max_turns_reached"

        logger.debug(
            f"Conversation ended: {conversation.outcome} "
            f"({conversation.num_turns} turns)"
        )

        return conversation

    def _generate_opener(self, user_a: UserProfile, user_b: UserProfile) -> Optional[str]:
        """Generate first message."""

        prompt = f"""You are {user_a.fake_name}, a {user_a.age}-year-old {user_a.gender}.
Your profile:
- Headline: {user_a.headline}
- About you: {user_a.bio}
- Interests: {', '.join(user_a.interests)}
- Occupation: {user_a.occupation}

You just matched with {user_b.fake_name}. Their profile:
- Headline: {user_b.headline}
- About them: {user_b.bio}
- Interests: {', '.join(user_b.interests)}

Your conversation style: {user_a.conversation_strategy}

Write a SHORT, natural first message. Be yourself. Keep it under 50 words.
Do NOT be generic or robotic. Sound authentic.

Message:"""

        try:
            response = self.llm.create_message(
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=100
            )
            return response.strip() if response else None
        except Exception as e:
            logger.error(f"LLM error in opener: {e}")
            return None

    def _generate_response(
        self,
        speaker: UserProfile,
        recipient: UserProfile,
        previous_messages: List[Message]
    ) -> Optional[str]:
        """Generate response to previous message."""

        # Build conversation context
        conversation_context = "\n".join(
            f"{'→' if m.sender_id == speaker.safe_id else '←'} {m.text}"
            for m in previous_messages[-4:]  # Last 4 messages
        )

        prompt = f"""You are {speaker.fake_name}, a {speaker.age}-year-old {speaker.gender}.
Your profile:
- Headline: {speaker.headline}
- About you: {speaker.bio}
- Interests: {', '.join(speaker.interests)}

You're talking to {recipient.fake_name}. Their profile:
- Headline: {recipient.headline}
- About them: {recipient.bio}

Your conversation style: {speaker.conversation_strategy}

Previous conversation:
{conversation_context}

Write your next message. Keep it SHORT (under 100 words). Be authentic, not robotic.
Match the tone of the conversation.

Message:"""

        try:
            response = self.llm.create_message(
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=150
            )
            return response.strip() if response else None
        except Exception as e:
            logger.error(f"LLM error in response: {e}")
            return None

    def _should_conclude(self, message: str) -> bool:
        """Check if message suggests natural conclusion."""

        conclusion_indicators = [
            "see you then", "great!", "awesome", "definitely",
            "can't wait", "looking forward", "talk soon",
            "let's get coffee", "let's grab", "meet up",
            "exchange number", "here's my number", "what's your number",
            "nice talking", "enjoyed talking", "pleasure talking",
        ]

        message_lower = message.lower()

        return any(indicator in message_lower for indicator in conclusion_indicators)


class MockLLMClient:
    """Mock LLM client for testing without API calls."""

    def __init__(self, response_templates: Optional[Dict] = None):
        """
        Initialize mock client.

        Args:
            response_templates: Optional dict mapping strategy to response templates
        """
        self.response_templates = response_templates or self._default_templates()
        self.call_count = 0

    def create_message(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 100
    ) -> str:
        """Return mock response."""

        self.call_count += 1

        # Extract strategy from prompt
        for strategy in ["casual", "direct", "romantic", "playful", "formal"]:
            if strategy in prompt.lower():
                templates = self.response_templates.get(strategy, self.response_templates["casual"])
                return np.random.choice(templates)

        return np.random.choice(self.response_templates["casual"])

    def _default_templates(self) -> Dict[str, List[str]]:
        """Default response templates by strategy."""
        return {
            "casual": [
                "Hey! How's your week going?",
                "What do you like to do for fun?",
                "Nice to match with you!",
                "Haha that's funny, I like that",
            ],
            "direct": [
                "You seem cool, want to grab coffee?",
                "Let's get drinks sometime?",
                "Want to hang out this week?",
            ],
            "romantic": [
                "You seem really interesting, I'd love to know more",
                "Something about your profile caught my attention",
                "You seem like someone special",
            ],
            "playful": [
                "Did it hurt? When you fell from heaven? 😂",
                "Challenge accepted!",
                "That's bold, I like it",
            ],
            "formal": [
                "Pleasure to make your acquaintance",
                "I appreciate your interest",
                "How do you do?",
            ],
        }
