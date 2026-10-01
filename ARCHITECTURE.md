# System Architecture

## Overview

This research framework is built on a layered architecture separating concerns:

```
┌─────────────────────────────────────────────────────────┐
│         VISUALIZATION & REPORTING LAYER                  │
│  (dashboards, plots, tables, paper-ready figures)        │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────┐
│           ANALYSIS LAYER                                  │
│  (homophily, gender, power, erotic capital, linguistics) │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────┐
│         DATA STORAGE & ANONYMIZATION LAYER               │
│  (conversation persistence, anonymization, versioning)   │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────┐
│         SIMULATION LAYER                                  │
│  (conversation simulator, LLM agents, matching)           │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────┐
│         USER GENERATION LAYER                            │
│  (synthetic users, demographics, preferences, personas)  │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────┐
│         UTILITIES & INFRASTRUCTURE LAYER                 │
│  (config, logging, LLM clients, ethics guards)           │
└─────────────────────────────────────────────────────────┘
```

## Layer Details

### 1. User Generation Layer
**Files**: `simulation/user_generator.py`

**Responsibilities**:
- Generate synthetic user profiles with demographic variety
- Sample from configured distributions
- Create realistic profile text
- Set homophily preferences
- Assign conversation strategies

**Key Classes**:
```python
UserProfile:
  - id, demographics, profile_text
  - personality traits (Big Five)
  - erotic_capital_score
  - preferences, strategies
  - anonymization support

UserGenerator:
  - generates batches of users
  - deterministic (seeded for reproducibility)
  - configurable distributions
```

**Outputs**: List of `UserProfile` objects

---

### 2. Simulation Layer
**Files**: `simulation/conversation_simulator.py`

**Responsibilities**:
- Determine if two users match
- Simulate realistic conversations
- Manage LLM-based agents
- Track conversation outcomes

**Key Classes**:
```python
ConversationSimulator:
  - match probability calculation
  - conversation flow management
  - LLM prompt engineering
  - conversation logging

Conversation:
  - message history
  - outcome tracking
  - metadata (duration, turns, etc)
  
Message:
  - sender/recipient
  - text, timestamp, turn
  - metrics (length, etc)

MockLLMClient:
  - fast testing without API calls
  - template-based responses
```

**Workflow**:
```
1. User A matches with User B
2. User A generates opener (LLM)
3. User B reads, decides to respond
4. User B generates response (LLM)
5. Repeat until conclusion or max turns
6. Save conversation with metadata
```

---

### 3. Data Storage Layer
**Files**: `data/storage.py`, `data/anonymization.py`

**Responsibilities**:
- Persist conversations to database/files
- Anonymize sensitive information
- Enable reproducible data loading
- Support versioning for experiments

**Key Classes**:
```python
ConversationStorage:
  - save/load conversations
  - database schema
  - file formatting
  
AnonymizationManager:
  - hash real identifiers
  - remove PII
  - verify anonymization
  - audit trail
```

**Storage Formats**:
- JSON (conversations with metadata)
- CSV (analytical tables)
- SQLite (indexed queries)
- Parquet (efficient analytics)

---

### 4. Analysis Layer
**Files**: `analysis/homophily_analyzer.py`, `analysis/gender_dynamics.py`, `analysis/power_dynamics.py`, etc.

**Responsibilities**:
- Extract patterns from conversations
- Compute statistical metrics
- Test hypotheses
- Disaggregate by demographics
- Assess fairness

**Key Classes**:

```python
HomophilyAnalyzer:
  - demographic similarity computation
  - mixing matrix construction
  - homophily coefficient
  - significance testing
  
GenderDynamicsAnalyzer:
  - initiation patterns
  - escalation analysis
  - response patterns
  - tone analysis
  
EroticCapitalAnalyzer:
  - physical reference detection
  - flirtation patterns
  - attractiveness signals
  
PowerDynamicsAnalyzer:
  - message frequency analysis
  - topic control
  - escalation patterns
  
LinguisticAnalyzer:
  - formality assessment
  - emotion analysis
  - self-disclosure metrics
```

