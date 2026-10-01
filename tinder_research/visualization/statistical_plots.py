"""
Statistical visualizations for research outputs.

Generates publication-ready figures for academic papers.
"""

from typing import List, Dict, Optional
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger

from ..simulation.conversation_simulator import Conversation
from ..analysis.homophily_analyzer import HomophilyAnalyzer
from ..analysis.gender_dynamics import GenderDynamicsAnalyzer


class StatisticalPlotter:
    """Create publication-ready statistical visualizations."""

    def __init__(
        self,
        conversations: List[Conversation],
        output_dir: Path = Path("outputs/figures"),
        dpi: int = 300,
        style: str = "seaborn-v0_8-darkgrid"
    ):
        """
        Initialize plotter.

        Args:
            conversations: Conversation data to visualize
            output_dir: Where to save figures
            dpi: Resolution for saved figures
            style: Matplotlib style
        """
        self.conversations = conversations
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi

        # Set style
        plt.style.use(style)
        sns.set_palette("husl")

        logger.info(f"Statistical plotter initialized, output to {self.output_dir}")

    def plot_homophily_matrix(self, save_format: str = "pdf") -> Path:
        """
        Plot demographic mixing matrix.

        Shows which demographic groups match together.
        """
        analyzer = HomophilyAnalyzer(self.conversations)
        results = analyzer.analyze_homophily()

        race_matrix = results["race_mixing_matrix"]

        fig, ax = plt.subplots(figsize=(10, 8))

        sns.heatmap(
            race_matrix,
            annot=True,
            fmt=".2f",
            cmap="RdYlGn",
            center=0.5,
            ax=ax,
            cbar_kws={"label": "Match proportion"}
        )

        ax.set_title(
            "Demographic Mixing Matrix: Race\n(Row = initiator, Col = recipient)",
            fontsize=14,
            fontweight="bold"
        )
        ax.set_xlabel("Recipient Race/Ethnicity", fontsize=12)
        ax.set_ylabel("Initiator Race/Ethnicity", fontsize=12)

        plt.tight_layout()

        output_path = self.output_dir / f"01_homophily_matrix.{save_format}"
        plt.savefig(output_path, dpi=self.dpi, format=save_format, bbox_inches="tight")
        plt.close()

        logger.info(f"Saved homophily matrix to {output_path}")
        return output_path

    def plot_homophily_distribution(self, save_format: str = "pdf") -> Path:
        """Plot distribution of homophily coefficients."""

        analyzer = HomophilyAnalyzer(self.conversations)

        similarities = []
        for conv in analyzer.matches:
            sim = analyzer.compute_demographic_similarity(conv.user_a, conv.user_b)
            similarities.append(sim["overall_similarity"])

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.hist(similarities, bins=30, color="steelblue", edgecolor="black", alpha=0.7)
        ax.axvline(np.mean(similarities), color="red", linestyle="--", linewidth=2, label=f"Mean={np.mean(similarities):.3f}")
        ax.axvline(0.5, color="gray", linestyle=":", linewidth=1, label="Random expectation (0.5)")

        ax.set_xlabel("Overall Demographic Similarity", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.set_title("Distribution of Homophily in Actual Matches", fontsize=14, fontweight="bold")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        output_path = self.output_dir / f"02_homophily_distribution.{save_format}"
        plt.savefig(output_path, dpi=self.dpi, format=save_format, bbox_inches="tight")
        plt.close()

        logger.info(f"Saved homophily distribution to {output_path}")
        return output_path

    def plot_gender_dynamics(self, save_format: str = "pdf") -> Path:
        """Plot gender-based differences in conversations."""

        analyzer = GenderDynamicsAnalyzer(self.conversations)
        initiation = analyzer.analyze_initiation_patterns()

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Left: Initiation rates
        genders = ["M", "F"]
        rates = [
            initiation.get("male_initiation_rate", 0),
            initiation.get("female_initiation_rate", 0)
        ]

        colors = ["steelblue", "salmon"]
        axes[0].bar(genders, rates, color=colors, edgecolor="black", alpha=0.7)
        axes[0].set_ylabel("Initiation Rate", fontsize=12)
        axes[0].set_xlabel("Gender", fontsize=12)
        axes[0].set_title("Who Initiates Conversations?", fontsize=12, fontweight="bold")
        axes[0].set_ylim([0, 1])
        axes[0].grid(True, alpha=0.3, axis="y")

        # Add value labels
        for i, (g, r) in enumerate(zip(genders, rates)):
            axes[0].text(i, r + 0.02, f"{r:.1%}", ha="center", fontsize=11, fontweight="bold")

        # Right: Pairing distribution
        pairings = initiation.get("pairing_distribution", {})
        if pairings:
            pairing_names = [k.replace("_initiates_", " → ") for k in pairings.keys()]
            pairing_values = list(pairings.values())

            axes[1].bar(range(len(pairing_values)), pairing_values, color=colors[:len(pairing_values)], edgecolor="black", alpha=0.7)
            axes[1].set_xticks(range(len(pairing_values)))
            axes[1].set_xticklabels(pairing_names, rotation=45, ha="right")
            axes[1].set_ylabel("Proportion", fontsize=12)
            axes[1].set_title("Conversation Pairings by Gender", fontsize=12, fontweight="bold")
            axes[1].grid(True, alpha=0.3, axis="y")

        plt.tight_layout()

        output_path = self.output_dir / f"03_gender_dynamics.{save_format}"
        plt.savefig(output_path, dpi=self.dpi, format=save_format, bbox_inches="tight")
        plt.close()

        logger.info(f"Saved gender dynamics to {output_path}")
        return output_path

    def plot_conversation_length_by_gender(self, save_format: str = "pdf") -> Path:
        """Plot conversation length distribution by gender."""

        data = []

        for conv in self.conversations:
            if not conv.completed:
                continue

            data.append({
                "initiator_gender": conv.user_a.gender,
                "messages": len(conv.messages),
                "chars": conv.total_chars
            })

        if not data:
            logger.warning("No completed conversations to plot")
            return None

        df = pd.DataFrame(data)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Message count by gender
        sns.boxplot(data=df, x="initiator_gender", y="messages", ax=axes[0], palette="Set2")
        axes[0].set_xlabel("Initiator Gender", fontsize=12)
        axes[0].set_ylabel("Number of Messages", fontsize=12)
        axes[0].set_title("Conversation Length by Initiator Gender", fontsize=12, fontweight="bold")
        axes[0].grid(True, alpha=0.3, axis="y")

        # Character count by gender
        sns.boxplot(data=df, x="initiator_gender", y="chars", ax=axes[1], palette="Set2")
        axes[1].set_xlabel("Initiator Gender", fontsize=12)
        axes[1].set_ylabel("Total Characters", fontsize=12)
        axes[1].set_title("Conversation Verbosity by Initiator Gender", fontsize=12, fontweight="bold")
        axes[1].grid(True, alpha=0.3, axis="y")

        plt.tight_layout()

        output_path = self.output_dir / f"04_conversation_length.{save_format}"
        plt.savefig(output_path, dpi=self.dpi, format=save_format, bbox_inches="tight")
        plt.close()

        logger.info(f"Saved conversation length plot to {output_path}")
        return output_path

    def plot_conversation_outcomes(self, save_format: str = "pdf") -> Path:
        """Plot distribution of conversation outcomes."""

        outcomes = {}
        for conv in self.conversations:
            outcome = conv.outcome or "unknown"
            outcomes[outcome] = outcomes.get(outcome, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 6))

        outcome_names = list(outcomes.keys())
        outcome_counts = list(outcomes.values())
        colors = sns.color_palette("husl", len(outcome_names))

        wedges, texts, autotexts = ax.pie(
            outcome_counts,
            labels=outcome_names,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90
        )

        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
            autotext.set_fontsize(10)

        ax.set_title("Distribution of Conversation Outcomes", fontsize=14, fontweight="bold")

        plt.tight_layout()

        output_path = self.output_dir / f"05_conversation_outcomes.{save_format}"
        plt.savefig(output_path, dpi=self.dpi, format=save_format, bbox_inches="tight")
        plt.close()

        logger.info(f"Saved conversation outcomes to {output_path}")
        return output_path

    def generate_all_figures(self) -> List[Path]:
        """Generate all standard visualizations."""

        logger.info("Generating all standard figures...")

        figures = []

        try:
            figures.append(self.plot_homophily_matrix())
        except Exception as e:
            logger.warning(f"Failed to generate homophily matrix: {e}")

        try:
            figures.append(self.plot_homophily_distribution())
        except Exception as e:
            logger.warning(f"Failed to generate homophily distribution: {e}")

        try:
            figures.append(self.plot_gender_dynamics())
        except Exception as e:
            logger.warning(f"Failed to generate gender dynamics: {e}")

        try:
            figures.append(self.plot_conversation_length_by_gender())
        except Exception as e:
            logger.warning(f"Failed to generate conversation length: {e}")

        try:
            figures.append(self.plot_conversation_outcomes())
        except Exception as e:
            logger.warning(f"Failed to generate conversation outcomes: {e}")

        logger.info(f"Generated {len([f for f in figures if f])} figures")

        return [f for f in figures if f]
