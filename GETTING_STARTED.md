# Getting Started with the Dating App Research Framework

Follow this checklist to get up and running with your research.

## Step 1: Read the Foundational Documents

- [ ] **ETHICS_FRAMEWORK.md** ⚠️ READ THIS FIRST
  - Why synthetic data is ethical
  - What you're NOT allowed to do
  - How to publish responsibly

- [ ] **METHODOLOGY.md**
  - Research design
  - How the simulation works
  - Analysis pipeline
  - Reproducibility standards

- [ ] **ARCHITECTURE.md**
  - System design
  - Code organization
  - How to extend

- [ ] **README_RESEARCH_TOOL.md**
  - Tool overview
  - Installation
  - Quick start

**Estimated time**: 30-45 minutes

---

## Step 2: Install & Verify

```bash
# Clone the repository
git clone <repo-url>
cd tinder-research

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

# Verify installation
python -c "import tinder_research; print('✓ Installation successful')"
```

**Expected output**: `✓ Installation successful`

---

## Step 3: Run the Example Experiment

This runs with synthetic data and mock LLM (no API calls):

```bash
python -m tinder_research.experiments.example_experiment
```

**What it does**:
1. Generates 100 synthetic users
2. Simulates 500+ conversations
3. Analyzes homophily patterns
4. Analyzes gender dynamics
5. Saves outputs to `outputs/example_experiment/`

**Expected time**: 2-5 minutes

**What to look for**:
```
outputs/example_experiment/
├── 01_user_statistics.json        # User generation stats
├── 02_conversation_statistics.json # Conversation outcomes  
├── 03_homophily_analysis.json      # Homophily findings
├── 03_homophily_summary.txt        # Text summary
├── 04_gender_dynamics.json         # Gender findings
├── 04_gender_summary.txt           # Text summary
└── REPORT.txt                      # Complete report
```

---

## Step 4: Review the Example Output

```bash
# Read the report
cat outputs/example_experiment/REPORT.txt

# Look at JSON results
python -m json.tool outputs/example_experiment/03_homophily_analysis.json

# Review user statistics
python -m json.tool outputs/example_experiment/01_user_statistics.json
```

**Key metrics to understand**:
- `homophily_coefficient`: 0-1 scale (0=no homophily, 1=perfect homophily)
- `overall_homophily_coeff`: Overall demographic similarity in matches
- `gender_mixing`: Distribution of who initiates by gender
- `conversation_statistics`: Outcomes, message counts, etc.

---

## Step 5: Design Your Own Experiment

Now it's time to ask YOUR research question.

### Choose a Research Question

Pick one of these (or your own):

**Option A: Homophily**
```
RQ: Do demographic characteristics affect matching probability?
Analysis: Compute homophily coefficients by demographic group
Output: Mixing matrices, statistical tests
```

**Option B: Gender Dynamics**
```
RQ: How do men and women initiate and escalate conversations differently?
Analysis: Disaggregate all metrics by gender
Output: Comparison tables, significance tests
```

**Option C: Communication Strategies**
```
RQ: Do different opening strategies get different response rates?
Analysis: By strategy type and demographic
Output: Strategy effectiveness by group
```

**Option D: Erotic Capital**
```
RQ: How are attractiveness signals expressed in conversations?
Analysis: Text analysis for physical references, flirtation
Output: Signal frequency, correlation with outcomes
```

### Modify the Configuration

```bash
# Copy template
cp config_template.yaml config.yaml

# Edit your config
nano config.yaml  # or your favorite editor
```

**Key parameters to modify**:
- `num_users`: How many synthetic users (100-1000)
- `num_conversations`: How many conversations (100-5000)
- `homophily_strength`: How much homophily (0.0-1.0)
- `demographics`: Your specific demographic distribution
- `random_seed`: Your experiment seed (for reproducibility)

### Run Your Experiment

```bash
python -m tinder_research.experiments.example_experiment --config config.yaml
```