**Output Format**:
```python
{
  "metric_name": {
    "overall": float,
    "by_dimension": {
      "gender": {...},
      "race": {...}
    },
    "statistics": {
      "p_value": float,
      "effect_size": float
    }
  }
}
```

---

### 5. Visualization Layer
**Files**: `visualization/dashboards.py`, `visualization/statistical_plots.py`, `visualization/networks.py`

**Responsibilities**:
- Create publication-ready figures
- Generate interactive dashboards
- Build network visualizations
- Produce summary tables

**Key Classes**:
```python
StatisticalPlotter:
  - demographic mixing matrices (heatmaps)
  - gender dynamics comparisons
  - homophily distributions
  
DashboardGenerator:
  - interactive Plotly dashboards
  - real-time analytics
  - multi-view summaries
  
NetworkVisualizer:
  - conversation graphs
  - user similarity networks
  - interaction flows
```

**Output Formats**:
- PDF (publication figures)
- PNG (presentations)
- SVG (web)
- HTML (interactive dashboards)

---

### 6. Utilities & Infrastructure
**Files**: `utils/config.py`, `utils/logging.py`, `utils/llm_interface.py`

**Responsibilities**:
- Centralized configuration
- Structured logging
- LLM client abstraction
- Ethics guardrails

**Key Classes**:
```python
Config:
  - all hyperparameters
  - YAML loading/saving
  - validation
  - reproducibility tracking
  
ResearchLogger:
  - experiment-scoped logging
  - file + console output
  - structured logging
  
LLMClient (abstract):
  - OpenAI, Anthropic, Mock implementations
  - prompt templating
  - rate limiting
  - error handling
  
EthicsGuard:
  - prevent real credentials
  - synthetic-only enforcement
  - audit logging
```

---

## Data Flow

### Experiment Workflow

```
┌─ SETUP ─────────────────────────────────────┐
│ Load config → Initialize logging → Ethics   │
│ check → Set random seed                     │
└──────────────┬──────────────────────────────┘
               │
┌──────────────┴──────────────────────────────┐
│ GENERATION                                   │
│ UserGenerator → Users (N=100)                │
│ Config.demographics → Realistic variation    │
└──────────────┬──────────────────────────────┘
               │
┌──────────────┴──────────────────────────────┐
│ MATCHING & SIMULATION                        │
│ For each potential pair:                     │
│  1. Calculate match probability              │
│  2. If match: simulate conversation          │
│  3. LLM agents exchange messages             │
│  4. Track outcomes                           │
└──────────────┬──────────────────────────────┘
               │
┌──────────────┴──────────────────────────────┐
│ STORAGE & ANONYMIZATION                      │
│ Save conversations → Hash IDs                │
│ Verify anonymization → Archive               │
└──────────────┬──────────────────────────────┘
               │
┌──────────────┴──────────────────────────────┐
│ ANALYSIS                                     │
│ For each analyzer:                           │
│  1. Load conversations                       │
│  2. Compute metrics                          │
│  3. Disaggregate by demographic              │
│  4. Test significance                        │
│  5. Assess fairness                          │
└──────────────┬──────────────────────────────┘
               │
┌──────────────┴──────────────────────────────┐
│ VISUALIZATION & REPORTING                    │
│ Generate figures → Create tables              │
│ Build dashboards → Write reports              │
│ Export for publication                        │
└──────────────┴──────────────────────────────┘
```

### Data Format Transitions

```
UserProfile (objects)
       ↓
Conversation (objects with messages)
       ↓
ConversationStore (JSON/SQLite)
       ↓
ConversationAnalysis (Dict of metrics)
       ↓
AnalysisDataFrame (Pandas)
       ↓
Visualization (PDF/PNG/HTML)
       ↓
Publication/Sharing
```

---

## Dependencies & Interfaces

### External Dependencies

