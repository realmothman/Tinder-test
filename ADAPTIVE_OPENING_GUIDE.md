# 🎯 Guia: Adaptive Opening Message Generator

## O que é?

Um sistema inteligente que **aprende com suas mensagens bem-sucedidas** e gera aberturas (opening messages) customizadas para cada novo match.

## Como Funciona

### 1. **Análise do Histórico**
```python
generator = AdaptiveOpeningMessageGenerator(seu_historico_de_conversas)
```

O gerador analisa:
- ✅ Quais opening messages receberam resposta rápida
- ✅ Quais conversas duraram mais (engagement)
- ✅ Padrões: emojis, perguntas, menção de perfil
- ✅ Tópicos que funcionam melhor
- ✅ Qual tipo de perfil responde melhor (idade, gênero, educação)

### 2. **Scoring de Sucesso**

Cada opening é avaliada por:
```python
success_score = (resposta_rápida + conversa_prolongada) / 2
```

**Exemplo:**
- Mensagem 1: "Oi Marina! Vi que você curte cinema francês, qual é seu favorito? 🎬"
  - Resposta em 45s ✅
  - Conversa com 3+ mensagens ✅
  - **Score: 0.75** (bem-sucedida)

- Mensagem 2: "Oi! Como seu dia está?"
  - Sem resposta ❌
  - **Score: 0** (falha)

### 3. **Geração Adaptativa**

Para novo match, o sistema:
1. **Seleciona melhor template** - baseado em similaridade de perfil
2. **Adapta aos dados reais** - nome, profissão, bio
3. **Mantém padrões bem-sucedidos** - emojis, perguntas, tom
4. **Fornece score de confiança** - baseado em histórico

## Exemplo Prático

### Seus Dados Históricos
```python
historico = [
    {
        'messages': [
            {'content': 'Oi Marina! Vi que você curte cinema, qual é seu favorito? 🎬'},
            {'content': 'Truffaut! Você tem bom gosto'},
            {'content': 'Exato, perfeito!'},
        ],
        'response_times': [45.0],  # respondeu em 45 segundos
        'profile': {
            'name': 'Marina',
            'age': 28,
            'gender': 'F',
            'profession': 'Jornalista',
            'bio': 'Cinema, viagens, café',
            'education_level': 'bachelor',
            'location': 'São Paulo'
        }
    },
    # ... mais conversas
]
```

### Novo Match
```python
novo_match = {
    'name': 'Ana',
    'age': 27,
    'gender': 'F',
    'profession': 'Arquiteta',
    'bio': 'Design, viagens, bom papo',
    'education_level': 'master',
    'location': 'São Paulo'
}

# Gerar opening inteligente
message, metadata = generator.generate_opening(novo_match)

print(message)
# Output: "Oi Ana! Vi que você curte design, qual é seu favorito? 🎬"

print(metadata)
# {
#   'strategy': 'adaptive',
#   'confidence': 0.75,  # 75% de confiança baseado no histórico
#   'expected_response_rate': 1.0,  # 100% de chance de resposta
#   'profile_match_score': 0.85  # Muito similar à Marina
# }
```

## Padrões Detectados Automaticamente

### Taxa de Sucesso
```
✓ Mensagens com emoji: 100% de resposta
✓ Mensagens com pergunta: 100% de resposta
✓ Mensagens mencionando perfil: 100% de resposta
```

### Comprimento Ideal
```
Comprimento médio: ~67 caracteres
- Muito curto (<40): Parece desinteressado
- Muito longo (>150): Parece desesperado
```

### Tópicos Que Funcionam
```python
common_topics = generator.extract_common_topics()
# ['cinema', 'viagens', 'arte', 'musica', 'livros']
```

### Perfis Que Respondem Melhor
```python
profile_success = generator.get_profile_success_mapping()
# {
#   'age:25-30': 0.95,      # Muito responsivo
#   'age:30-35': 0.65,      # Menos responsivo
#   'gender:F': 0.85,       # Mulheres respondem mais (seu caso)
#   'edu:master': 0.92,     # Mestrado = mais engagement
# }
```

## Usando com Seu Bot

### 1. Exportar Histórico Real
```python
# Do seu banco de dados ou arquivos JSON
conversas_passadas = load_from_database()  # ou JSON

# Criar gerador
generator = AdaptiveOpeningMessageGenerator(conversas_passadas)
```