Or create a custom experiment:

```python
# my_experiment.py
from tinder_research.simulation.user_generator import UserGenerator
from tinder_research.simulation.conversation_simulator import ConversationSimulator, MockLLMClient
from tinder_research.analysis.homophily_analyzer import HomophilyAnalyzer
from tinder_research.utils.config import get_config

config = get_config()

# Step 1: Generate users
generator = UserGenerator(seed=config.random_seed)
users = generator.generate_users(100, config.demographics)

# Step 2: Simulate conversations
llm = MockLLMClient()
simulator = ConversationSimulator(llm, config.dict())

conversations = []
for i in range(200):
    user_a = users[i % len(users)]
    user_b = users[(i + 1) % len(users)]
    
    if simulator.simulate_match(user_a, user_b)[0]:
        conv = simulator.simulate_conversation(user_a, user_b)
        conversations.append(conv)

# Step 3: Analyze
analyzer = HomophilyAnalyzer(conversations)
results = analyzer.analyze_homophily()
print(f"Homophily coefficient: {results['overall_homophily_coeff']:.3f}")
```

---

## Step 6: Analyze Results

After your experiment runs, analyze the JSON outputs:

```python
import json
import pandas as pd

# Load results
with open("outputs/my_experiment/03_homophily_analysis.json") as f:
    results = json.load(f)

# Create summary table
summary = {
    "Metric": [],
    "Value": [],
    "Interpretation": []
}

summary["Metric"].append("Homophily Coefficient")
summary["Value"].append(f"{results['overall_coefficient']:.3f}")
summary["Interpretation"].append("0-1 scale, higher = more homophily")

summary["Metric"].append("Statistical Significance")
summary["Value"].append(f"p={results['significance_test']['p_value']:.3f}")
summary["Interpretation"].append("< 0.05 = significant")

df = pd.DataFrame(summary)
print(df.to_string())
```

---

## Step 7: Create Visualizations

```python
from tinder_research.visualization.statistical_plots import StatisticalPlotter
from pathlib import Path

# Load conversations (you'd have saved them)
# plotter = StatisticalPlotter(conversations, output_dir=Path("figures"))
# plotter.generate_all_figures()

# Or create individual plots
# plotter.plot_homophily_matrix()
# plotter.plot_gender_dynamics()
# plotter.plot_conversation_length_by_gender()
```

This creates publication-ready figures in `figures/`:
- `01_homophily_matrix.pdf`
- `03_gender_dynamics.pdf`
- `04_conversation_length.pdf`

---

## Step 8: Write Your Research Paper

### Structure

```
1. Introduction
   - Why study dating apps?
   - Your specific research question
   
2. Related Work
   - Homophily literature
   - Gender and communication
   - Online dating research
   
3. Methodology
   - Synthetic user generation
   - Conversation simulation
   - Analysis approach
   - (Include METHODOLOGY.md as appendix)
   
4. Results
   - Your key findings
   - Tables and figures from Step 7
   - Disaggregated by demographics
   
5. Discussion
   - Interpretation of results
   - Limitations (important!)
   - Implications
   
6. Ethics & Reproducibility
   - Why synthetic data is appropriate
   - How to reproduce your results
   - Code availability (GitHub)
   
7. Conclusion
```

### Sample Results Section

```markdown
## Results

We analyzed 1,247 synthetic conversations across 100 users 
with varied demographics.

### Homophily Analysis

Demographic similarity significantly predicted matching 
(homophily coefficient = 0.68, p < 0.001). This was 
particularly strong for:

- Race/ethnicity (r = 0.82)
- Education level (r = 0.71)  
- Age similarity (r = 0.64)

Gender showed moderate mixing (homophily = 0.52), 
suggesting less gender-based homophily in our simulation.

[TABLE 1: Homophily by Demographic]
[FIGURE 1: Demographic Mixing Matrix]

### Gender Dynamics

Men initiated 52% of conversations (n=615), while women 
initiated 48% (n=582). No significant difference was found 
in initiation rates (χ²=0.18, p=0.67).

However, we observed significant differences in conversation 
length. Conversations initiated by men averaged 12.3 messages 
(SD=4.1), while those by women averaged 11.8 messages 
(SD=3.9), t(1245)=2.11, p=0.035.

[TABLE 2: Conversation Statistics by Gender]
[FIGURE 2: Gender Dynamics Comparison]
```

