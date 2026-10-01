"""
Real Tinder Automation + Anthropological Analysis Pipeline
Integrates: TinderAutomation + AdaptiveOpeningGenerator + Analyzers

Workflow:
1. Login to Tinder (via Selenium)
2. Get match list
3. For each match: generate intelligent opening → send message → collect response
4. Analyze conversation with anthropological frameworks
5. Update adaptive model with learnings
6. Repeat
"""

import json
import time
from typing import List, Dict, Optional
from datetime import datetime
import logging

from tinder_automation import TinderAutomation, TinderMatch, TinderMessage


class RateLimiter:
    """
    Structured rate limiting to respect API/service limits (best practice).
    Prevents ban by respecting message rate limits.
    """

    def __init__(self, actions_per_hour: int = 20, name: str = "RateLimiter"):
        """
        Args:
            actions_per_hour: Max actions allowed per 60 minutes
            name: For logging
        """
        self.max_actions = actions_per_hour
        self.window_seconds = 3600  # 1 hour
        self.action_times = []
        self.name = name
        self.logger = logging.getLogger(name)

    def can_act(self) -> bool:
        """Check if we can perform action without exceeding rate limit."""
        now = time.time()
        # Remove old actions outside window
        self.action_times = [t for t in self.action_times if now - t < self.window_seconds]
        return len(self.action_times) < self.max_actions

    def wait_if_needed(self) -> float:
        """Wait if rate limited. Returns time waited."""
        now = time.time()
        self.action_times = [t for t in self.action_times if now - t < self.window_seconds]

        if len(self.action_times) >= self.max_actions:
            oldest = self.action_times[0]
            sleep_time = self.window_seconds - (now - oldest)
            self.logger.info(
                f"⏰ Rate limit reached ({self.max_actions}/{self.window_seconds}s). "
                f"Waiting {sleep_time:.1f}s..."
            )
            time.sleep(sleep_time)
            return sleep_time
        return 0.0

    def record_action(self):
        """Record that action was performed."""
        self.action_times.append(time.time())
        remaining = self.max_actions - len(self.action_times)
        self.logger.debug(f"Action recorded. {remaining} remaining this hour.")
from tinder_bot_example import (
    Profile, Message, Conversation,
    HomophilyAnalyzer, GenderAnalyzer, CapitalAnalyzer,
    PersonaManager
)
from adaptive_opening_generator import AdaptiveOpeningMessageGenerator
from integrated_bot_system import IntegratedBotSystem


