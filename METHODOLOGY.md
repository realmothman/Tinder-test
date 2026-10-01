# Research Methodology: Dating App Conversation Analysis

## Overview

This tool simulates conversations between heterogeneous synthetic users to study emergent communication patterns. Unlike automation of real Tinder, this research framework:
- Generates synthetic user profiles with controlled demographic variation
- Simulates realistic conversations using LLM-based agents
- Analyzes patterns ethically without deceiving real users
- Produces reproducible, publishable research

## Research Questions

### Primary
1. **Homophily Patterns**: Do users preferentially match with others similar to themselves? (demographics, interests)
2. **Gender Dynamics**: Do conversation initiators, progression patterns, and escalation differ by gender?
3. **Erotic Capital**: Can we identify signals of physical attractiveness claims in conversations?
4. **Power Dynamics**: Who escalates? Who rejects? What's the pattern?

### Secondary
1. **Persona Effects**: Do different conversation strategies get different responses?
2. **Demographic Signaling**: How do users signal race/class/status in conversations?
3. **Communication Rituals**: Are there consistent opening patterns?
4. **Performativity**: Do conversations match profile personas?

## Methodology

### Phase 1: Synthetic User Generation

#### User Profile Schema
```python
{
    "id": "user_XXXX_synthetic",  # hashed, not real
    "demographics": {
        "age": 25-45,              # uniform random
        "gender": "M"/"F"/"NB",     # controlled ratio
        "race_ethnicity": "string", # categorical
        "education": "string",      # categorical
        "occupation": "string"      # categorical
    },
    "profile_text": {
        "headline": "generated",    # LLM-generated from persona
        "bio": "generated",         # LLM-generated
        "interests": [...]          # sampled from taxonomy
    },
    "erotic_capital_score": 0-10,   # latent attribute
    "homophily_preferences": {
        "age_range": [min, max],    # preference distribution
        "race_preferences": {...},  # preference matrix
        "class_preferences": {...}  # occupational similarity
    },
    "personality": {
        "openness": 0-1,
        "extraversion": 0-1,
        "agreeableness": 0-1,
        "conscientiousness": 0-1,
        "neuroticism": 0-1
    }
}
```

#### Generation Strategy
1. Sample base demographics (age, gender, race)
2. Generate correlated attributes (education from age/race distributions)
3. Sample personality traits (Big Five)
4. Generate profile text using LLM templated to persona
5. Create preference matrices for homophily testing

#### Demographic Sampling
```
Gender:     50% M, 50% F (+ NB variant)
Age:        Normal(28, 5) truncated [22, 50]
Race:       US Census approximation (70% W, 20% AA, 10% Latinx, ...)
Education:  Categorical (HS, BA, MA, PhD)
Class:      Inferred from education + occupation
```

### Phase 2: Conversation Simulation

#### Matching Algorithm
```python
def match(user_a, user_b):
    """
    Probability of match based on:
    1. Homophily (preference for similar demographics)
    2. Attractiveness (erotic capital)
    3. Randomness (serendipity)
    """
    homophily_score = compute_homophily(user_a, user_b)
    attractiveness_compat = compute_attraction(user_a, user_b)
    random_factor = np.random.beta(2, 5)  # skewed toward 0
    
    match_prob = (
        0.4 * homophily_score +
        0.3 * attractiveness_compat +
        0.3 * random_factor
    )
    return np.random.random() < match_prob
```

#### Conversation Agent

Each user is an LLM-based agent with:
- **System prompt**: Persona matching profile
- **Strategy**: Opening approach, escalation style, rejection threshold
- **Memory**: Previous messages in this conversation
- **Goals**: Win user interest, test boundaries, maintain authenticity

```python
class ConversationAgent:
    def __init__(self, user_profile, strategy="default"):
        self.profile = user_profile
        self.strategy = strategy
        self.conversation_history = []
    
    def generate_opener(self, matched_user):
        """First message based on matched user's profile"""
        prompt = f"""You are {self.profile.name}, a {self.profile.age}yo {self.profile.gender}.
        Your profile says: {self.profile.bio}
        
        You just matched with {matched_user.name}. Their profile says: {matched_user.bio}
        
        Write a natural, engaging first message. Be yourself.
        Strategy: {self.strategy}
        Keep it under 100 words."""
        
        return openai.ChatCompletion.create(...)
    
    def respond(self, incoming_message):
        """Generate response to message"""
        # Update conversation history
        # Generate next message based on strategy
        # Check rejection threshold
        pass
```

#### Strategies (Experimental Conditions)

