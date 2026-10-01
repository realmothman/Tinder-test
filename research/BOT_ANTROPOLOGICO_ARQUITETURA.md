# 🤖 Tinder Conversation Bot + Anthropological Analysis

## Visão Geral do Projeto

**Objetivo**: Um bot que conversa com matches do Tinder, coleta dados de conversas, e analisa padrões antropológicos automaticamente.

**Diferencial**: Não é só automação - é uma **ferramenta de research** que coleta dados para análise científica.

---

## 🏗️ ARQUITETURA DO SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│                   TINDER CONVERSATION BOT                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐         ┌──────────────────┐           │
│  │  AUTOMATION     │         │  CONVERSATION    │           │
│  │  LAYER          │────────▶│  GENERATION      │           │
│  │                 │         │  (LLM/GPT)       │           │
│  │ - Login Tinder  │         └──────────────────┘           │
│  │ - Auto-swipe    │                 │                       │
│  │ - Get matches   │                 ▼                       │
│  │ - Send message  │         ┌──────────────────┐           │
│  │                 │         │  PERSONA         │           │
│  └─────────────────┘         │  MANAGEMENT      │           │
│           │                  │                  │           │
│           │                  │ - Friendly       │           │
│           │                  │ - Professional   │           │
│           │                  │ - Flirty         │           │
│           │                  │ - Casual         │           │
│           │                  └──────────────────┘           │
│           │                          │                       │
│           └──────────────┬───────────┘                       │
│                          ▼                                    │
│         ┌─────────────────────────────┐                      │
│         │    DATA COLLECTION LAYER    │                      │
│         │                             │                      │
│         │ - Store conversations       │                      │
│         │ - Anonymize user data       │                      │
│         │ - Track response patterns   │                      │
│         │ - Metadata (time, gender)   │                      │
│         └─────────────────────────────┘                      │
│                    │                                         │
│                    ▼                                         │
│    ┌────────────────────────────────────────┐               │
│    │  ANTHROPOLOGICAL ANALYSIS LAYER        │               │
│    │                                        │               │
│    │ ┌──────────────────────────────────┐  │               │
│    │ │ NLP Analysis                     │  │               │
│    │ │ - Sentiment (positive/negative)  │  │               │
│    │ │ - Entity extraction (professions)│  │               │
│    │ │ - Topic modeling                 │  │               │
│    │ └──────────────────────────────────┘  │               │
│    │                                        │               │
│    │ ┌──────────────────────────────────┐  │               │
│    │ │ Anthropological Patterns         │  │               │
│    │ │ - Homophilia detection           │  │               │
│    │ │ - Gender dynamics                │  │               │
│    │ │ - Capital signals                │  │               │
│    │ │ - Power dynamics                 │  │               │
│    │ │ - Communication rituals          │  │               │
│    │ └──────────────────────────────────┘  │               │
│    │                                        │               │
│    │ ┌──────────────────────────────────┐  │               │
│    │ │ Statistical Analysis             │  │               │
│    │ │ - Response rates by persona      │  │               │
│    │ │ - Gender differences             │  │               │
│    │ │ - Correlation analysis           │  │               │
│    │ │ - Clustering users               │  │               │
│    │ └──────────────────────────────────┘  │               │
│    └────────────────────────────────────────┘               │
│                    │                                         │
│                    ▼                                         │
│    ┌────────────────────────────────────────┐               │
│    │     OUTPUT & VISUALIZATION LAYER       │               │
│    │                                        │               │
│    │ - Dashboards (Streamlit/Dash)          │               │
│    │ - Graphs & charts                      │               │
│    │ - Statistical reports                  │               │
│    │ - Paper-ready findings                 │               │
│    └────────────────────────────────────────┘               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 ESTRUTURA DO CÓDIGO

