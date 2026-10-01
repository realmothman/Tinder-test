"""
Gender Dynamics Analysis: How does gender affect conversation patterns?

Analyzes:
- Who initiates conversations
- Conversation escalation patterns
- Tone and language differences
- Response patterns by gender
"""

from typing import List, Dict
import numpy as np
import pandas as pd
from collections import Counter
from loguru import logger

from ..simulation.conversation_simulator import Conversation


class GenderDynamicsAnalyzer:
    """Analyze gender patterns in conversations."""

    def __init__(self, conversations: List[Conversation]):
        """Initialize with conversation list."""
        self.conversations = [c for c in conversations if c.completed]
        logger.info(f"Analyzing gender dynamics in {len(self.conversations)} conversations")

    def analyze_initiation_patterns(self) -> Dict:
        """
        Who initiates conversations?

        Returns:
            Statistics on conversation initiation by gender
        """

        results = {}

        # Count initiators by gender
        male_initiators = sum(1 for c in self.conversations if c.user_a.gender == "M")
        female_initiators = sum(1 for c in self.conversations if c.user_a.gender == "F")

        total_convs = len(self.conversations)

        results["male_initiation_rate"] = male_initiators / total_convs if total_convs > 0 else 0
        results["female_initiation_rate"] = female_initiators / total_convs if total_convs > 0 else 0
        results["total_conversations"] = total_convs

        # Analyze by pairing type
        results["pairing_distribution"] = self._analyze_pairing_distribution()

        # Analyze opening strategies by gender
        results["opening_strategies"] = self._analyze_opening_strategies()

        return results

    def analyze_escalation_patterns(self) -> Dict:
        """
        How do conversations escalate?
        - Who suggests meeting
        - Who introduces physical topics
        - Who escalates emotional intimacy
        """

        results = {}

        escalation_data = []

        for conv in self.conversations:
            if len(conv.messages) < 2:
                continue

            # Analyze message progression
            msg_lengths = [m.length for m in conv.messages]
            initiator_lengths = [
                m.length for m in conv.messages if m.sender_id == conv.user_a.safe_id
            ]
            respondent_lengths = [
                m.length for m in conv.messages if m.sender_id == conv.user_b.safe_id
            ]

            escalation_data.append({
                "initiator_gender": conv.user_a.gender,
                "respondent_gender": conv.user_b.gender,
                "num_messages": len(conv.messages),
                "initiator_avg_length": np.mean(initiator_lengths) if initiator_lengths else 0,
                "respondent_avg_length": np.mean(respondent_lengths) if respondent_lengths else 0,
                "engagement_ratio": np.mean(msg_lengths) if msg_lengths else 0,
            })

        escal_df = pd.DataFrame(escalation_data)

        if not escal_df.empty:
            # Overall patterns
            results["avg_messages_by_initiator_gender"] = escal_df.groupby("initiator_gender")["num_messages"].mean().to_dict()

            # Engagement differences
            results["message_length_difference"] = {
                "initiators_longer": (escal_df["initiator_avg_length"].mean() >
                                     escal_df["respondent_avg_length"].mean()),
                "avg_initiator_length": escal_df["initiator_avg_length"].mean(),
                "avg_respondent_length": escal_df["respondent_avg_length"].mean(),
            }

            # By pairing
            for pairing in escal_df["initiator_gender"].unique():
                subset = escal_df[escal_df["initiator_gender"] == pairing]
                results[f"escalation_{pairing}"] = {
                    "avg_messages": subset["num_messages"].mean(),
                    "avg_initiator_length": subset["initiator_avg_length"].mean(),
                    "count": len(subset)
                }

        return results

    def analyze_response_patterns(self) -> Dict:
        """
        How quickly and thoroughly do people respond?
        """

        results = {}

        response_data = []

        for conv in self.conversations:
            messages = conv.messages

            for i in range(1, len(messages)):
                prev_msg = messages[i - 1]
                curr_msg = messages[i]

                # Verify it's actually a response
                if prev_msg.sender_id == curr_msg.sender_id:
                    continue

                response_data.append({
                    "respondent_gender": curr_msg.sender_id.split("_")[1],
                    "message_length": curr_msg.length,
                    "prev_message_length": prev_msg.length,
                    "turn": curr_msg.turn,
                })

        if response_data:
            resp_df = pd.DataFrame(response_data)

            # Response lengths by gender
            results["avg_response_length_by_gender"] = resp_df.groupby("respondent_gender")["message_length"].mean().to_dict()

            # Does response length match initiation length?
            results["reciprocal_engagement"] = {
                "correlation": resp_df["message_length"].corr(resp_df["prev_message_length"]),
                "interpretation": "Positive = people match effort"
            }

            # Response patterns over conversation
            results["engagement_decay"] = self._analyze_engagement_decay(resp_df)

        return results

    def analyze_conversation_outcomes(self) -> Dict:
        """
        Are there gender differences in conversation success/completion?
        """

        results = {}

        outcome_data = []

        for conv in self.conversations:
            outcome_data.append({
                "initiator_gender": conv.user_a.gender,
                "respondent_gender": conv.user_b.gender,
                "num_messages": len(conv.messages),
                "completed": conv.completed,
                "outcome": conv.outcome,
            })

        outcome_df = pd.DataFrame(outcome_data)

        # Success rate by gender pairing
        for g1 in outcome_df["initiator_gender"].unique():
            for g2 in outcome_df["respondent_gender"].unique():
                subset = outcome_df[
                    (outcome_df["initiator_gender"] == g1) &
                    (outcome_df["respondent_gender"] == g2)
                ]

                if len(subset) > 0:
                    results[f"success_{g1}_to_{g2}"] = {
                        "success_rate": subset["completed"].mean(),
                        "avg_messages": subset["num_messages"].mean(),
                        "count": len(subset),
                    }

        return results

    def _analyze_pairing_distribution(self) -> Dict:
        """Count different gender pairings."""

        pairings = Counter()

        for conv in self.conversations:
            key = f"{conv.user_a.gender}_initiates_{conv.user_b.gender}"
            pairings[key] += 1

        total = sum(pairings.values())

        return {
            k: v / total if total > 0 else 0
            for k, v in pairings.items()
        }

    def _analyze_opening_strategies(self) -> Dict:
        """Analyze what opening strategies different genders use."""

        strategy_by_gender = {}

        for conv in self.conversations:
            if not conv.messages:
                continue

            opener = conv.messages[0].text.lower()
            gender = conv.user_a.gender

            # Classify opener
            strategy_type = self._classify_opener(opener)

            if gender not in strategy_by_gender:
                strategy_by_gender[gender] = Counter()

            strategy_by_gender[gender][strategy_type] += 1

        # Convert to proportions
        results = {}
        for gender, strategies in strategy_by_gender.items():
            total = sum(strategies.values())
            results[gender] = {
                s: count / total for s, count in strategies.items()
            }

        return results

    def _classify_opener(self, text: str) -> str:
        """Classify opening message type."""

        if any(word in text for word in ["hey", "hi", "hello", "what's up", "sup"]):
            return "casual_greeting"
        elif any(word in text for word in ["compliment", "beautiful", "handsome", "cute", "attractive"]):
            return "compliment"
        elif any(word in text for word in ["question", "what", "how", "tell me"]):
            return "question"
        elif any(word in text for word in ["meet", "coffee", "drink", "hang"]):
            return "suggest_meeting"
        else:
            return "other"

    def _analyze_engagement_decay(self, resp_df: pd.DataFrame) -> Dict:
        """
        Do conversations lose steam (engagement decay)?
        """

        if "turn" not in resp_df.columns:
            return {}

        early = resp_df[resp_df["turn"] <= 5]["message_length"].mean()
        late = resp_df[resp_df["turn"] > 10]["message_length"].mean()

        if pd.isna(early) or pd.isna(late):
            return {}

        return {
            "early_engagement": early,
            "late_engagement": late,
            "decay_rate": (early - late) / early if early > 0 else 0,
        }

    def generate_summary(self) -> str:
        """Generate text summary of gender findings."""

        initiation = self.analyze_initiation_patterns()
        escalation = self.analyze_escalation_patterns()
        response = self.analyze_response_patterns()
        outcomes = self.analyze_conversation_outcomes()

        summary = f"""
GENDER DYNAMICS ANALYSIS SUMMARY
{'=' * 50}

INITIATION PATTERNS:
  Male initiators: {initiation['male_initiation_rate']:.1%}
  Female initiators: {initiation['female_initiation_rate']:.1%}

GENDER PAIRINGS:
"""
        for pairing, pct in initiation['pairing_distribution'].items():
            summary += f"  {pairing}: {pct:.1%}\n"

        if escalation:
            summary += f"""
ESCALATION:
"""
            for gender, stats in escalation.items():
                if isinstance(stats, dict) and "avg_messages" in stats:
                    summary += f"  {gender}: avg {stats['avg_messages']:.1f} messages\n"

        if response:
            summary += f"""
RESPONSE PATTERNS:
"""
            for gender, length in response.get('avg_response_length_by_gender', {}).items():
                summary += f"  {gender}: avg {length:.0f} chars\n"

        return summary
