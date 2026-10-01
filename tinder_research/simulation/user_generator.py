"""
Synthetic user profile generation for research.

Generates realistic synthetic dating app users with:
- Demographic attributes (age, gender, race, education)
- Personality traits (Big Five)
- Profile text (generated)
- Homophily preferences
- Erotic capital scores
"""

import uuid
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import numpy as np
from faker import Faker
import hashlib
from loguru import logger


@dataclass
class UserProfile:
    """Synthetic user profile."""

    # Identity (hashed, not personally identifiable)
    id: str
    fake_name: str  # Generated name, not real

    # Demographics
    age: int
    gender: str  # "M", "F", "NB"
    race_ethnicity: str
    education: str
    occupation: str

    # Profile text (synthetically generated)
    headline: str
    bio: str
    interests: List[str]

    # Latent attributes
    erotic_capital_score: float  # 0-10, physical attractiveness claim strength

    # Personality (Big Five)
    openness: float
    extraversion: float
    agreeableness: float
    conscientiousness: float
    neuroticism: float

    # Homophily preferences
    age_preference_min: int
    age_preference_max: int
    race_preference_weights: Dict[str, float]  # by race
    education_preference: float  # how much they prefer similar education
    class_preference: float  # how much they prefer similar socioeconomic

    # Conversation behavior
    conversation_strategy: str  # "casual", "direct", "romantic", "playful", "formal"
    response_threshold: float  # 0-1, how responsive they are
    escalation_tendency: float  # 0-1, how quickly they escalate

    @property
    def safe_id(self) -> str:
        """Return safely anonymized ID."""
        return f"user_{self.id[:8]}_synthetic"

    def to_dict(self) -> Dict:
        """Convert to dictionary, excluding potentially identifying info."""
        data = asdict(self)
        data['id'] = self.safe_id
        return data


