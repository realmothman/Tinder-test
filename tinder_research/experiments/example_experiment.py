"""
Example Experiment: Homophily and Gender Dynamics in Dating Conversations

This script demonstrates the full research workflow:
1. Generate synthetic users
2. Simulate conversations
3. Analyze patterns
4. Generate outputs

Run: python -m tinder_research.experiments.example_experiment
"""

import os
from pathlib import Path
import json
import numpy as np
from loguru import logger

from ..simulation.user_generator import UserGenerator
from ..simulation.conversation_simulator import ConversationSimulator, MockLLMClient
from ..analysis.homophily_analyzer import HomophilyAnalyzer
from ..analysis.gender_dynamics import GenderDynamicsAnalyzer
from ..utils.config import get_config


def run_experiment():
    """Run complete example experiment."""

    # Configuration
    config = get_config()

    logger.info("=" * 60)
    logger.info("DATING APP CONVERSATION RESEARCH - EXAMPLE EXPERIMENT")
    logger.info("=" * 60)
    logger.info(f"Configuration: {config.num_users} users, {config.num_conversations} conversations")
    logger.info(f"Random seed: {config.random_seed}")

    # Create output directories
    output_dir = Path("outputs") / "example_experiment"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ====== PHASE 1: Generate Synthetic Users ======
    logger.info("\n[PHASE 1] Generating synthetic users...")

    generator = UserGenerator(seed=config.random_seed)
    users = generator.generate_users(
        num_users=config.num_users,
        demographics_config=config.demographics
    )

    logger.info(f"✓ Generated {len(users)} synthetic users")

    # Save user statistics
    user_stats = {
        "total_users": len(users),
        "gender_distribution": {
            "M": sum(1 for u in users if u.gender == "M") / len(users),
            "F": sum(1 for u in users if u.gender == "F") / len(users),
            "NB": sum(1 for u in users if u.gender == "NB") / len(users),
        },
        "age_stats": {
            "mean": float(np.mean([u.age for u in users])),
            "std": float(np.std([u.age for u in users])),
            "min": int(np.min([u.age for u in users])),
            "max": int(np.max([u.age for u in users])),
        },
        "race_distribution": {
            race: sum(1 for u in users if u.race_ethnicity == race) / len(users)
            for race in set(u.race_ethnicity for u in users)
        },
    }

    with open(output_dir / "01_user_statistics.json", "w") as f:
        json.dump(user_stats, f, indent=2)

    logger.info(f"  - Saved user statistics to {output_dir / '01_user_statistics.json'}")

    # ====== PHASE 2: Simulate Conversations ======
    logger.info("\n[PHASE 2] Simulating conversations...")
    logger.info("  (Using mock LLM for demonstration)")

    # Use mock LLM for fast demonstration
    llm = MockLLMClient()
    simulator = ConversationSimulator(llm, config.dict())

    conversations = []
    matches = 0

    for i in range(min(config.num_conversations, len(users) - 1)):
        user_a = users[i % len(users)]
        user_b = users[(i + 1) % len(users)]

        # Check if they match
        does_match, match_prob = simulator.simulate_match(
            user_a, user_b,
            homophily_strength=config.homophily_strength
        )

        if does_match:
            # Simulate conversation
            conv = simulator.simulate_conversation(user_a, user_b)
            conversations.append(conv)
            matches += 1

        if (i + 1) % 100 == 0:
            logger.debug(f"  Processed {i + 1}/{config.num_conversations} potential matches")

    logger.info(f"✓ Simulated {matches} conversations from {config.num_conversations} attempts")
    logger.info(f"  - Match rate: {matches / config.num_conversations:.1%}")
    logger.info(f"  - Avg messages per conversation: {np.mean([len(c.messages) for c in conversations]):.1f}")

    # Save conversation statistics
    conv_stats = {
        "total_conversations": len(conversations),
        "match_rate": matches / config.num_conversations,
        "avg_messages": float(np.mean([len(c.messages) for c in conversations])),
        "avg_chars": float(np.mean([c.total_chars for c in conversations])),
        "outcomes": {
            outcome: sum(1 for c in conversations if c.outcome == outcome) / len(conversations)
            for outcome in set(c.outcome for c in conversations)
        }
    }

    with open(output_dir / "02_conversation_statistics.json", "w") as f:
        json.dump(conv_stats, f, indent=2)

    # ====== PHASE 3: Analyze Homophily ======
    logger.info("\n[PHASE 3] Analyzing homophily patterns...")

    homophily_analyzer = HomophilyAnalyzer(conversations)
    homophily_results = homophily_analyzer.analyze_homophily()

    logger.info(f"  ✓ Overall homophily coefficient: {homophily_results['overall_homophily_coeff']:.3f}")
    logger.info(f"    - Age similarity: {homophily_results['homophily_by_dimension']['age']:.3f}")
    logger.info(f"    - Gender match: {homophily_results['homophily_by_dimension']['gender']:.3f}")
    logger.info(f"    - Race match: {homophily_results['homophily_by_dimension']['race']:.3f}")
    logger.info(f"    - Education similarity: {homophily_results['homophily_by_dimension']['education']:.3f}")

    # Save results
    homophily_output = {
        "overall_coefficient": float(homophily_results['overall_homophily_coeff']),
        "by_dimension": {
            k: float(v) for k, v in homophily_results['homophily_by_dimension'].items()
        },
        "significance_test": {
            "observed_mean": float(homophily_results['homophily_significance']['observed_mean']),
            "random_mean": float(homophily_results['homophily_significance']['random_mean']),
            "p_value": float(homophily_results['homophily_significance']['p_value']),
            "significant": bool(homophily_results['homophily_significance']['significant']),
        }
    }

    with open(output_dir / "03_homophily_analysis.json", "w") as f:
        json.dump(homophily_output, f, indent=2)

    # Save summary
    summary = homophily_analyzer.generate_summary()
    with open(output_dir / "03_homophily_summary.txt", "w") as f:
        f.write(summary)

    logger.info(f"  - Saved analysis to {output_dir / '03_homophily_analysis.json'}")

    # ====== PHASE 4: Analyze Gender Dynamics ======
    logger.info("\n[PHASE 4] Analyzing gender dynamics...")

    gender_analyzer = GenderDynamicsAnalyzer(conversations)
    initiation = gender_analyzer.analyze_initiation_patterns()
    escalation = gender_analyzer.analyze_escalation_patterns()

    logger.info(f"  ✓ Male initiation rate: {initiation['male_initiation_rate']:.1%}")
    logger.info(f"  ✓ Female initiation rate: {initiation['female_initiation_rate']:.1%}")

    gender_output = {
        "initiation": {
            "male_rate": float(initiation['male_initiation_rate']),
            "female_rate": float(initiation['female_initiation_rate']),
            "pairings": {
                k: float(v) for k, v in initiation.get('pairing_distribution', {}).items()
            }
        },
        "escalation": {
            k: v for k, v in escalation.items()
        }
    }

    with open(output_dir / "04_gender_dynamics.json", "w") as f:
        json.dump(gender_output, f, indent=2)

    summary = gender_analyzer.generate_summary()
    with open(output_dir / "04_gender_summary.txt", "w") as f:
        f.write(summary)

    logger.info(f"  - Saved analysis to {output_dir / '04_gender_dynamics.json'}")

    # ====== PHASE 5: Generate Report ======
    logger.info("\n[PHASE 5] Generating research report...")

    report = f"""
DATING APP CONVERSATION RESEARCH - EXPERIMENT REPORT
{'=' * 60}

EXPERIMENT: Homophily and Gender Dynamics
Date: {np.datetime64('today')}
Configuration: {config.random_seed} (seed)

USER GENERATION
{'-' * 60}
Total users: {user_stats['total_users']}
Gender distribution:
  - Male: {user_stats['gender_distribution']['M']:.1%}
  - Female: {user_stats['gender_distribution']['F']:.1%}

Age statistics:
  - Mean: {user_stats['age_stats']['mean']:.1f}
  - Std Dev: {user_stats['age_stats']['std']:.1f}

Race distribution:
{chr(10).join(f"  - {k}: {v:.1%}" for k, v in user_stats['race_distribution'].items())}

CONVERSATION SIMULATION
{'-' * 60}
Total conversations: {conv_stats['total_conversations']}
Match rate: {conv_stats['match_rate']:.1%}
Avg messages per conversation: {conv_stats['avg_messages']:.1f}

Outcomes:
{chr(10).join(f"  - {k}: {v:.1%}" for k, v in conv_stats['outcomes'].items())}

HOMOPHILY ANALYSIS
{'-' * 60}
Overall homophily coefficient: {homophily_results['overall_homophily_coeff']:.3f}
(0 = no homophily, 1 = perfect homophily)

By demographic:
  - Age: {homophily_results['homophily_by_dimension']['age']:.3f}
  - Gender: {homophily_results['homophily_by_dimension']['gender']:.3f}
  - Race: {homophily_results['homophily_by_dimension']['race']:.3f}
  - Education: {homophily_results['homophily_by_dimension']['education']:.3f}

Statistical significance:
  - Observed: {homophily_results['homophily_significance']['observed_mean']:.3f}
  - Random baseline: {homophily_results['homophily_significance']['random_mean']:.3f}
  - P-value: {homophily_results['homophily_significance']['p_value']:.3f}
  - Significant: {'YES' if homophily_results['homophily_significance']['significant'] else 'NO'}

GENDER DYNAMICS
{'-' * 60}
Initiation patterns:
  - Male initiators: {initiation['male_initiation_rate']:.1%}
  - Female initiators: {initiation['female_initiation_rate']:.1%}

OUTPUTS SAVED
{'-' * 60}
Location: {output_dir}

Files generated:
  - 01_user_statistics.json
  - 02_conversation_statistics.json
  - 03_homophily_analysis.json
  - 03_homophily_summary.txt
  - 04_gender_dynamics.json
  - 04_gender_summary.txt
  - REPORT.txt (this file)

NEXT STEPS
{'-' * 60}
1. Review outputs in {output_dir}
2. Extend analysis (erotic capital, power dynamics)
3. Create visualizations for publication
4. Write research paper
5. Submit to conference/journal

ETHICS & REPRODUCIBILITY
{'-' * 60}
✓ Synthetic data only (no real users)
✓ Fully reproducible (seed {config.random_seed})
✓ Configuration saved
✓ Code version controlled
✓ Meets publication standards

For ethics discussion, see ETHICS_FRAMEWORK.md
For methodology details, see METHODOLOGY.md

{'=' * 60}
"""

    with open(output_dir / "REPORT.txt", "w") as f:
        f.write(report)

    logger.info(report)

    logger.info(f"\n✓ All outputs saved to: {output_dir}")
    logger.info("✓ Experiment complete!")

    return {
        "output_dir": str(output_dir),
        "user_stats": user_stats,
        "conversation_stats": conv_stats,
        "homophily_results": homophily_output,
        "gender_results": gender_output,
    }


if __name__ == "__main__":
    try:
        results = run_experiment()
        logger.info("Experiment successful!")
    except Exception as e:
        logger.error(f"Experiment failed: {e}", exc_info=True)
        raise