```python
STRATEGIES = {
    "casual": "Friendly, low-stakes conversation. Light jokes.",
    "direct": "Straight to point. Suggest meeting quickly.",
    "romantic": "Compliments, interest in deeper connection.",
    "investigative": "Ask questions about background, interests.",
    "playful": "Teasing, witty, sexual undertones.",
    "formal": "Professional, respect boundaries.",
}
```

#### Conversation Flow

```
1. User A opens (msg 1)
2. User B responds (msg 2)
3. Continue until:
   - MAX_TURNS (20-30 messages)
   - One user stops responding
   - Conversation concludes (exchange contact info)
   - One party requests to meet
```

### Phase 3: Analysis Layer

#### Homophily Analysis
```python
class HomophilyAnalyzer:
    def analyze(self, conversation_pairs):
        """
        Do actual matches show homophily?
        
        Metrics:
        1. Demographic similarity score
           - age diff: |a1 - a2|
           - race match: a1.race == a2.race ? 1 : 0
           - education match: normalize(|ed1 - ed2|)
        
        2. Trait similarity
           - Big Five correlation
           - Personality alignment
        
        3. Preference verification
           - Did they match within stated preferences?
           - Did homophily preferences predict matches?
        
        Output: 
        - Homophily coefficient (correlation of similarity to matching)
        - Demographic heatmaps (who matches with whom)
        - Preference satisfaction (stated vs actual)
        """
        pass
```

#### Gender Dynamics
```python
class GenderDynamicsAnalyzer:
    def analyze(self, conversations):
        """
        Who initiates? Who escalates? Who rejects?
        
        Metrics:
        1. Initiation patterns
           - % of M openers vs F openers
           - Opening strategy by gender (direct vs casual)
           - Response rates to different opener types
        
        2. Conversation escalation
           - Compliment frequency (who gives, who receives)
           - Topic progression (personal → physical → meeting)
           - Message length/effort over time
        
        3. Rejection patterns
           - Who drops out first?
           - Response decay rate
           - Explicit vs implicit rejection
        
        4. Tone analysis
           - Politeness (female > male?)
           - Flirtation intensity
           - Emotional disclosure
        
        Disaggregate by:
        - M initiating F vs F initiating M
        - Same-gender conversations
        - Different strategies by gender
        """
        pass
```

#### Erotic Capital Analysis
```python
class EroticCapitalAnalyzer:
    """
    Erotic capital = physical attractiveness claims in conversation
    
    Signals:
    1. Direct: "I'm told I'm attractive", "fit/athletic"
    2. Indirect: Photo descriptions, compliment fishing
    3. Physical: Body part mentions, fitness references
    4. Flirtation: Sexual innuendo, compliments received
    5. Escalation: Quick move to physical/meeting
    """
    
    def analyze(self, conversations):
        """
        Extract erotic capital signals and their effects
        
        Metrics:
        1. Signal frequency
           - msgs/total physical references
           - erotic_signals/total_messages
        
        2. Signal types (taxonomy)
           - Explicit claims of attractiveness
           - Implicit demonstrations (photos, lifestyle)
           - Responses to compliments
           - Initiation of physical topics
        
        3. Response patterns
           - Does high erotic signal → faster escalation?
           - Does it → more/longer responses?
           - Does it → successful meeting?
        
        4. Gender differences
           - Who uses erotic signals more?
           - What types by gender?
           - Effectiveness differences?
        """
        pass
```

#### Power Dynamics
```python
class PowerDynamicsAnalyzer:
    """
    Power = who controls conversation direction?
    
    Indicators:
    1. Topic control (who suggests topics)
    2. Message frequency (who talks more)
    3. Question vs statement ratio
    4. Agreement patterns
    5. Escalation (who suggests next step)
    """
    
    def analyze(self, conversations):
        """
        Who has conversational power?
        
        Metrics:
        1. Message frequency
           - msgs_count by speaker
           - word_count by speaker
           - q_a_ratio (questions asked)
        
        2. Topic initiation
           - topic_shifts (who introduces new topics)
           - topic_acceptance (does other person follow)
        
        3. Escalation control
           - who suggests meeting
           - who suggests physical contact
           - who terminates
        
        4. Agreement patterns
           - mirroring/matching behavior
           - accommodation (linguistic)
        
        Disaggregate by:
        - Gender pairings
        - Demographic differences
        - Erotic capital differences
        """
        pass
```