```
tinder-bot-research/
│
├── README.md                    # Overview do projeto
├── requirements.txt             # Dependências Python
├── .env.example                 # Template de variáveis de ambiente
├── setup.py                     # Para publicar no PyPI
│
├── tinder_bot/
│   ├── __init__.py
│   │
│   ├── automation/              # AUTOMATION LAYER
│   │   ├── __init__.py
│   │   ├── tinder_api.py        # API wrapper
│   │   ├── browser.py           # Selenium automation
│   │   ├── login.py             # Auth handling
│   │   ├── swiper.py            # Auto-swipe logic
│   │   └── messenger.py         # Message sending
│   │
│   ├── conversation/            # CONVERSATION GENERATION
│   │   ├── __init__.py
│   │   ├── llm_client.py        # OpenAI GPT integration
│   │   ├── persona.py           # Different personalities
│   │   ├── prompt_templates.py  # System prompts
│   │   └── response_generator.py
│   │
│   ├── data/                    # DATA COLLECTION
│   │   ├── __init__.py
│   │   ├── storage.py           # Database (SQLite/PostgreSQL)
│   │   ├── models.py            # ORM models (SQLAlchemy)
│   │   ├── anonymizer.py        # GDPR compliance
│   │   └── backup.py            # Data backup
│   │
│   ├── analysis/                # ANTHROPOLOGICAL ANALYSIS
│   │   ├── __init__.py
│   │   ├── nlp_analysis.py      # Sentiment, entities, topics
│   │   ├── homophily.py         # Homophilia detection
│   │   ├── gender_analysis.py   # Gender dynamics
│   │   ├── capital.py           # Capital signals detection
│   │   ├── rituals.py           # Communication pattern analysis
│   │   └── statistics.py        # Statistical analysis
│   │
│   ├── visualization/           # OUTPUTS
│   │   ├── __init__.py
│   │   ├── dashboard.py         # Streamlit dashboard
│   │   ├── reports.py           # PDF/HTML reports
│   │   ├── charts.py            # Visualization functions
│   │   └── export.py            # Export to CSV/JSON
│   │
│   └── config/
│       ├── __init__.py
│       ├── settings.py          # Config management
│       └── constants.py         # Constants
│
├── notebooks/                   # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_pattern_analysis.ipynb
│   └── 03_anthropological_insights.ipynb
│
├── tests/                       # Unit tests
│   ├── test_automation.py
│   ├── test_conversation.py
│   ├── test_analysis.py
│   └── test_data.py
│
├── docs/
│   ├── METHODOLOGY.md           # Research methodology
│   ├── ETHICS.md                # Ethical considerations
│   ├── INSTALLATION.md          # Setup guide
│   ├── USAGE.md                 # How to use
│   └── API.md                   # Code documentation
│
└── examples/
    ├── basic_usage.py
    ├── custom_persona.py
    └── analysis_example.py
```

---

## 🧪 COMPONENTES PRINCIPAIS

### 1. AUTOMATION LAYER

**O que faz:**
- Login no Tinder (via Selenium + undetected-chromedriver)
- Coleta lista de matches
- Envia mensagens iniciais
- Coleta respostas
- Gerencia conversas

**Código exemplo:**
```python
from tinder_bot.automation import TinderAutomation
from tinder_bot.conversation import ConversationManager

# Inicializar
bot = TinderAutomation(
    email="seu_email@gmail.com",
    password="senha"
)

# Login
bot.login()

# Obter matches
matches = bot.get_matches()

# Para cada match, conversar
for match in matches:
    response = bot.send_message(
        match_id=match['id'],
        message="Oi! Como vai?"
    )
```

### 2. CONVERSATION GENERATION

**O que faz:**
- Gera respostas usando GPT-3/4
- Diferentes personas (friendly, professional, flirty, etc)
- Mantém contexto da conversa
- Simula padrões realistas de resposta

