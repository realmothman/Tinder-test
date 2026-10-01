# 🚀 Guia Prático: Sistema Integrado de Bot + Análise Antropológica

## Visão Geral

O sistema `IntegratedBotSystem` combina **5 componentes** em um pipeline único:

```
Seu Histórico
(conversas passadas)
        │
        ▼
Gerador Adaptativo
(aprende padrões)
        │
        ▼
Novo Match
(Ana, 27, Arquiteta)
        │
        ▼
Opening Inteligente
(personalizada + score)
        │
        ├─ Persona Seleção (auto: baseado em perfil)
        │
        ▼
Simulação de Conversa
(4-6 mensagens)
        │
        ├─ Homophilia Analyzer
        ├─ Gender Analyzer
        └─ Capital Analyzer
        │
        ▼
Feedback Loop
(atualiza modelo adaptativo)
        │
        ▼
Relatório JSON
(insights + data)
```

---

## Uso Básico

### 1. Setup Inicial

```python
from integrated_bot_system import IntegratedBotSystem
from tinder_bot_example import Profile

# Seu perfil
my_profile = Profile(
    name="Seu Nome",
    age=28,
    gender="M",
    profession="Profissão",
    bio="Sua bio",
    education_level="bachelor",
    location="São Paulo"
)

# Histórico de conversas passadas (opcional, mas MUITO recomendado)
historico = [
    {
        'messages': [
            {'content': 'Sua mensagem inicial'},
            {'content': 'Resposta dela'}
        ],
        'response_times': [45.0],  # segundos
        'profile': {
            'name': 'Nome',
            'age': 26,
            'gender': 'F',
            'profession': 'Designer',
            'bio': 'Bio dela',
            'education_level': 'bachelor',
            'location': 'São Paulo'
        }
    }
]

# Inicializar sistema
bot = IntegratedBotSystem(my_profile, historico)
```

### 2. Processar Novo Match

```python
novo_match = Profile(
    name="Ana",
    age=27,
    gender="F",
    profession="Arquiteta",
    bio="Design, viagens",
    education_level="master",
    location="São Paulo"
)

# Processar completamente
resultado = bot.process_new_match(novo_match, persona='auto')

print(resultado['opening']['message'])
# Output: "Oi Ana! Vi que você curte design, qual é seu projeto favorito? 🎬"

print(resultado['success'])
# Output: {'got_response': True, 'number_of_turns': 2, 'success_level': 'medium'}
```

### 3. Gerar Relatórios

```python
# Relatório completo com todas as conversas e análises
relatorio = bot.generate_report('meu_relatorio.json')

# Insights do sistema adaptativo
bot.export_insights('meus_insights.json')
```

---

## O que Cada Componente Faz

### 1. **Adaptive Opening Generator**
```python
# Automaticamente:
✓ Analisa quais mensagens funcionaram
✓ Extrai padrões bem-sucedidos
✓ Gera novas baseado em templates comprovados
✓ Adapta para perfil específico
✓ Fornece confidence score
```

**Exemplo:**
```python
opening, metadata = bot.adaptive_generator.generate_opening(novo_match)

# opening:
# "Oi Ana! Vi que você curte design, qual é seu favorito? 🎬"

# metadata:
# {
#   'strategy': 'adaptive',
#   'confidence': 0.75,           # 75% de confiança
#   'profile_match_score': 0.85,  # Muito similar
#   'expected_response_rate': 1.0 # 100% chance
# }
```

### 2. **Persona Selection**
```python
# Automático (persona='auto')
Se education == 'master': professional
Se gender == 'F' + confidence > 0.7: flirty
Padrão: friendly

# Manual: persona='professional' / 'flirty' / etc
```

### 3. **Conversation Simulation**
```python
# Simula 3-4 turnos de conversa realista
# - Bot envia opening inteligente
# - Match responde (baseado em perfil)
# - Bot responde (baseado em persona)
# - Match responde novamente
```