class RealBotSystem:
    """
    Complete production system combining real browser automation with intelligent analysis.

    Usage:
        bot = RealBotSystem(
            my_profile=my_profile,
            historical_conversations=past_data,
            email="your@email.com",
            password="your_password"
        )
        bot.run_once()  # Process one batch of matches
        bot.run_continuous(interval_seconds=3600)  # Run hourly
    """

    def __init__(
        self,
        my_profile: Profile,
        email: str,
        password: str,
        historical_conversations: Optional[List[Dict]] = None,
        headless: bool = True,
        mock_mode: bool = True,  # Default safe: use mock mode
        output_file: str = "real_bot_activity.json"
    ):
        """
        Initialize real automation system.

        Args:
            my_profile: Your Profile (demographics)
            email: Tinder email
            password: Tinder password
            historical_conversations: Past conversations for adaptive learning
            headless: Run browser hidden
            mock_mode: Use mock responses (safe testing)
            output_file: Where to save results
        """
        self.logger = logging.getLogger("RealBotSystem")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self.my_profile = my_profile
        self.email = email
        self.password = password
        self.headless = headless
        self.mock_mode = mock_mode
        self.output_file = output_file

        # Initialize automation
        self.automation = TinderAutomation(
            headless=headless,
            mock_mode=mock_mode
        )

        # Initialize adaptive learning
        self.adaptive_generator = AdaptiveOpeningMessageGenerator(
            historical_conversations or []
        )

        # Initialize integrated analysis system
        self.integrated_system = IntegratedBotSystem(
            my_profile,
            historical_conversations or []
        )

        # Activity log
        self.activity_log = {
            "started_at": datetime.now().isoformat(),
            "total_matches_processed": 0,
            "successful_conversations": 0,
            "failed_conversations": 0,
            "matches": [],
            "errors": []
        }

        self.logged_in = False

    def login(self) -> bool:
        """Login to Tinder."""
        try:
            self.logger.info("🔐 Logging in to Tinder...")
            success = self.automation.login(
                self.email,
                self.password,
                wait_for_2fa=not self.mock_mode
            )
            if success:
                self.logged_in = True
                self.logger.info("✓ Login successful")
            return success
        except Exception as e:
            self.logger.error(f"✗ Login failed: {e}")
            self.activity_log["errors"].append(str(e))
            return False

    def process_match(self, match: TinderMatch) -> Dict:
        """
        Process single match: generate opening → send message → analyze.

        Returns:
            Dict with: opening, success, analysis
        """
        try:
            self.logger.info(f"📌 Processing match: {match.name}")

            # Convert TinderMatch to Profile
            match_profile = Profile(
                name=match.name,
                age=match.age,
                gender="F",  # Assumption: most Tinder usage is M→F
                profession="Unknown",
                bio=match.bio,
                education_level="bachelor",
                location=match.location
            )

            # 1. Generate intelligent opening
            opening_msg, metadata = self.adaptive_generator.generate_opening(
                match_profile
            )
            self.logger.info(f"💬 Opening: {opening_msg}")
            self.logger.info(f"   Confidence: {metadata['confidence']:.0%}")

            # 2. Send message via automation
            if not self.mock_mode:
                self.logger.info("📤 Sending message...")
                success = self.automation.send_message(match.match_id, opening_msg)
                if not success:
                    return {
                        "match_id": match.match_id,
                        "name": match.name,
                        "opening": opening_msg,
                        "sent": False,
                        "success_score": 0.0
                    }
            else:
                self.logger.info("📤 (Mock) Would send message")

            # 3. Wait for response (in real scenario)
            if not self.mock_mode:
                self.logger.info("⏳ Waiting for response (30 seconds)...")
                time.sleep(30)
                conversation = self.automation.get_conversation(match.match_id)
            else:
                # In mock mode, use simulated conversation
                conversation = self.automation._generate_mock_conversation()

            # 4. Use IntegratedBotSystem for full analysis
            result = self.integrated_system.process_new_match(
                match_profile,
                persona='auto'
            )

            success_score = result['success']['success_level']
            success_value = {
                'high': 0.9,
                'medium': 0.6,
                'low': 0.3
            }.get(success_score, 0.0)

            # 5. Log activity
            activity = {
                "match_id": match.match_id,
                "name": match.name,
                "age": match.age,
                "location": match.location,
                "timestamp": datetime.now().isoformat(),
                "opening": opening_msg,
                "opening_confidence": metadata['confidence'],
                "sent": True,
                "got_response": result['success']['got_response'],
                "conversation_turns": result['success']['number_of_turns'],
                "success_score": success_value,
                "analysis": result['analysis'],
                "persona_used": result['persona'],
                "opening_metadata": metadata
            }

            self.activity_log["matches"].append(activity)

            # Update success counters
            if result['success']['got_response']:
                self.activity_log["successful_conversations"] += 1
            else:
                self.activity_log["failed_conversations"] += 1

            self.logger.info(
                f"✓ Processed: {match.name} | "
                f"Success: {success_value:.0%} | "
                f"Homophily: {result['analysis']['homophily_score']:.0%}"
            )

            return activity

        except Exception as e:
            self.logger.error(f"✗ Error processing {match.name}: {e}")
            self.activity_log["errors"].append(f"{match.name}: {str(e)}")
            self.activity_log["failed_conversations"] += 1
            return {
                "match_id": match.match_id,
                "name": match.name,
                "error": str(e),
                "success_score": 0.0
            }

    def run_once(self, limit: int = 5) -> Dict:
        """
        Process one batch of matches.

        Args:
            limit: Max matches to process

        Returns:
            Activity log
        """
        if not self.logged_in:
            if not self.login():
                return self.activity_log

        try:
            self.logger.info(f"📋 Fetching up to {limit} matches...")
            matches = self.automation.get_matches(limit=limit)

            if not matches:
                self.logger.warning("No matches found")
                return self.activity_log

            self.logger.info(f"Found {len(matches)} matches")

            for match in matches:
                self.process_match(match)
                self.activity_log["total_matches_processed"] += 1

                # Rate limiting: random delay between matches
                time.sleep(5)

            self.save_activity()
            self.logger.info(
                f"✓ Batch complete: "
                f"{self.activity_log['successful_conversations']} success, "
                f"{self.activity_log['failed_conversations']} failed"
            )

            return self.activity_log

        except Exception as e:
            self.logger.error(f"✗ Batch failed: {e}")
            self.activity_log["errors"].append(f"Batch: {str(e)}")
            return self.activity_log

    def run_continuous(self, interval_seconds: int = 3600, max_iterations: Optional[int] = None):
        """
        Run continuously at regular intervals.

        Args:
            interval_seconds: Wait between batches (default 1 hour)
            max_iterations: Stop after N iterations (None = infinite)
        """
        iteration = 0
        while max_iterations is None or iteration < max_iterations:
            try:
                self.logger.info(f"🔄 Iteration {iteration + 1}")
                self.run_once(limit=3)
                iteration += 1

                if max_iterations is None or iteration < max_iterations:
                    self.logger.info(f"⏰ Next run in {interval_seconds}s")
                    time.sleep(interval_seconds)

            except KeyboardInterrupt:
                self.logger.info("⏹️  Interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"✗ Iteration failed: {e}")
                self.activity_log["errors"].append(f"Iteration {iteration}: {str(e)}")
                time.sleep(60)  # Wait before retry

        self.close()

    def save_activity(self):
        """Save activity log to file."""
        try:
            with open(self.output_file, 'w') as f:
                json.dump(self.activity_log, f, indent=2)
            self.logger.info(f"💾 Activity saved to {self.output_file}")
        except Exception as e:
            self.logger.error(f"✗ Failed to save activity: {e}")

    def get_analysis_summary(self) -> Dict:
        """Get aggregated analysis of all processed conversations."""
        if not self.activity_log["matches"]:
            return {
                "total_processed": 0,
                "message": "No matches processed yet"
            }

        matches = self.activity_log["matches"]
        successful = [m for m in matches if m.get('got_response', False)]

        # Aggregate homophily scores
        homophily_scores = [
            m['analysis']['homophily_score']
            for m in matches
            if 'analysis' in m and 'homophily_score' in m['analysis']
        ]

        # Aggregate by gender
        by_gender = {}
        for match in matches:
            if 'analysis' in match:
                analysis = match['analysis']
                if 'gender_dynamics' in analysis:
                    for key, val in analysis['gender_dynamics'].items():
                        if key not in by_gender:
                            by_gender[key] = []
                        by_gender[key].append(val)

        return {
            "total_processed": self.activity_log["total_matches_processed"],
            "successful_responses": len(successful),
            "success_rate": len(successful) / len(matches) if matches else 0,
            "avg_homophily_score": sum(homophily_scores) / len(homophily_scores) if homophily_scores else 0,
            "avg_opening_confidence": sum(
                m['opening_confidence'] for m in matches if 'opening_confidence' in m
            ) / len(matches) if matches else 0,
            "gender_dynamics_summary": {k: len(v) for k, v in by_gender.items()},
            "top_successful_topics": self._extract_top_topics(successful),
        }

    def _extract_top_topics(self, matches: List[Dict]) -> List[str]:
        """Extract most common successful topics."""
        topics = []
        for match in matches:
            if 'opening' in match:
                # Simple heuristic: extract words after "curte" or similar
                opening = match['opening'].lower()
                if 'curte' in opening or 'gosta' in opening:
                    # In a real scenario, would use NLP
                    topics.append(opening)
        return topics[:5]

    def close(self):
        """Close browser and save final state."""
        self.logger.info("🔚 Closing system...")
        if self.automation:
            self.automation.close()
        self.save_activity()
        self.logger.info("✓ System closed")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import sys

    print("="*70)
    print("🤖 REAL TINDER BOT + ANALYSIS SYSTEM")
    print("="*70)

    # Your profile
    my_profile = Profile(
        name="Your Name",
        age=28,
        gender="M",
        profession="Software Engineer",
        bio="Exploring tech, sociology, and connections",
        education_level="master",
        location="São Paulo"
    )

    # Historical data (optional, but recommended)
    historical = [
        {
            'messages': [
                {'content': 'Oi! Como vai?'},
                {'content': 'Oi! Tudo bem sim!'}
            ],
            'response_times': [45.0],
            'profile': {
                'name': 'Marina',
                'age': 26,
                'gender': 'F',
                'profession': 'Designer',
                'bio': 'Design, viagens',
                'education_level': 'bachelor',
                'location': 'São Paulo'
            }
        }
    ]

    # Initialize (SAFE MODE: mock_mode=True)
    print("\n⚠️  Starting in MOCK MODE (safe testing, no real connections)")
    bot = RealBotSystem(
        my_profile=my_profile,
        email="your_email@gmail.com",
        password="your_password",
        historical_conversations=historical,
        headless=True,
        mock_mode=True  # IMPORTANT: Set to False only when ready for real automation
    )

    print("\n📝 To use with REAL Tinder:")
    print("  1. Set mock_mode=False")
    print("  2. Provide real email and password")
    print("  3. Understand the risks (ToS violation, potential ban)")
    print("\n⚠️  DISCLAIMER:")
    print("  - This violates Tinder ToS")
    print("  - Use for research/development only")
    print("  - Risk of account ban")
    print("  - Ethical concerns about data collection")
    print("  - Consider synthetic data or mock mode")

    print("\n" + "="*70)
    print("Running mock demonstration...")
    print("="*70)

    # Run one batch in mock mode
    activity = bot.run_once(limit=3)

    print("\n📊 Activity Summary:")
    print(f"  Total processed: {activity['total_matches_processed']}")
    print(f"  Successful: {activity['successful_conversations']}")
    print(f"  Failed: {activity['failed_conversations']}")

    print("\n📈 Analysis Summary:")
    analysis = bot.get_analysis_summary()
    print(f"  Success rate: {analysis['success_rate']:.0%}")
    print(f"  Avg homophily: {analysis['avg_homophily_score']:.0%}")
    print(f"  Avg opening confidence: {analysis['avg_opening_confidence']:.0%}")

    print("\n" + "="*70)
    print(f"✅ Results saved to {bot.output_file}")
    print("="*70)

    bot.close()