**Código exemplo:**
```python
from tinder_bot.conversation import ConversationManager

# Criar gerenciador com persona específica
conv_manager = ConversationManager(
    persona="friendly",  # ou "professional", "flirty", "casual"
    context_window=5     # últimas 5 mensagens
)

# Gerar resposta
response = conv_manager.generate_response(
    profile_data={
        'name': 'Marina',
        'age': 28,
        'bio': 'Jornalista, amo viajar',
        'photos': ['photo1.jpg', 'photo2.jpg']
    },
    conversation_history=[
        {'role': 'user', 'content': 'Oi! Tudo bem?'},
        {'role': 'assistant', 'content': 'Oi! Tudo certo!'},
        {'role': 'user', 'content': 'Que tipo de música você gosta?'},
    ]
)

print(response)  # "Eu curto bastante indie e eletrônico!"
```

### 3. DATA COLLECTION & STORAGE

**O que armazena:**
```python
# Modelo de conversa
class Conversation(Model):
    id = UUID
    match_id = UUID
    timestamp = DateTime
    
    # Profile data (anonymized)
    profile_age = Integer
    profile_gender = Enum('M', 'F', 'NB')
    profile_profession = String  # "Jornalista" não "Marina é jornalista"
    profile_education = String   # "Ensino Superior"
    profile_location = String    # "São Paulo"
    
    # Messages
    messages = List[Message]
    
    # Analysis results
    sentiment_scores = List[Float]
    detected_entities = List[String]
    topics = List[String]
    homophily_score = Float
    response_time = Float
    conversation_length = Integer
    escalation_pattern = String
    
    # Metadata
    persona_used = String
    language = String
    created_at = DateTime
```

### 4. ANALYSIS LAYER - ANTROPOLÓGICA

**Homophily Detection:**
```python
from tinder_bot.analysis import HomophilyAnalyzer

analyzer = HomophilyAnalyzer()

# Analisar se há homophilia
result = analyzer.analyze(
    my_profile={
        'age': 28,
        'gender': 'M',
        'education': 'Ensino Superior',
        'profession': 'Engenheiro',
        'class': 'middle',
        'location': 'Zona Oeste'
    },
    matches=[
        {'age': 26, 'gender': 'F', 'education': 'ES', 'profession': 'Designer', 'class': 'middle'},
        {'age': 29, 'gender': 'F', 'education': 'ES', 'profession': 'Advogada', 'class': 'upper'},
        # ... mais matches
    ]
)

print(result)
# {
#   'homophily_score': 0.78,  # 0-1 scale
#   'age_similarity': 0.82,
#   'education_match': 0.95,
#   'class_match': 0.70,
#   'analysis': 'Você tem preferência por pessoas com educação similar (homophilia forte)'
# }
```

**Gender Dynamics:**
```python
from tinder_bot.analysis import GenderAnalyzer

gender_analyzer = GenderAnalyzer()

# Comparar padrões por gênero
comparison = gender_analyzer.analyze_patterns(
    conversations_with_women=[...],
    conversations_with_men=[...]
)

print(comparison)
# {
#   'response_rate_women': 0.85,
#   'response_rate_men': 0.62,
#   'avg_message_length_women': 45,
#   'avg_message_length_men': 38,
#   'flirtation_index_women': 0.72,
#   'flirtation_index_men': 0.58,
#   'insight': 'Mulheres tendem responder mais e com mensagens mais longas'
# }
```

**Capital Analysis:**
```python
from tinder_bot.analysis import CapitalAnalyzer

capital = CapitalAnalyzer()

# Detectar sinais de capital em conversas
signals = capital.detect_capital_signals(
    conversation_text="Eu trabalho em startup de IA, acabei de voltar da Europa..."
)

print(signals)
# {
#   'economic_capital': ['startup', 'Europa'],
#   'cultural_capital': ['IA', 'Europa - viagem sofisticada'],
#   'social_capital': ['startup - network'],
#   'education_signals': None,
#   'capital_index': 0.72
# }
```

### 5. VISUALIZATION & OUTPUT