#### Linguistic Analysis
```python
class LinguisticAnalyzer:
    """
    Communication style analysis
    """
    
    def analyze(self, conversations):
        """
        1. Formality (casual vs formal language)
        2. Humor (joke frequency, types)
        3. Emotion words (positive/negative/neutral)
        4. Self-disclosure (personal information shared)
        5. Compliments (frequency, sincerity cues)
        6. Agreement signals
        7. Politeness markers
        8. Sexual/romantic language
        
        Analysis:
        - By gender
        - By strategy
        - By demographic pairing
        - Correlation with outcomes (meeting, continuation)
        """
        pass
```

### Phase 4: Statistical Analysis

#### Methods

```python
class StatisticalAnalysis:
    def analyze(self, results):
        """
        1. Descriptive statistics
           - Means, medians, distributions
           - By demographic group
        
        2. Correlation analysis
           - Homophily → matching?
           - Erotic capital → response rate?
           - Strategy → outcome?
        
        3. Regression models
           - DV: Meeting probability / Conversation length / Response rate
           - IV: Demographics, homophily, signals, strategy
           - Controls: Random effects by user
        
        4. Fairness metrics
           - Are outcomes equal across groups?
           - If not, what drives disparities?
        
        5. Effect sizes
           - How big are gender differences?
           - How much does homophily matter?
        
        6. Hypothesis testing
           - Explicit tests of research questions
           - Multiple comparison corrections
        
        Outputs:
        - Summary statistics tables
        - Regression tables
        - Fairness dashboards
        - Confidence intervals
        """
        pass
```

#### Disaggregation

All analyses MUST disaggregate by:
- Gender (M, F, NB separately)
- Race/ethnicity
- Age groups
- Education level
- Relationship to erotic capital distribution

Why? To detect (and report) differential effects.

### Phase 5: Visualization & Research Output

#### Dashboards
```
1. Homophily Dashboard
   - Demographic mixing matrix (race/gender/age)
   - Preference satisfaction plots
   - Homophily coefficient by group

2. Gender Dynamics Dashboard
   - Who initiates (pie chart by gender)
   - Conversation length by gender pairing
   - Topic progression over conversation time

3. Power Analysis
   - Message frequency heatmap
   - Topic initiation network graph
   - Escalation patterns by group

4. Erotic Capital
   - Signal frequency distribution
   - Correlation with outcomes
   - Disaggregation by gender

5. Statistical Summary
   - Key findings table
   - Effect sizes
   - Confidence intervals
```

#### Publication Artifacts
```
outputs/
├── figures/
│   ├── figure_1_homophily_matrix.pdf
│   ├── figure_2_gender_dynamics.pdf
│   ├── figure_3_power_analysis.pdf
│   └── ...
├── tables/
│   ├── table_1_summary_stats.csv
│   ├── table_2_regression_results.csv
│   └── ...
├── report.pdf
└── supplementary_materials/
    ├── full_regression_tables.csv
    ├── demographic_breakdowns.xlsx
    └── methodology_details.md
```

## Reproducibility

### Version Control
- All code in git with commit messages
- All data generation scripts deterministic (seeds fixed)
- All random seeds documented
- All hyperparameters in config files

### Docker Environment
```dockerfile
FROM python:3.10
RUN pip install -r requirements.txt
WORKDIR /research
COPY . .
CMD ["python", "-m", "tinder_research.experiments.run_all"]
```

### Run Scripts
```bash
# Reproduce exact experiment
./scripts/reproduce_experiment_1.sh

# Generate all figures
python -m tinder_research.visualization.generate_all_figures

# Run statistical tests
python -m tinder_research.analysis.run_statistics
```

## Limitations

This research CAN answer:
- Do synthetic users show homophily preferences?
- What conversation patterns emerge with different strategies?
- How do synthetic gender representations affect interactions?
- Can we identify erotic capital signals in text?

This research CANNOT answer:
- Do REAL Tinder users behave this way?
- What causes homophily (preference vs opportunity)?
- Real human psychology of dating apps
- Actual meeting/relationship outcomes

**Generalization**: Results on synthetic data are models of possible patterns, not reflections of real behavior.

## Ethics Checkpoints

- [x] No real user data
- [x] All synthetic generation documented
- [x] LLM prompts designed to avoid harmful stereotyping
- [x] Results disaggregated by demographics
- [x] Limitations clearly stated
- [x] Bias assessment complete
- [x] Designed for research publication, not platform abuse

See `ETHICS_FRAMEWORK.md` for more.

## Timeline

- Week 1-2: Setup, generate users, test agents
- Week 3-4: Run conversations (10k simulations)
- Week 5-6: Analysis pipeline (homophily, gender, power)
- Week 7-8: Visualization and statistics
- Week 9-10: Write paper, prepare figures
- Week 11-12: Refinement, submission prep