### 4. **Anthropological Analysis**
```python
analysis = resultado['analysis']

# Homophilia: Você matcher com pessoas similares?
analysis['homophily']
# {
#   'homophily_score': 0.78,
#   'education_match_rate': 0.95,
#   'age_range': '25-30',
#   'interpretation': 'Você tende a matcher com pessoas similares'
# }

# Gender Dynamics: Diferenças por gênero?
analysis['gender_dynamics']
# {
#   'by_gender': {
#     'F': {'response_time': 45s, 'message_length': 120 chars}
#   }
# }

# Capital Signals: Que tipo de capital é sinalizado?
analysis['capital_signals']
# {
#   'capital_distribution': {'cultural': 0.6, 'economic': 0.4},
#   'dominant_capital': 'cultural'
# }
```

### 5. **Feedback Loop**
```python
# Automático! A cada conversa:
✓ Calcula success_score
✓ Se score > 0.5: adiciona a successful_openings
✓ Se score < 0.5: adiciona a failed_openings
✓ Próximos matches usam padrões atualizados
```

---

## Workflow Completo: Passo a Passo

### Dia 1-2: Preparação
```python
# Coletar histórico real
historico_real = carregar_do_banco_dados()  # 10-20 conversas

# Ou exportar do Tinder manualmente em JSON

# Criar bot
bot = IntegratedBotSystem(my_profile, historico_real)

# Analisar padrões
print("Padrões detectados:")
print(bot.adaptive_generator.get_patterns())
```

### Dia 3-7: Processar Novos Matches
```python
matches_novos = carregar_matches_nao_processados()

for match in matches_novos:
    # Sistema faz tudo automaticamente
    resultado = bot.process_new_match(match, persona='auto')
    
    # Salvar resultado
    salvar_resultado(resultado)
    
    # Sistema aprende
    # (feedback loop automático)
```

### Dia 8+: Análise e Ajustes
```python
# Gerar relatório
relatorio = bot.generate_report()

# Analisar
print(f"Taxa de sucesso: {relatorio['adaptive_generator_stats']['success_rate']}")
print(f"Personas mais efetivas: {relatorio['aggregate_analysis']}")

# Se taxa baixa:
# 1. Adicionar mais histórico
# 2. Refinar personas
# 3. A/B testar diferentes approaches
```

---

## Saídas (Outputs)

### 1. **integrated_bot_report.json**
```json
{
  "session_timestamp": "2026-10-01T15:30:00",
  "my_profile": {...},
  "conversations_processed": 10,
  "adaptive_generator_stats": {
    "successful_openings": 8,
    "failed_openings": 2,
    "success_rate": 0.80,
    "patterns": {
      "avg_length": 67,
      "emoji_usage": 1.0,
      "question_rate": 1.0,
      "avg_success_score": 0.75
    }
  },
  "aggregate_analysis": {
    "homophily": {...},
    "gender_dynamics": {...},
    "capital": {...}
  },
  "individual_results": [
    {
      "id": "conv_0",
      "profile": {...},
      "messages": [...],
      "success": {...}
    }
  ]
}
```

### 2. **adaptive_insights_final.json**
```json
{
  "total_successful": 8,
  "success_rate": 0.80,
  "patterns": {
    "emoji_usage": 1.0,
    "question_rate": 1.0,
    "mention_profile": 0.95
  },
  "common_topics": ["design", "viagens", "arte"],
  "top_performing_messages": [
    "Oi {name}! Vi que você curte {topic}, qual é seu favorito? 🎬",
    "Que tipo de {topic} você mais gosta?"
  ]
}
```

---

## Personalizações

### 1. **Mudar Estratégia de Persona**
```python
class MeuBot(IntegratedBotSystem):
    def _select_persona(self, persona, profile, opening_metadata):
        # Custom logic
        if profile.profession == 'Designer':
            return 'flirty'
        else:
            return 'professional'
```

