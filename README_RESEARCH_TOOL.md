# Dating App Conversation Research Framework

**Research tool for studying conversation patterns using synthetic simulation and ethical analysis.**

## CRITICAL DISCLAIMER

This tool uses **SYNTHETIC DATA ONLY**. It is designed for academic research on conversation patterns without deceiving real users or violating platform terms.

- **NOT for automating real Tinder**: Does not connect to Tinder's platform
- **NOT for bot creation**: Does not interact with real users
- **NOT for scraping**: Does not collect real data without consent

## Why Synthetic Simulation?

| Approach | Ethical | Legal | Academic Value |
|----------|----------|--------|-----------------|
| **Real Tinder (this tool doesn't do)** | ❌ No | ❌ No (violates ToS) | ✓ High but unethical |
| **Synthetic Simulation (this tool)** | ✓ Yes | ✓ Yes | ✓ High + publishable |
| **Consented Real Study** | ✓ Yes | ✓ Yes | ✓ Highest |
| **Public Datasets** | ✓ Yes | ✓ Yes | ✓ Good |

This tool enables the ethical, legal approach with publishable research quality.

## What This Tool Does

### 1. Generates Synthetic Users
- Realistic demographic profiles (age, gender, race, education)
- Personality traits (Big Five)
- Generated profile text (not real)
- Homophily preferences for matching
- Conversation strategies

### 2. Simulates Conversations
- Two LLM-based agents (not real users)
- Realistic conversation flow
- Different conversation strategies
- Controllable parameters

### 3. Analyzes Patterns

**Homophily**: Do similar users match together?
```
- Demographics mixing matrix (race, gender, age)
- Preference satisfaction rates
- Homophily coefficient
- Statistical significance tests
```

**Gender Dynamics**: How do men and women interact differently?
```
- Who initiates conversations
- Conversation length by gender
- Topic progression
- Response patterns
- Escalation differences
```

**Erotic Capital**: How are attractiveness signals expressed?
```
- Physical reference frequency
- Flirtation patterns
- Body-related language
- Compliment dynamics
```

**Power Dynamics**: Who controls the conversation?
```
- Message frequency
- Topic initiation
- Escalation patterns
- Agreement signals
```

**Communication Patterns**: How do people talk?
```
- Linguistic analysis
- Formality levels
- Humor and tone
- Self-disclosure
- Politeness markers
```

### 4. Produces Research Outputs
- Statistical summaries (tables, significance tests)
- Visualizations (demographic matrices, network graphs)
- Publishable figures (PDF, PNG)
- Reproducible experiments (code + config)

## Architecture

```
tinder_research/
├── simulation/
│   ├── user_generator.py      # Synthetic user generation
│   └── conversation_simulator.py  # LLM-based agents
├── analysis/
│   ├── homophily_analyzer.py     # Demographic patterns
│   ├── gender_dynamics.py        # Gender differences
│   ├── power_dynamics.py         # Conversational power
│   ├── erotic_capital.py         # Attractiveness signals
│   └── linguistic_analysis.py    # Language patterns
├── visualization/
│   ├── dashboards.py             # Interactive plots
│   ├── statistical_plots.py      # Figures for papers
│   └── networks.py               # Network visualizations
├── data/
│   ├── storage.py                # Database/file storage
│   └── anonymization.py          # Data protection
└── utils/
    ├── config.py                 # Configuration management
    └── logging.py                # Research logging
```

## Quick Start

### Installation

```bash
# Clone repository
git clone <repo-url>
cd tinder-research

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

### Basic Usage

```python
from tinder_research.simulation.user_generator import UserGenerator
from tinder_research.simulation.conversation_simulator import ConversationSimulator, MockLLMClient
from tinder_research.analysis.homophily_analyzer import HomophilyAnalyzer
from tinder_research.utils.config import Config

# Configuration
config = Config(
    num_users=100,
    num_conversations=500,
    random_seed=42
)

# Generate synthetic users
generator = UserGenerator(seed=config.random_seed)
users = generator.generate_users(config.num_users, config.demographics)

# Simulate conversations (using mock LLM for testing)
llm = MockLLMClient()
simulator = ConversationSimulator(llm, config)

conversations = []
for i in range(config.num_conversations):
    user_a = users[i % len(users)]
    user_b = users[(i + 1) % len(users)]
    
    # Check if they match
    matches, prob = simulator.simulate_match(user_a, user_b)
    
    if matches:
        conv = simulator.simulate_conversation(user_a, user_b)
        conversations.append(conv)

# Analyze homophily
analyzer = HomophilyAnalyzer(conversations)
results = analyzer.analyze_homophily()

print(analyzer.generate_summary())
```

### Run Full Experiment

```bash
# Run example experiment
python -m tinder_research.experiments.example_experiment

# Or with command-line interface
tinder-research --config config.yaml --output results/
```

## Research Questions

This framework helps answer:

1. **Homophily**: Do users preferentially match with similar demographics?
2. **Gender Bias**: Do men and women experience different conversation dynamics?
3. **Erotic Capital**: How do attractiveness signals appear in conversations?
4. **Power Dynamics**: Who controls conversation direction?
5. **Communication Norms**: What conversation patterns emerge?
6. **Strategy Effects**: Do different approaches get different responses?

## Configuration

All parameters in `config.yaml`:

```yaml
# User generation
num_users: 100
demographics:
  gender_split: {M: 0.5, F: 0.5}
  age_mean: 28
  age_std: 5
  race_distribution:
    white: 0.65
    black: 0.13
    hispanic: 0.19

# Conversations
num_conversations: 1000
max_turns_per_conversation: 25
homophily_strength: 0.6
strategies: ["casual", "direct", "romantic", "playful"]

# LLM
llm_provider: openai
openai_model: gpt-4
temperature: 0.7

# Analysis
disaggregate_by: [gender, race, age_group, education]
fairness_metrics: [demographic_parity, equalized_odds]
```

## Analysis Walkthrough

### 1. Homophily Analysis

```python
from tinder_research.analysis.homophily_analyzer import HomophilyAnalyzer

analyzer = HomophilyAnalyzer(conversations)

# Overall homophily
results = analyzer.analyze_homophily()
print(f"Homophily coefficient: {results['overall_homophily_coeff']:.3f}")

# Demographic mixing
print(f"Race mixing matrix:\n{results['race_mixing_matrix']}")

# Statistical significance
sig = results['homophily_significance']
print(f"Significant homophily? {sig['significant']} (p={sig['p_value']:.3f})")
```

### 2. Gender Dynamics

```python
from tinder_research.analysis.gender_dynamics import GenderDynamicsAnalyzer

analyzer = GenderDynamicsAnalyzer(conversations)

# Who initiates?
initiation = analyzer.analyze_initiation_patterns()
print(f"Male initiation rate: {initiation['male_initiation_rate']:.1%}")

# How do they escalate?
escalation = analyzer.analyze_escalation_patterns()

# Response patterns
response = analyzer.analyze_response_patterns()
```

### 3. Visualization

```python
from tinder_research.visualization.statistical_plots import StatisticalPlotter

plotter = StatisticalPlotter(conversations)

# Homophily matrix heatmap
plotter.plot_homophily_matrix()

# Gender dynamics comparison
plotter.plot_gender_dynamics()

# Network of conversations
plotter.plot_conversation_network()
```

## Methodological Details

### Synthetic User Generation

Users are generated with:
- **Reproducible randomness** (seeds for all RNG)
- **Realistic distributions** (US Census-based demographics)
- **Homophily preferences** (preferential matching)
- **Personality traits** (Big Five model)
- **Latent attributes** (erotic capital)

See `METHODOLOGY.md` for complete details.

### Conversation Simulation

Each conversation:
- **Uses LLM agents** (OpenAI/Anthropic) or **mocks for testing**
- **Has realistic personas** from synthetic profiles
- **Follows natural flow** (opening → escalation → conclusion)
- **Is reproducible** (all seeds and prompts logged)
- **Is stored with metadata** (turn count, outcome, etc.)

### Analysis Pipeline

All analyses include:
- **Disaggregation** (by gender, race, age, education)
- **Significance testing** (is effect real or random?)
- **Fairness assessment** (are outcomes equitable?)
- **Bias documentation** (limitations disclosed)
- **Effect sizes** (practical significance, not just stats)

## Ethics & Reproducibility

### Ethics Framework

See `ETHICS_FRAMEWORK.md` for:
- Why this approach is ethical
- What's prohibited
- Data protection protocols
- Publication standards
- IRB considerations

### Reproducibility

Every experiment:
- **Version controlled** (git)
- **Seeded** (deterministic randomness)
- **Configurable** (all params in YAML)
- **Logged** (all decisions recorded)
- **Tested** (unit + integration tests)
- **Documented** (inline + separate docs)

### Example: Full Reproducibility

```bash
# Exact reproduction
git clone <repo-url>
git checkout v0.1.0
python -m tinder_research.experiments.experiment_1 --config config_v0.1.0.yaml

# Will produce identical results (same seed, same LLM responses)
```

## Publication & Sharing

This framework is designed for:

✓ **Conference papers** (ACM FAccT, AIES, NeurIPS, etc.)
✓ **Journal articles** (social science, CS, HCI)
✓ **Dissertations** (thesis chapters)
✓ **Preprints** (arXiv)

**NOT for:**
- ❌ Real Tinder automation
- ❌ Deceiving users
- ❌ Privacy violation
- ❌ Discrimination systems

## Extending the Framework

### Add New Analysis

```python
from tinder_research.analysis.base import ConversationAnalyzer

class MyAnalysis(ConversationAnalyzer):
    def __init__(self, conversations):
        super().__init__(conversations)
    
    def analyze(self):
        # Your analysis here
        pass
```

### Add Visualization

```python
from tinder_research.visualization.base import Visualizer

class MyPlot(Visualizer):
    def plot(self):
        # Your plot here
        pass
```

### Custom LLM Provider

```python
from tinder_research.utils.llm_interface import LLMClient

class MyLLM(LLMClient):
    def create_message(self, prompt, temperature, max_tokens):
        # Your LLM call here
        pass
```

## Papers Using This Tool

(To be filled as research is published)

## Citation

```bibtex
@software{dating_research_2024,
  title={Dating App Conversation Research Framework},
  author={Research Team},
  year={2024},
  url={https://github.com/your-org/tinder-research},
  note={Synthetic simulation for ethical academic research}
}
```

## Contributing

Contributions welcome! Please:
1. Review `ETHICS_FRAMEWORK.md` first
2. Add tests for new code
3. Document methodology changes
4. Note any bias/fairness implications

## License

MIT License - See LICENSE file

## Authors

Research Team

## Support

- **Issues**: GitHub Issues
- **Questions**: Discussions
- **Ethics concerns**: ETHICS_FRAMEWORK.md

---

**Remember**: This tool is designed for ethical, publishable research. When in doubt, check `ETHICS_FRAMEWORK.md`.