---

## Step 9: Submit to Conference/Journal

### Choose Your Venue

Based on your RQ:
- **Homophily/matching**: Sociology, social computing
- **Gender/communication**: Communication, gender studies, HCI
- **Strategy/persuasion**: Marketing, psychology
- **Fairness/bias**: ACM FAccT, AIES conferences

### Prepare Supplementary Materials

```
supplementary/
├── methodology/
│   ├── METHODOLOGY.md
│   ├── ETHICS_FRAMEWORK.md
│   └── config_used.yaml
├── code/
│   ├── experiment.py
│   ├── analysis.py
│   └── requirements.txt
├── data/
│   ├── conversations_anonymized.json
│   └── analysis_results.csv
└── reproducibility/
    ├── REPRODUCE.md
    └── random_seed_log.txt
```

### Include Reproducibility Statement

```markdown
## Reproducibility

All code is available at: https://github.com/your-org/tinder-research

To reproduce:
1. `git clone https://github.com/your-org/tinder-research`
2. `pip install -r requirements.txt`
3. `cp config_template.yaml config.yaml`
4. Modify as needed
5. `python -m tinder_research.experiments.example_experiment --config config.yaml`

Results will match exactly (same seed).
```

---

## Step 10: Publish & Share

```bash
# Create GitHub repository
git init
git add .
git commit -m "Initial commit: dating app research framework"
git remote add origin <repo-url>
git push -u origin main

# Get DOI (via Zenodo)
# https://zenodo.org/

# Share on:
# - ArXiv (preprint)
# - GitHub (code)
# - OSF (open science framework)
```

---

## Troubleshooting

### Installation Issues

```bash
# Make sure you have Python 3.10+
python --version

# If pip install fails, try upgrading pip
pip install --upgrade pip

# Install with minimal deps first
pip install -r requirements-minimal.txt
```

### LLM API Issues

```bash
# Test OpenAI API
export OPENAI_API_KEY="sk-..."
python -c "from openai import OpenAI; c = OpenAI(); print(c.models.list())"

# Test Anthropic API
export ANTHROPIC_API_KEY="sk-ant-..."
python -c "from anthropic import Anthropic; c = Anthropic(); print(c.models.list())"
```

### Performance Issues

```bash
# Start small
num_users: 20
num_conversations: 50

# Use mock LLM
llm_provider: mock

# Once working, scale up gradually
```

---

## Checklist Summary

- [ ] Read ETHICS_FRAMEWORK.md
- [ ] Read METHODOLOGY.md  
- [ ] Install requirements
- [ ] Run example experiment
- [ ] Review example outputs
- [ ] Choose research question
- [ ] Create config.yaml
- [ ] Run your experiment
- [ ] Analyze JSON results
- [ ] Create visualizations
- [ ] Write paper
- [ ] Submit to venue
- [ ] Share on GitHub/OSF

---

## Next Steps

1. **If starting now**: Jump to Step 3 (Run Example)
2. **If designing custom research**: Jump to Step 5
3. **If ready to publish**: Jump to Step 8

Good luck! 🚀

---

## Questions?

- **Ethics**: See ETHICS_FRAMEWORK.md
- **Methodology**: See METHODOLOGY.md
- **Technical**: See ARCHITECTURE.md and README_RESEARCH_TOOL.md
- **Code examples**: See `tinder_research/experiments/example_experiment.py`