### 2. **Customizar Conversation Simulation**
```python
class MeuBot(IntegratedBotSystem):
    def _simulate_conversation(self, profile, opening, persona):
        # Usar GPT real em vez de mock
        # Integrar com OpenAI API
        # Mais turnos de conversa
        pass
```

### 3. **Adicionar Nova Análise**
```python
class MeuBot(IntegratedBotSystem):
    def _anthropological_analysis(self, conversation):
        # Chamar análise original
        analysis = super()._anthropological_analysis(conversation)
        
        # Adicionar nova análise
        analysis['power_dynamics'] = PowerDynamicsAnalyzer.analyze(conversation)
        
        return analysis
```

---

## Métricas Importantes

### Success Rate
```python
success_rate = successful_openings / (successful + failed)
```
**Target:** > 70%

### Response Time
```python
média < 60 segundos = muito bom
60-300 segundos = bom
> 300 segundos = melhorar
```

### Conversation Length
```python
1-2 mensagens = não engajante
3-5 mensagens = bom
6+ mensagens = excelente
```

### Homophily Score
```python
0.0-0.3 = Muito diverso
0.3-0.7 = Moderado
0.7-1.0 = Homofílico (similares)
```

---

## Troubleshooting

### Problema: "Sucesso baixo (< 50%)"
```python
# Solução 1: Adicionar mais histórico
bot.historical_conversations.extend(mais_conversas)
bot.adaptive_generator._analyze_history()

# Solução 2: Ajustar threshold de sucesso
# (editar _update_adaptive_model -> success_score > 0.5)

# Solução 3: Usar personas diferentes
for match in matches:
    resultado = bot.process_new_match(match, persona='professional')
```

### Problema: "Mesma opening para todos"
```python
# Sistema está recombinando a mesma template
# Solução: Adicionar mais histórico diverso
# Com diferentes personas e perfis

historico_diverso = [
    # Conversas com mulheres
    # Conversas com homens
    # Conversas com diferentes idades/profissões
]
```

### Problema: "Análise vazia"
```python
# Precisa de múltiplas conversas para análise agregada
if len(bot.conversation_history) < 5:
    print("Aguarde mais conversas para análise completa")
```

---

## Próximos Passos

1. **Coletar dados reais** (10-20 conversas históricas)
2. **Testar em 5-10 novos matches** para validar
3. **Medir: taxa de resposta antes vs depois**
4. **Refinar baseado em resultados**
5. **Publicar achados** (GitHub + Academia)

---

## Estrutura de Arquivos

```
Tinder-test/
├── tinder_bot_example.py          # Core: perfil, conversa, análise
├── adaptive_opening_generator.py  # Aprendizado adaptativo
├── integrated_bot_system.py       # Sistema integrado (MAIN)
├── ADAPTIVE_OPENING_GUIDE.md
├── INTEGRATED_SYSTEM_GUIDE.md     # Este arquivo
├── integrated_bot_report.json     # Output: relatório
├── adaptive_insights_final.json   # Output: insights
└── research/                      # Documentação teórica
    ├── FRAMEWORKS_ANTROPOLOGICOS.md
    ├── METODOLOGIA_PRATICA_TINDER.md
    └── ...
```

---

## Exemplo Real: Seu Primeiro Uso

```python
# 1. Exportar histórico real do Tinder
# (20 últimas conversas como JSON)

# 2. Executar:
from integrated_bot_system import IntegratedBotSystem
from tinder_bot_example import Profile

my_profile = Profile("Você", 28, "M", "Dev", "Bio real", "bachelor", "SP")
bot = IntegratedBotSystem(my_profile, seu_historico_json)

# 3. Para cada novo match:
novo = Profile("Ana", 27, "F", "Arquiteta", "Design", "master", "SP")
resultado = bot.process_new_match(novo, persona='auto')

# 4. Verificar opening:
print(resultado['opening']['message'])

# 5. Ao final da semana:
relatorio = bot.generate_report()
print(f"Success rate: {relatorio['adaptive_generator_stats']['success_rate']:.0%}")
```

---

**Este é o seu bot antropológico completo! 🚀**
