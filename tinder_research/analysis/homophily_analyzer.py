"""
Homophily Analysis: Do similar users match together?

Tests whether users preferentially match with others similar to themselves
on demographic dimensions (age, race, education, etc).
"""

from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
from scipy import stats
from loguru import logger

from ..simulation.conversation_simulator import Conversation
from ..simulation.user_generator import UserProfile


class HomophilyAnalyzer:
    """Analyze homophily patterns in matching and conversations."""

    def __init__(self, conversations: List[Conversation]):
        """
        Initialize analyzer.

        Args:
            conversations: List of completed conversations
        """
        self.conversations = conversations
        self.matches = [c for c in conversations if c.completed]

        logger.info(f"Analyzing homophily in {len(self.matches)} matches")

    def compute_demographic_similarity(
        self,
        user_a: UserProfile,
        user_b: UserProfile
    ) -> Dict[str, float]:
        """
        Compute similarity scores across demographics.

        Returns:
            Dict with similarity for each demographic dimension
        """

        # Age similarity (normalized to 0-1)
        age_diff = abs(user_a.age - user_b.age)
        age_similarity = 1.0 - (age_diff / 30)  # Normalized over max age diff

        # Gender match
        gender_match = 1.0 if user_a.gender == user_b.gender else 0.0

        # Race match
        race_match = 1.0 if user_a.race_ethnicity == user_b.race_ethnicity else 0.0

        # Education match
        education_levels = ["high_school", "bachelor", "master", "phd"]
        if user_a.education in education_levels and user_b.education in education_levels:
            edu_diff = abs(
                education_levels.index(user_a.education) -
                education_levels.index(user_b.education)
            )
            education_similarity = 1.0 - (edu_diff / len(education_levels))
        else:
            education_similarity = 0.5

        return {
            "age_similarity": age_similarity,
            "gender_match": gender_match,
            "race_match": race_match,
            "education_similarity": education_similarity,
            "overall_similarity": np.mean([
                age_similarity, gender_match, race_match, education_similarity
            ])
        }

    def analyze_homophily(self) -> Dict:
        """
        Comprehensive homophily analysis.

        Returns:
            Results including homophily coefficients, matrices, etc.
        """

        results = {}

        # Compute similarities for all matches
        similarities = []
        for conv in self.matches:
            sim = self.compute_demographic_similarity(conv.user_a, conv.user_b)
            similarities.append(sim)

        # Convert to DataFrame for analysis
        sim_df = pd.DataFrame(similarities)

        # Overall homophily coefficient
        results["overall_homophily_coeff"] = sim_df["overall_similarity"].mean()
        results["homophily_std"] = sim_df["overall_similarity"].std()

        # By demographic dimension
        results["homophily_by_dimension"] = {
            "age": sim_df["age_similarity"].mean(),
            "gender": sim_df["gender_match"].mean(),
            "race": sim_df["race_match"].mean(),
            "education": sim_df["education_similarity"].mean(),
        }

        logger.info(f"Overall homophily coefficient: {results['overall_homophily_coeff']:.3f}")

        # Build demographic mixing matrix
        results["race_mixing_matrix"] = self._build_mixing_matrix(
            "race_ethnicity"
        )
        results["gender_mixing_matrix"] = self._build_mixing_matrix("gender")

        # Homophily by group
        results["homophily_by_group"] = self._analyze_homophily_by_group()

        # Statistical test: Is homophily significant?
        results["homophily_significance"] = self._test_homophily_significance()

        return results

    def _build_mixing_matrix(self, attribute: str) -> pd.DataFrame:
        """
        Build demographic mixing matrix.

        Shows proportion of matches between each demographic group.
        """

        # Get all attribute values
        values = set()
        for conv in self.matches:
            values.add(getattr(conv.user_a, attribute))
            values.add(getattr(conv.user_b, attribute))

        values = sorted(list(values))

        # Initialize matrix
        matrix = pd.DataFrame(
            0,
            index=values,
            columns=values
        )

        # Fill matrix
        for conv in self.matches:
            val_a = getattr(conv.user_a, attribute)
            val_b = getattr(conv.user_b, attribute)
            matrix.loc[val_a, val_b] += 1

        # Normalize by row (proportion of each group's matches)
        matrix = matrix.div(matrix.sum(axis=1), axis=0)

        return matrix

    def _analyze_homophily_by_group(self) -> Dict[str, float]:
        """
        Analyze homophily separately for each demographic group.
        """

        results = {}

        # By gender
        for gender in ["M", "F"]:
            gender_convs = [
                c for c in self.matches
                if c.user_a.gender == gender or c.user_b.gender == gender
            ]

            if gender_convs:
                similarities = [
                    self.compute_demographic_similarity(c.user_a, c.user_b)["overall_similarity"]
                    for c in gender_convs
                ]
                results[f"homophily_{gender}"] = np.mean(similarities)

        # By race
        for race in ["white", "black", "hispanic", "asian"]:
            race_convs = [
                c for c in self.matches
                if c.user_a.race_ethnicity == race or c.user_b.race_ethnicity == race
            ]

            if race_convs:
                similarities = [
                    self.compute_demographic_similarity(c.user_a, c.user_b)["overall_similarity"]
                    for c in race_convs
                ]
                results[f"homophily_{race}"] = np.mean(similarities)

        return results

    def _test_homophily_significance(self) -> Dict:
        """
        Statistical test: Is observed homophily significantly different from random?
        """

        observed_similarities = []
        for conv in self.matches:
            sim = self.compute_demographic_similarity(conv.user_a, conv.user_b)
            observed_similarities.append(sim["overall_similarity"])

        observed_mean = np.mean(observed_similarities)

        # Random baseline: Simulate random matching
        n_perms = 1000
        random_similarities = []

        all_users = [c.user_a for c in self.matches] + [c.user_b for c in self.matches]

        for _ in range(n_perms):
            # Random pairing
            shuffled = all_users.copy()
            np.random.shuffle(shuffled)

            pairs_sim = []
            for i in range(0, len(shuffled) - 1, 2):
                sim = self.compute_demographic_similarity(shuffled[i], shuffled[i + 1])
                pairs_sim.append(sim["overall_similarity"])

            random_similarities.append(np.mean(pairs_sim))

        # Compute p-value
        p_value = np.mean(np.array(random_similarities) >= observed_mean)

        return {
            "observed_mean": observed_mean,
            "random_mean": np.mean(random_similarities),
            "p_value": p_value,
            "significant": p_value < 0.05
        }

    def analyze_preference_satisfaction(self) -> Dict:
        """
        Do users match within their stated preferences?
        """

        within_pref = []

        for conv in self.matches:
            # Check if user_b is within user_a's preferences
            a_satisfied = (
                conv.user_b.age >= conv.user_a.age_preference_min and
                conv.user_b.age <= conv.user_a.age_preference_max and
                conv.user_a.race_preference_weights.get(conv.user_b.race_ethnicity, 0) > 0.1
            )

            # Check if user_a is within user_b's preferences
            b_satisfied = (
                conv.user_a.age >= conv.user_b.age_preference_min and
                conv.user_a.age <= conv.user_b.age_preference_max and
                conv.user_b.race_preference_weights.get(conv.user_a.race_ethnicity, 0) > 0.1
            )

            within_pref.append({
                "user_a_satisfied": a_satisfied,
                "user_b_satisfied": b_satisfied,
                "mutual_satisfaction": a_satisfied and b_satisfied
            })

        pref_df = pd.DataFrame(within_pref)

        return {
            "prop_a_satisfied": pref_df["user_a_satisfied"].mean(),
            "prop_b_satisfied": pref_df["user_b_satisfied"].mean(),
            "prop_mutual_satisfied": pref_df["mutual_satisfaction"].mean(),
        }

    def generate_summary(self) -> str:
        """Generate text summary of homophily findings."""

        analysis = self.analyze_homophily()
        preferences = self.analyze_preference_satisfaction()

        summary = f"""
HOMOPHILY ANALYSIS SUMMARY
{'=' * 50}

Overall Homophily Coefficient: {analysis['overall_homophily_coeff']:.3f}
(Scale: 0 = no homophily, 1 = perfect homophily)

Homophily by Demographic:
  - Age: {analysis['homophily_by_dimension']['age']:.3f}
  - Gender: {analysis['homophily_by_dimension']['gender']:.3f}
  - Race: {analysis['homophily_by_dimension']['race']:.3f}
  - Education: {analysis['homophily_by_dimension']['education']:.3f}

Preference Satisfaction:
  - User A satisfied: {preferences['prop_a_satisfied']:.1%}
  - User B satisfied: {preferences['prop_b_satisfied']:.1%}
  - Mutual satisfaction: {preferences['prop_mutual_satisfied']:.1%}

Significance Test:
  - Observed similarity: {analysis['homophily_significance']['observed_mean']:.3f}
  - Random baseline: {analysis['homophily_significance']['random_mean']:.3f}
  - P-value: {analysis['homophily_significance']['p_value']:.3f}
  - Significant: {analysis['homophily_significance']['significant']}
"""

        return summary