**Dashboard interativo (Streamlit):**
```python
# streamlit run dashboard.py

# Mostra:
# - Gráfico de response rates por persona
# - Distribuição de matches por gênero/idade
# - Padrões de homophilia
# - Sentiment analysis das conversas
# - Clusters de usuários
# - Comparação de estratégias
```

---

## 🔬 FLUXO DE PESQUISA

### Semana 1-2: Setup
```
1. Clone repo
2. Configure Tinder credentials
3. Setup OpenAI API key
4. Run tests
5. Configure database
```

### Semana 3-4: Coleta de Dados
```
1. Bot começa conversando (ex: 50 matches)
2. Coleta todas as conversas
3. Anonimiza dados
4. Armazena em banco de dados
```

### Semana 5-6: Análise
```
1. Roda análises antropológicas
2. Gera gráficos e visualizações
3. Extrai insights
4. Escreve primeiras conclusões
```

### Semana 7-8: Publicação
```
1. Escreve paper
2. GitHub com stars ⭐
3. Publicação em conferência/journal
```

---

## 📊 OUTPUTS ESPERADOS

### Gráficos:
```
1. Response Rate by Persona
2. Homophilia Distribution
3. Gender Dynamics Comparison
4. Capital Signals Frequency
5. Sentiment Over Conversation Time
6. User Clustering (homophily/demographics)
7. Message Length Distribution by Gender
8. Escalation Patterns
```

### Insights Antropológicos:
```
- "75% de homophilia em matches"
- "Mulheres respondem 20% mais que homens"
- "Capital cultural (educação) sinais 3x mais que econômico"
- "Heteronormatividade replicada em padrões de mensagem"
- "Performatividade: bio vs conversa diferem em 40% dos casos"
```

### Paper Exemplo:
```
"Automated Conversation Analysis in Dating Apps: 
Using AI to Study Homophily, Gender Dynamics, and Erotic Capital 
in Tinder Matching Patterns"

Conference: FAccT (Fairness, Accountability, Transparency)
```

---

## ⚖️ ÉTICA & COMPLIANCE

**O projeto DEVE ter:**
```python
# ANONIMIZAÇÃO
├─ Sem nomes reais
├─ Sem fotos
├─ Sem dados de localização exatos
├─ Sem IDs do Tinder
└─ Pseudônimos para análise

# CONSENTIMENTO
├─ Aviso que conversa será analisada?
├─ OU análise apenas de sua própria conversa?
└─ Transparência em metodologia

# DATA PROTECTION
├─ Criptografia de dados
├─ Deletion policy (30 dias?)
├─ GDPR compliance
└─ Data backup seguro

# DOCUMENTATION
├─ ethics/METHODOLOGY.md
├─ Disclosure responsável
└─ Limitações da pesquisa
```

---

## 🎯 POR QUE ISSO MERECE STARS NO GITHUB

**Diferencial:**
1. ✅ Primeira ferramenta que combina automação + análise antropológica
2. ✅ Código clean, bem documentado, testado
3. ✅ Publicável em conferências acadêmicas
4. ✅ Reusável para outros dating apps
5. ✅ Integração com frameworks teóricos
6. ✅ Automated pipeline de research
7. ✅ Abordagem ética e transparente

**Potencial de Publicação:**
- FAccT Conference (Fairness, Accountability, Transparency)
- CSCW (Computer-Supported Cooperative Work)
- Journal of Online Safety Technology
- Sociological Review
- Anthropology of Technology journals

---

## 🚀 PRÓXIMOS PASSOS

1. **Validar Arquitetura**: Qual componente adicionar primeiro?
2. **Escolher Stack**: Python? FastAPI? PostgreSQL?
3. **Prototipo MVP**: Bot simples + análise básica
4. **Pesquisa Piloto**: Testar com 20-30 conversas
5. **Refinar**: Baseado em achados
6. **Publicar**: GitHub + Paper

---

**Isso combina:** Automação + Pesquisa + Análise + GitHub Stars = Impactante! 🚀