class UserGenerator:
    """Generate synthetic user profiles."""

    # Define interest categories
    INTEREST_CATEGORIES = {
        "outdoors": ["hiking", "camping", "beach", "parks", "sports"],
        "cultural": ["art", "museums", "music", "theater", "books"],
        "social": ["travel", "parties", "restaurants", "nightlife", "festivals"],
        "wellness": ["yoga", "fitness", "meditation", "nutrition", "health"],
        "tech": ["coding", "gaming", "sci-fi", "tech", "ai"],
        "creative": ["photography", "painting", "writing", "music", "design"],
    }

    OCCUPATIONS = [
        "Software Engineer", "Data Scientist", "Product Manager",
        "UX Designer", "Lawyer", "Doctor", "Nurse", "Teacher",
        "Accountant", "Consultant", "Entrepreneur", "Artist",
        "Musician", "Writer", "Photographer", "Marketer",
        "Sales", "HR Manager", "Project Manager", "Analyst",
    ]

    HEADLINES = [
        "Love {interest1} and {interest2}",
        "Let's {activity} together",
        "{personality} person looking for {goal}",
        "{interest1} enthusiast",
        "Honest and direct",
        "Life's too short for BS",
        "Looking for real connection",
        "Adventure seeker",
        "Work hard, play hard",
        "{hobby} on weekends",
    ]

    def __init__(self, seed: int = 42):
        """Initialize generator with reproducible randomness."""
        np.random.seed(seed)
        self.faker = Faker()
        Faker.seed(seed)

    def generate_users(
        self,
        num_users: int,
        demographics_config: Dict
    ) -> List[UserProfile]:
        """
        Generate synthetic users.

        Args:
            num_users: Number of users to generate
            demographics_config: Configuration for demographic distribution

        Returns:
            List of UserProfile objects
        """
        logger.info(f"Generating {num_users} synthetic users")

        users = []
        for i in range(num_users):
            user = self._generate_single_user(i, demographics_config)
            users.append(user)

            if (i + 1) % 100 == 0:
                logger.debug(f"Generated {i + 1}/{num_users} users")

        logger.info(f"Generated {num_users} synthetic users successfully")
        return users

    def _generate_single_user(
        self,
        user_idx: int,
        config: Dict
    ) -> UserProfile:
        """Generate a single synthetic user."""

        # Deterministic ID based on index (allows reproduction)
        user_id = hashlib.md5(f"user_{user_idx}".encode()).hexdigest()

        # Demographics
        gender = self._sample_gender(config)
        age = self._sample_age(config)
        race = self._sample_race(config)
        education = self._sample_education(config)
        occupation = np.random.choice(self.OCCUPATIONS)

        # Personality traits
        personality = self._sample_personality()

        # Erotic capital: varies by gender, somewhat by personality
        erotic_capital = self._sample_erotic_capital(gender, personality)

        # Generate profile text
        interests = self._sample_interests()
        headline = self._generate_headline(gender, interests)
        bio = self._generate_bio(gender, education, occupation, personality)

        # Homophily preferences (prefer similar demographics)
        race_prefs = self._generate_race_preferences(race)
        age_pref_min = age - np.random.randint(3, 7)
        age_pref_max = age + np.random.randint(3, 7)

        # Conversation behavior
        strategy = np.random.choice([
            "casual", "direct", "romantic", "playful", "formal"
        ], p=[0.3, 0.2, 0.25, 0.15, 0.1])

        return UserProfile(
            id=user_id,
            fake_name=self.faker.name(),
            age=age,
            gender=gender,
            race_ethnicity=race,
            education=education,
            occupation=occupation,
            headline=headline,
            bio=bio,
            interests=interests,
            erotic_capital_score=erotic_capital,
            openness=personality["openness"],
            extraversion=personality["extraversion"],
            agreeableness=personality["agreeableness"],
            conscientiousness=personality["conscientiousness"],
            neuroticism=personality["neuroticism"],
            age_preference_min=age_pref_min,
            age_preference_max=age_pref_max,
            race_preference_weights=race_prefs,
            education_preference=np.random.uniform(0.3, 0.9),
            class_preference=np.random.uniform(0.2, 0.8),
            conversation_strategy=strategy,
            response_threshold=np.random.uniform(0.3, 0.95),
            escalation_tendency=np.random.uniform(0.0, 1.0),
        )

    def _sample_gender(self, config: Dict) -> str:
        """Sample gender from configured distribution."""
        gender_dist = config.get("gender_split", {"M": 0.5, "F": 0.5})
        return np.random.choice(
            list(gender_dist.keys()),
            p=list(gender_dist.values())
        )

    def _sample_age(self, config: Dict) -> int:
        """Sample age from normal distribution."""
        age_mean = config.get("age_mean", 28)
        age_std = config.get("age_std", 5)
        age_min = config.get("age_min", 22)
        age_max = config.get("age_max", 50)

        age = int(np.random.normal(age_mean, age_std))
        return np.clip(age, age_min, age_max)

    def _sample_race(self, config: Dict) -> str:
        """Sample race from configured distribution."""
        race_dist = config.get("race_distribution", {
            "white": 0.65,
            "black": 0.13,
            "hispanic": 0.19,
            "asian": 0.06,
            "other": 0.04
        })
        return np.random.choice(
            list(race_dist.keys()),
            p=list(race_dist.values())
        )

    def _sample_education(self, config: Dict) -> str:
        """Sample education level."""
        edu_dist = config.get("education_distribution", {
            "high_school": 0.20,
            "bachelor": 0.45,
            "master": 0.25,
            "phd": 0.10
        })
        return np.random.choice(
            list(edu_dist.keys()),
            p=list(edu_dist.values())
        )

    def _sample_personality(self) -> Dict[str, float]:
        """Sample Big Five personality traits."""
        return {
            "openness": np.random.uniform(0, 1),
            "extraversion": np.random.uniform(0, 1),
            "agreeableness": np.random.uniform(0, 1),
            "conscientiousness": np.random.uniform(0, 1),
            "neuroticism": np.random.uniform(0, 1),
        }

    def _sample_erotic_capital(self, gender: str, personality: Dict) -> float:
        """
        Sample erotic capital (attractiveness claims in profile).

        Varies by:
        - Gender (some cultural differences in how attractiveness is discussed)
        - Extraversion (more extraverted people might claim more)
        - Base randomness
        """
        base = np.random.uniform(2, 8)

        # Gender effect (cultural signal)
        if gender == "F":
            base += np.random.normal(0.5, 0.3)  # Women slightly higher on average

        # Extraversion effect
        base += personality["extraversion"] * 2

        # Neuroticism effect (insecure people might overstate)
        base += personality["neuroticism"] * 1

        return np.clip(base, 0, 10)

    def _sample_interests(self) -> List[str]:
        """Sample 3-5 interests from categories."""
        num_interests = np.random.randint(3, 6)
        selected = []

        for _ in range(num_interests):
            category = np.random.choice(list(self.INTEREST_CATEGORIES.keys()))
            interest = np.random.choice(self.INTEREST_CATEGORIES[category])
            selected.append(interest)

        return list(set(selected))  # Remove duplicates

    def _generate_headline(self, gender: str, interests: List[str]) -> str:
        """Generate profile headline."""
        interests_sample = interests[:2] if interests else ["adventure"]

        template = np.random.choice(self.HEADLINES)
        return template.format(
            interest1=interests_sample[0],
            interest2=interests_sample[1] if len(interests_sample) > 1 else "life",
            activity=np.random.choice(["hike", "travel", "explore", "create"]),
            personality=np.random.choice(["Fun", "Honest", "Adventurous", "Creative"]),
            goal=np.random.choice(["something real", "new friends", "adventure", "connection"]),
            hobby=interests_sample[0],
        )

    def _generate_bio(
        self,
        gender: str,
        education: str,
        occupation: str,
        personality: Dict
    ) -> str:
        """Generate profile bio."""

        # Base sentences
        occupation_sentence = f"I work as a {occupation}."

        interests_val = ["loves", "enjoys", "am into"][np.random.randint(0, 3)]
        interest_sentence = f"I {interests_val} spending time outdoors and meeting new people."

        # Add personality flavor
        if personality["openness"] > 0.7:
            personality_sentence = "Open to new experiences and perspectives."
        elif personality["extraversion"] > 0.7:
            personality_sentence = "Social butterfly, always up for an adventure."
        elif personality["conscientiousness"] > 0.7:
            personality_sentence = "Believe in honesty and genuine connections."
        else:
            personality_sentence = "Looking for something real."

        return f"{occupation_sentence} {interest_sentence} {personality_sentence}"

    def _generate_race_preferences(self, user_race: str) -> Dict[str, float]:
        """
        Generate race preferences, incorporating homophily.

        Higher weight for own race (homophily effect),
        but realistic variability.
        """
        races = ["white", "black", "hispanic", "asian", "other"]

        # Start with baseline preference for own race (homophily)
        homophily_strength = np.random.uniform(0.3, 0.8)

        # Initialize weights
        weights = {}
        for race in races:
            if race == user_race:
                # Prefer own race (homophily)
                weights[race] = 0.5 + homophily_strength * 0.3
            else:
                # Equal distribution for others
                weights[race] = (0.5 - weights.get(user_race, 0)) / (len(races) - 1)

        # Normalize
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}

        return weights
