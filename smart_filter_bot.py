"""
Smart Filter Bot: Prioritize Online Matches + Use Only Successful Conversations

Workflow:
1. Filter matches: only those who are ONLINE
2. Filter history: only conversations that WORKED (success_score > 0.6)
3. Generate openings: based ONLY on successful patterns
4. Send messages: to online matches, in order of confidence
"""

import json
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import asdict

from real_bot_system import RealBotSystem
from tinder_automation import TinderMatch, TinderAutomation
from tinder_bot_example import Profile
from adaptive_opening_generator import AdaptiveOpeningMessageGenerator


class SmartFilterBot(RealBotSystem):
    """
    Enhanced RealBotSystem with intelligent filtering:
    - Only targets ONLINE matches
    - Only learns from SUCCESSFUL conversations
    - Prioritizes high-confidence openings
    """

    def __init__(
        self,
        my_profile: Profile,
        email: str,
        password: str,
        historical_conversations: Optional[List[Dict]] = None,
        success_threshold: float = 0.6,  # Only use convos with score > 60%
        headless: bool = True,
        mock_mode: bool = True,
        output_file: str = "smart_bot_activity.json"
    ):
        """
        Initialize with smart filtering.

        Args:
            success_threshold: Min success score to learn from (0-1)
                              0.6 = only conversations that went well
        """
        super().__init__(
            my_profile=my_profile,
            email=email,
            password=password,
            historical_conversations=historical_conversations,
            headless=headless,
            mock_mode=mock_mode,
            output_file=output_file
        )

        self.success_threshold = success_threshold
        self.logger.info(
            f"🎯 Smart mode enabled: only learning from conversations with "
            f"success > {success_threshold:.0%}"
        )

        # Initialize adaptive generator with ONLY successful conversations
        self._init_successful_adapter()

    def _init_successful_adapter(self):
        """Train the opening generator only on conversations that worked."""
        history = self.historical_conversations
        successful = self._filter_successful_conversations(history)
        self.logger.info(
            f"📚 Using {len(successful)}/{len(history)} successful conversations as templates"
        )
        self.adaptive_generator = AdaptiveOpeningMessageGenerator(successful)

    def _filter_successful_conversations(
        self,
        conversations: List[Dict]
    ) -> List[Dict]:
        """
        Filter to keep ONLY conversations that went well.

        Success criteria:
        - Got response
        - Conversation length > 2 turns
        - (If available) success_score > threshold
        """
        successful = []

        for conv in conversations:
            # Skip if no response
            if not conv.get('success', {}).get('got_response', False):
                continue

            # Check conversation length
            num_turns = conv.get('success', {}).get('number_of_turns', 0)
            if num_turns < 2:
                continue

            # If we have explicit score, check it
            success_score = conv.get('success_score', 0.5)
            if success_score < self.success_threshold:
                continue

            # This one counts!
            successful.append(conv)

        return successful

    def filter_online_matches(
        self,
        matches: List[TinderMatch]
    ) -> Tuple[List[TinderMatch], int]:
        """
        Filter matches: keep only ONLINE ones.

        Returns:
            (online_matches, total_found)
        """
        online = [m for m in matches if m.is_online]

        self.logger.info(
            f"🟢 Online matches: {len(online)}/{len(matches)}"
        )
        return online, len(matches)

    def process_smart_batch(self, limit: int = 5) -> Dict:
        """
        Smart batch processing:
        1. Get all matches
        2. Filter to ONLINE only
        3. Process with high-confidence openings only
        """
        if not self.logged_in:
            if not self.login():
                return self.activity_log

        try:
            self.logger.info(f"📋 Fetching matches...")
            all_matches = self.automation.get_matches(limit=limit * 2)

            if not all_matches:
                self.logger.warning("No matches found")
                return self.activity_log

            # STEP 1: Filter to online only
            online_matches, total = self.filter_online_matches(all_matches)

            if not online_matches:
                self.logger.warning("❌ No online matches right now")
                return self.activity_log

            # STEP 2: Sort by confidence (highest first)
            online_with_confidence = []
            for match in online_matches[:limit]:
                _, metadata = self.adaptive_generator.generate_opening(
                    asdict(self._tinder_match_to_profile(match))
                )
                online_with_confidence.append((match, metadata['confidence']))

            # Sort by confidence descending
            online_with_confidence.sort(key=lambda x: x[1], reverse=True)

            self.logger.info(
                f"🎯 Processing {len(online_with_confidence)} online matches "
                f"(sorted by opening confidence)"
            )

            # STEP 3: Process only high-confidence matches
            for match, confidence in online_with_confidence:
                if confidence < 0.5:
                    self.logger.info(
                        f"⏭️  Skipping {match.name} (confidence: {confidence:.0%} < 50%)"
                    )
                    continue

                self.logger.info(
                    f"✅ {match.name} | Confidence: {confidence:.0%}"
                )
                result = self.process_match(match)
                self.activity_log["total_matches_processed"] += 1

            self.save_activity()
            return self.activity_log

        except Exception as e:
            self.logger.error(f"✗ Smart batch failed: {e}")
            self.activity_log["errors"].append(str(e))
            return self.activity_log

    def _tinder_match_to_profile(self, match: TinderMatch) -> Profile:
        """Convert TinderMatch to Profile for analysis."""
        return Profile(
            name=match.name,
            age=match.age,
            gender="F",
            profession="Unknown",
            bio=match.bio,
            education_level="bachelor",
            location=match.location
        )

    def get_smart_summary(self) -> Dict:
        """Summarize how the filters performed."""
        summary = self.get_analysis_summary()
        summary.update({
            "success_threshold": self.success_threshold,
            "historical_total": len(self.historical_conversations),
            "successful_only": len(self._filter_successful_conversations(self.historical_conversations)),
        })
        return summary

    def auto_run_smart(self, interval_seconds: int = 600, max_iterations: Optional[int] = None):
        """
        Smart continuous run: every N seconds, message online people.

        Args:
            interval_seconds: Wait between batches (default 10 min)
            max_iterations: Max runs (None = infinite)
        """
        iteration = 0
        while max_iterations is None or iteration < max_iterations:
            try:
                self.logger.info(f"\n{'='*70}")
                self.logger.info(f"🔄 Smart Run #{iteration + 1} - {datetime.now().strftime('%H:%M:%S')}")
                self.logger.info(f"{'='*70}")

                self.process_smart_batch(limit=3)

                summary = self.get_smart_summary()
                self.logger.info(f"\n📊 Summary:")
                self.logger.info(f"  Success threshold: {summary['success_threshold']:.0%}")
                self.logger.info(f"  Using {summary['successful_only']}/{summary['historical_total']} successful convos")
                self.logger.info(f"  Messages sent this run: {self.activity_log['total_matches_processed']}")
                self.logger.info(f"  Overall success: {summary['success_rate']:.0%}")

                iteration += 1
                if max_iterations is None or iteration < max_iterations:
                    self.logger.info(f"\n⏰ Next run in {interval_seconds}s...")
                    time.sleep(interval_seconds)

            except KeyboardInterrupt:
                self.logger.info("\n⏹️  Stopped by user")
                break
            except Exception as e:
                self.logger.error(f"✗ Run failed: {e}")
                time.sleep(30)

        self.close()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import time

    print("="*70)
    print("🎯 SMART FILTER BOT - Only Online + Only Successful Patterns")
    print("="*70)

    # Your profile
    my_profile = Profile(
        name="You",
        age=28,
        gender="M",
        profession="Dev",
        bio="Learning patterns",
        education_level="master",
        location="São Paulo"
    )

    # IMPORTANT: Historical conversations from YOUR real experience
    # Only conversations that WORKED (got responses, lasted 3+ messages)
    successful_history = [
        {
            'messages': [
                {'content': 'Oi! Como vai?'},
                {'content': 'Oi! Tudo bem!'},
                {'content': 'Que legal! Você curte design?'},
                {'content': 'Adorooo!'}
            ],
            'response_times': [45.0, 30.0, 25.0],
            'success_score': 0.8,  # This one worked great!
            'success': {
                'got_response': True,
                'number_of_turns': 3,
                'success_level': 'high'
            },
            'profile': {
                'name': 'Ana',
                'age': 26,
                'gender': 'F',
                'profession': 'Designer',
                'bio': 'Design, viagens, arte',
                'education_level': 'bachelor',
                'location': 'São Paulo'
            }
        }
    ]

    print("\n⚙️  Mode: MOCK (safe testing)")
    print(f"📚 Using {len(successful_history)} successful conversation(s) as template")
    print("🟢 Will target ONLINE matches only")
    print("💡 Will use ONLY patterns from successful convos")

    # Initialize SMART bot
    bot = SmartFilterBot(
        my_profile=my_profile,
        email="your@email.com",
        password="your_password",
        historical_conversations=successful_history,
        success_threshold=0.6,  # Only convos with 60%+ success
        mock_mode=True  # SAFE
    )

    print("\n" + "="*70)
    print("Running smart batch...")
    print("="*70)

    # Single batch
    activity = bot.process_smart_batch(limit=3)

    print("\n" + "="*70)
    print("📊 Results:")
    print("="*70)
    summary = bot.get_smart_summary()
    print(json.dumps(summary, indent=2))

    print("\n" + "="*70)
    print("✅ Smart filtering demo complete!")
    print("="*70)

    print("\n💡 To run continuously (every 10 minutes):")
    print("  bot.auto_run_smart(interval_seconds=600, max_iterations=10)")

    bot.close()