```
┌─────────────────────────────────────────────┐
│ LLM Providers                                │
├─────────────────────────────────────────────┤
│ - OpenAI (GPT-4)                             │
│ - Anthropic (Claude)                         │
│ - Mock (testing)                             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Data & Analytics Libraries                   │
├─────────────────────────────────────────────┤
│ - Pandas (DataFrames)                        │
│ - NumPy (numerical)                          │
│ - SciPy (statistics)                         │
│ - Scikit-learn (ML metrics)                  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Visualization Libraries                      │
├─────────────────────────────────────────────┤
│ - Matplotlib (static)                        │
│ - Seaborn (statistical)                      │
│ - Plotly (interactive)                       │
│ - NetworkX (graphs)                          │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Fairness & Ethics                            │
├─────────────────────────────────────────────┤
│ - FairLearn (fairness metrics)               │
│ - AIF360 (algorithmic fairness)              │
└─────────────────────────────────────────────┘
```

---

## Extensibility Points

### Add New Analysis Type

```python
# analysis/my_analysis.py
from .base import ConversationAnalyzer

class MyAnalyzer(ConversationAnalyzer):
    def analyze(self) -> Dict:
        # Your logic here
        return results
```

### Add New Visualization

```python
# visualization/my_plots.py
from .base import Visualizer

class MyPlotter(Visualizer):
    def plot_something(self):
        # Your plotting code
        return figure
```

### Add New LLM Provider

```python
# utils/llm_clients.py
class MyLLM(LLMClient):
    def create_message(self, prompt, temperature, max_tokens):
        # Your API call
        return response_text
```

### Add New User Generation Strategy

```python
# simulation/user_generator.py
# Extend UserGenerator with new demographic sampling methods
```

---

## Testing Strategy

### Unit Tests
```
tests/
├── test_user_generator.py
├── test_conversation_simulator.py
├── test_analyzers.py
└── test_storage.py
```

### Integration Tests
```
tests/
├── test_full_pipeline.py
└── test_reproducibility.py
```

### Reproducibility Tests
```
# Same config → Exact same results
# Different seed → Different but consistent results
```

---

## Performance Considerations

### Scalability

| Component | Users | Conversations | Time | Memory |
|-----------|-------|---------------|------|--------|
| Generate | 1,000 | - | ~5s | ~100MB |
| Simulate | - | 10,000 | ~5m* | ~500MB |
| Analyze | - | 10,000 | ~30s | ~1GB |
| Visualize | - | 10,000 | ~1m | ~500MB |

*With mock LLM. Real LLM: ~30-60m (rate-limited)

### Optimization Techniques

1. **Batch Processing**: Process conversations in batches
2. **Caching**: Cache computed metrics
3. **Multiprocessing**: Parallel analysis by demographic
4. **Lazy Loading**: Load data on demand
5. **Vectorization**: NumPy operations instead of loops

---

## Deployment Considerations

### Production Deployment

```dockerfile
FROM python:3.10
WORKDIR /research
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "tinder_research.experiments.run_all"]
```

### Configuration Management

- Development: `config_dev.yaml`
- Staging: `config_staging.yaml`
- Production: `config_prod.yaml`

### Monitoring & Logging

- All experiments logged to `logs/`
- Error tracking with structured logging
- Experiment metadata captured
- Results versioned with git

---

## Security & Ethics

### Code-Level Safeguards

```python
# In config.py
if os.getenv("TINDER_TOKEN"):
    raise ValueError("Real credentials detected!")

# In simulation.py
if not self.config.synthetic_mode:
    raise ValueError("Only synthetic mode allowed!")
```

### Data Protection

1. Hashed user IDs (not linkable to real people)
2. Synthetic profile text (generated, not real)
3. Anonymization verification
4. Audit logs of all access
5. Secure deletion protocols

---

## Maintenance & Evolution

### Version Compatibility

```python
# Each analysis version tracks:
- methodology version
- data version
- config version
- code commit hash
```

### Backwards Compatibility

- Maintain support for older data formats
- Document breaking changes
- Provide migration scripts
- Version all APIs

---

## Documentation Structure

```
docs/
├── ARCHITECTURE.md (this file)
├── API.md (function signatures)
├── METHODOLOGY.md (research design)
├── ETHICS_FRAMEWORK.md (ethical guidelines)
├── CONTRIBUTING.md (developer guide)
└── examples/ (code examples)
```

This architecture enables academic-grade research with strong ethical foundations and reproducibility guarantees.
