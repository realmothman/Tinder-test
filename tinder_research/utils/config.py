"""
Configuration management for research experiments.

All hyperparameters, data paths, and settings centralized here.
"""

from pathlib import Path
from typing import Optional
import yaml
import os
from pydantic import BaseSettings, Field


class Config(BaseSettings):
    """Main configuration object for research framework."""

    # Project paths
    project_root: Path = Field(default=Path(__file__).parent.parent.parent)
    data_dir: Path = Field(default=Path("data"))
    output_dir: Path = Field(default=Path("outputs"))
    logs_dir: Path = Field(default=Path("logs"))

    # Ethics & validation
    enforce_synthetic_only: bool = Field(
        default=True,
        description="Block real API credentials to ensure synthetic-only research"
    )
    require_ethics_approval: bool = Field(
        default=True,
        description="Require documentation of ethical approval before running"
    )

    # LLM Configuration
    llm_provider: str = Field(
        default="openai",
        description="LLM provider: 'openai' or 'anthropic'"
    )
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key (from env)"
    )
    openai_model: str = Field(
        default="gpt-4",
        description="OpenAI model to use"
    )
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key (from env)"
    )
    anthropic_model: str = Field(
        default="claude-3-sonnet-20240229",
        description="Anthropic model to use"
    )
    temperature: float = Field(
        default=0.7,
        description="Temperature for LLM sampling"
    )

    # Synthetic User Generation
    num_users: int = Field(
        default=100,
        description="Number of synthetic users to generate"
    )
    demographics: dict = Field(
        default_factory=lambda: {
            "gender_split": {"M": 0.5, "F": 0.5, "NB": 0.0},
            "age_mean": 28,
            "age_std": 5,
            "age_min": 22,
            "age_max": 50,
            "race_distribution": {
                "white": 0.65,
                "black": 0.13,
                "hispanic": 0.19,
                "asian": 0.06,
                "other": 0.04
            },
            "education_distribution": {
                "high_school": 0.20,
                "bachelor": 0.45,
                "master": 0.25,
                "phd": 0.10
            }
        }
    )

    # Matching & Conversation
    num_conversations: int = Field(
        default=1000,
        description="Number of conversations to simulate"
    )
    max_turns_per_conversation: int = Field(
        default=25,
        description="Max back-and-forth messages"
    )
    homophily_strength: float = Field(
        default=0.6,
        description="How much users prefer similar demographics (0-1)"
    )
    strategies: list = Field(
        default_factory=lambda: ["casual", "direct", "romantic", "playful"],
        description="Conversation strategies to test"
    )

    # Analysis settings
    disaggregate_by: list = Field(
        default_factory=lambda: ["gender", "race", "age_group", "education"],
        description="Dimensions to disaggregate analyses"
    )

    # Fairness & Ethics
    fairness_metrics: list = Field(
        default_factory=lambda: [
            "demographic_parity",
            "equalized_odds",
            "calibration"
        ],
        description="Fairness metrics to compute"
    )

    # Output & Reporting
    generate_figures: bool = Field(
        default=True,
        description="Generate visualization outputs"
    )
    generate_tables: bool = Field(
        default=True,
        description="Generate summary statistics tables"
    )
    figure_format: str = Field(
        default="pdf",
        description="Figure output format (pdf, png, svg)"
    )

    # Reproducibility
    random_seed: int = Field(
        default=42,
        description="Random seed for reproducibility"
    )
    verbose: int = Field(
        default=1,
        description="Verbosity level (0-2)"
    )

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def validate_synthetic_mode(self) -> bool:
        """Verify no real API credentials are being used."""
        if not self.enforce_synthetic_only:
            return True

        # Check for real Tinder credentials
        if os.getenv("TINDER_TOKEN"):
            raise ValueError(
                "ERROR: Real Tinder credentials detected. "
                "This tool is for synthetic research only. "
                "Remove TINDER_TOKEN from environment."
            )

        if os.getenv("TINDER_API_KEY"):
            raise ValueError(
                "ERROR: Real Tinder API key detected. "
                "This tool is for synthetic research only. "
                "Remove TINDER_API_KEY from environment."
            )

        return True

    def load_from_yaml(self, path: Path) -> None:
        """Load configuration from YAML file."""
        with open(path, "r") as f:
            config_dict = yaml.safe_load(f)

        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save_to_yaml(self, path: Path) -> None:
        """Save configuration to YAML for reproducibility."""
        with open(path, "w") as f:
            yaml.dump(self.dict(), f, default_flow_style=False)


# Global config instance
_global_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance."""
    global _global_config
    if _global_config is None:
        _global_config = Config()
        _global_config.validate_synthetic_mode()
    return _global_config


def set_config(config: Config) -> None:
    """Set global configuration instance."""
    global _global_config
    _global_config = config
    _global_config.validate_synthetic_mode()