### 2. Para Cada Novo Match
```python
# Ao receber novo match
novo_match = fetch_match_profile(match_id)

# Gerar opening inteligente
opening_message, metadata = generator.generate_opening(novo_match)

# Enviar para Tinder
bot.send_message(match_id, opening_message)

# Rastrear resultado
track_message(opening_message, metadata, match_id)
```

### 3. Feedback Loop
```python
# Depois de X horas, se recebeu resposta:
response_received = check_response(match_id)

if response_received:
    # Adicionar ao histórico como sucesso
    generator.successful_openings.append(SuccessfulOpening(...))
    
    # Recalcular padrões
    generator._analyze_history()

# Exportar insights periódico
generator.export_insights('opening_insights_v2.json')
```

## Métodos Principais

### `generate_opening(profile: Dict) -> Tuple[str, Dict]`
Gera opening message para novo match.

```python
message, metadata = generator.generate_opening({
    'name': 'Ana',
    'age': 27,
    'profession': 'Arquiteta',
    'bio': 'Design, viagens',
    'education_level': 'master',
    'location': 'São Paulo'
})

print(message)       # "Oi Ana! Vi que você curte design..."
print(metadata)      # {'strategy': 'adaptive', 'confidence': 0.75, ...}
```

### `get_patterns() -> Dict`
Extrai padrões de sucesso.

```python
patterns = generator.get_patterns()
# {
#   'avg_length': 67,
#   'emoji_usage': 1.0,      # 100% com emoji
#   'question_rate': 1.0,     # 100% com pergunta
#   'mention_profile': 1.0,   # 100% menciona nome
#   'avg_success_score': 0.75
# }
```

### `extract_common_topics() -> List[str]`
Tópicos que funcionam.

```python
topics = generator.extract_common_topics()
# ['cinema', 'viagens', 'arte', 'musica']
```

### `get_profile_success_mapping() -> Dict[str, float]`
Qual tipo de perfil responde melhor.

```python
mapping = generator.get_profile_success_mapping()
# {
#   'age:25-30': 0.95,
#   'gender:F': 0.85,
#   'edu:master': 0.92
# }
```

### `export_insights(filename: str)`
Exporta relatório JSON com tudo.

```python
insights = generator.export_insights('meu_analise.json')
# Salva em opening_insights.json
```

## Fluxo Completo de Integração

```
┌─────────────────────┐
│  HISTÓRICO PASSADO  │
│  (20-50 conversas)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  AdaptiveOpeningMessageGenerator    │
│  - Analisa padrões de sucesso      │
│  - Extrai tópicos comuns           │
│  - Mapeia perfis responsivos       │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────┐
│   NOVO MATCH        │
│   (Ana, 27, Design) │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  Gerar Opening Inteligente           │
│  - Selecionar melhor template        │
│  - Adaptar para Ana                  │
│  - Calcular confidence score         │
└──────────┬───────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  "Oi Ana! Vi que você curte design, │
│   qual é seu projeto favorito? 🎬"  │
│  Confidence: 75%, Expected: 100%    │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Enviar para Tinder │
│  Rastrear resposta  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Feedback Loop                      │
│  - Recebeu resposta? ✓              │
│  - Adicionar ao histórico           │
│  - Retraining dos padrões           │
└─────────────────────────────────────┘
```

## Recomendações

### ✅ Para Bons Resultados
1. **Coletar mínimo 20-30 conversas** antes de usar gerador
2. **Marcas claras de sucesso**: resposta em <5 min + conversa >5 msgs
3. **Atualizações periódicas**: retraining a cada 10 novas conversas
4. **A/B testing**: testar 2 versões de opening paralelas

### ❌ Armadilhas
- Usar com muito poucos dados (<5 conversas)
- Templates muito genéricos perdem adaptabilidade
- Não atualizar após feedback
- Ignorar mudanças sazonais (padrões mudam)

## Próximos Passos

1. **Exportar seu histórico real** de conversas
2. **Converter para formato esperado** do gerador
3. **Treinar gerador** com seus dados
4. **Testar em 5-10 novos matches**
5. **Medir: taxa de resposta % antes vs depois**
6. **Refinar padrões** baseado em resultados

---

**Resumo**: Este sistema transforma seu histórico de sucesso em um "maestro de aberturas" inteligente que entende exatamente o que funciona para você! 🎯
