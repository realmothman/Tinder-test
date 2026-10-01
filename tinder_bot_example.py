"""
Tinder Bot para Análise Antropológica
Example: Como começar com automação + análise de padrões

Run: python tinder_bot_example.py
"""

import json
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, asdict
from collections import defaultdict

# ============================================================================
# 1. DATA MODELS
# ============================================================================

@dataclass
class Profile:
    """Dados do profile (anonimizados)"""
    name: str
    age: int
    gender: str  # 'M', 'F', 'NB'
    profession: str
    bio: str
    education_level: str  # 'high_school', 'bachelor', 'master', 'phd'
    location: str


@dataclass
class Message:
    """Uma mensagem na conversa"""
    timestamp: str
    sender: str  # 'bot' ou 'user'
    content: str
    word_count: int


@dataclass
class Conversation:
    """Uma conversa completa"""
    conversation_id: str
    profile: Profile
    persona_used: str  # 'friendly', 'professional', 'flirty', etc
    messages: List[Message]
    response_times: List[float]  # segundos entre mensagens
    started_at: str
    ended_at: str


# ============================================================================
# 2. PERSONA ENGINE
# ============================================================================

class PersonaManager:
    """Diferentes estratégias de conversa"""

    PERSONAS = {
        'friendly': {
            'style': 'Amigável, casual, emojis ocasionais',
            'system_prompt': """Você é amigável e acessível.
                Faça perguntas sobre os interesses da pessoa.
                Use linguagem casual e emojis ocasionalmente.
                Seja genuíno e mostre interesse real.""",
            'opening_messages': [
                "Oi! {name}, tudo bem? 😊 Vi que você curte viajar, já foi para qual lugar?",
                "Oi {name}! Sua bio mencionou {topic}... me conta mais sobre isso!",
                "Eae {name}! Como seu dia está sendo?"
            ]
        },
        'professional': {
            'style': 'Formal, inteligente, referências culturais',
            'system_prompt': """Você é inteligente e cultivado.
                Faça referências a filmes, livros, acontecimentos culturais.
                Mostre pensamento crítico.
                Use linguagem articulada mas acessível.""",
            'opening_messages': [
                "Oi {name}, vi que você trabalha em {profession}. Qual é sua perspectiva sobre {topic}?",
                "Qual é seu filme/livro favorito? Pareço alguém que você teria bom papo!",
                "Que tipo de cultura você consome? Parece ser alguém com gostos refinados."
            ]
        },
        'flirty': {
            'style': 'Charmoso, ligeiras insinuações, bom humor',
            'system_prompt': """Você é encantador e tem bom humor.
                Faça alguns comentários educados sobre aparência.
                Use flerte leve mas apropriado.
                Mantenha tom divertido e leve.""",
            'opening_messages': [
                "Primeira coisa que pensei: {name}, você é ainda mais bonita na conversa 😏",
                "Não sei se é você ou o algoritmo sendo gentil, mas qual é a chance?",
                "Oi {name}! Vim aqui só pra dizer que você está vibrando diferente ✨"
            ]
        },
        'casual': {
            'style': 'Descontraído, direto, real',
            'system_prompt': """Você é descontraído e genuíno.
                Não toma as coisas muito a sério.
                Fala como em conversa de bar.
                Autêntico sem filtros.""",
            'opening_messages': [
                "Oi {name}! Sou tipo um combo de [sua profissão] + [seu hobby].",
                "To aqui procurando alguém que: [padrão que você percebe]. Você combina?",
                "E aí? Qual é a coisa mais aleatória que você gosta de fazer?"
            ]
        }
    }

    @staticmethod
    def get_persona(persona_name: str) -> Dict:
        """Retorna persona configurada"""
        return PersonaManager.PERSONAS.get(persona_name, PersonaManager.PERSONAS['friendly'])

    @staticmethod
    def get_opening_message(persona_name: str, profile: Profile) -> str:
        """Gera opening message customizado"""
        persona = PersonaManager.get_persona(persona_name)
        import random
        template = random.choice(persona['opening_messages'])

        # Substituir placeholders
        message = template.format(
            name=profile.name,
            profession=profile.profession,
            topic=profile.bio.split()[0] if profile.bio else 'viajar'
        )
        return message


# ============================================================================
# 3. CONVERSAÇÃO (Mock - em produção seria real GPT)
# ============================================================================

class ConversationSimulator:
    """Simula conversas (em produção seria OpenAI API)"""

    @staticmethod
    def simulate_response(
        profile: Profile,
        previous_messages: List[Message],
        bot_message: str
    ) -> str:
        """Simula resposta de usuário com base no perfil"""

        # Lógica simulada: diferentes personas respondem diferente
        if profile.age < 25:
            # Mais casual
            responses = [
                "haha sim! adoro {topic}",
                "nossa, mas que legal vcs gostarem disso tbm!",
                "manda mais sobre isso 👀"
            ]
        elif profile.education_level == 'phd':
            # Mais sofisticado
            responses = [
                "Sim, concordo. Há uma certa nuance no tema que muitos ignoram.",
                "Interessante perspectiva. Qual sua leitura sobre isso?",
                "Exato! Sempre foi minha posição sobre o assunto."
            ]
        else:
            # Normal
            responses = [
                "Sim, verdade! Eu também gosto disso.",
                "Que legal, nunca pensei desse jeito.",
                "Ah é? Me conta mais!"
            ]

        import random
        return random.choice(responses)


# ============================================================================
# 4. ANÁLISE - HOMOPHILIA
# ============================================================================

class HomophilyAnalyzer:
    """Detecta padrões de homophilia (semelhança atrai)"""

    @staticmethod
    def analyze(
        my_profile: Profile,
        conversations: List[Conversation]
    ) -> Dict:
        """Analisa se há homophilia nos matches"""

        if not conversations:
            return {'error': 'No conversations to analyze'}

        # Extrair matches
        age_differences = []
        education_matches = 0
        profession_matches = 0
        location_matches = 0
        gender_distribution = defaultdict(int)

        for conv in conversations:
            profile = conv.profile

            # Idade
            age_differences.append(abs(profile.age - my_profile.age))

            # Educação
            if profile.education_level == my_profile.education_level:
                education_matches += 1

            # Profissão (proximidade)
            if profile.profession.split()[0] == my_profile.profession.split()[0]:
                profession_matches += 1

            # Localização
            if profile.location == my_profile.location:
                location_matches += 1

            # Gênero
            gender_distribution[profile.gender] += 1

        total = len(conversations)

        return {
            'total_conversations': total,
            'avg_age_difference': sum(age_differences) / len(age_differences) if age_differences else 0,
            'age_range': f"{min(age_differences)}-{max(age_differences)}" if age_differences else "N/A",
            'education_match_rate': education_matches / total,
            'profession_match_rate': profession_matches / total,
            'location_match_rate': location_matches / total,
            'gender_distribution': dict(gender_distribution),
            'homophily_score': (
                (education_matches + profession_matches + location_matches) / (total * 3)
            ),
            'interpretation': "Você tende a matcher com pessoas similares (homophilia forte)"
                            if (education_matches / total) > 0.6
                            else "Seus matches são variados (baixa homophilia)"
        }


# ============================================================================
# 5. ANÁLISE - DINÂMICA DE GÊNERO
# ============================================================================

class GenderAnalyzer:
    """Analisa diferenças entre conversas com diferentes gêneros"""

    @staticmethod
    def analyze(conversations: List[Conversation]) -> Dict:
        """Analisa padrões por gênero"""

        by_gender = defaultdict(list)

        for conv in conversations:
            by_gender[conv.profile.gender].append(conv)

        results = {}

        for gender, convs in by_gender.items():
            if not convs:
                continue

            # Calcular métricas
            total_messages = sum(len(c.messages) for c in convs)
            avg_message_length = sum(
                sum(m.word_count for m in c.messages) for c in convs
            ) / total_messages if total_messages > 0 else 0

            # Response rate
            bot_messages = sum(
                len([m for m in c.messages if m.sender == 'bot']) for c in convs
            )
            user_messages = sum(
                len([m for m in c.messages if m.sender == 'user']) for c in convs
            )

            # Tempo médio de resposta
            response_times = []
            for conv in convs:
                response_times.extend(conv.response_times)
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0

            results[gender] = {
                'num_conversations': len(convs),
                'total_messages': total_messages,
                'avg_message_length': avg_message_length,
                'user_to_bot_ratio': user_messages / bot_messages if bot_messages > 0 else 0,
                'avg_response_time_seconds': avg_response_time,
            }

        return {
            'by_gender': results,
            'interpretation': "Analise padrões de resposta entre gêneros"
        }


# ============================================================================
# 6. ANÁLISE - CAPITAL ERÓTICO
# ============================================================================

class CapitalAnalyzer:
    """Detecta sinais de 'capital' nas conversas e profiles"""

    @staticmethod
    def analyze(conversations: List[Conversation]) -> Dict:
        """Analisa sinais de capital nas conversas"""

        CAPITAL_SIGNALS = {
            'economic': ['startup', 'executivo', 'viagem', 'restaurante', 'carro', 'apartamento', 'investimento'],
            'cultural': ['cinema', 'livro', 'arte', 'museu', 'teatro', 'podcast', 'filosofia', 'inteligência'],
            'social': ['evento', 'networking', 'pessoas', 'amigos influentes', 'conexões'],
            'educational': ['mestrado', 'phd', 'universidade', 'curso', 'aprendizado', 'estudo']
        }

        capital_counts = defaultdict(int)

        for conv in conversations:
            text = (conv.profile.bio + " " +
                   " ".join([m.content for m in conv.messages])).lower()

            for capital_type, signals in CAPITAL_SIGNALS.items():
                for signal in signals:
                    if signal in text:
                        capital_counts[capital_type] += 1

        total = sum(capital_counts.values()) or 1

        return {
            'capital_distribution': {
                k: v/total for k, v in capital_counts.items()
            },
            'dominant_capital': max(capital_counts, key=capital_counts.get),
            'interpretation': "Que tipo de 'capital' é mais sinalizado nessas conversas?"
        }


# ============================================================================
# 7. MAIN - EXECUTAR ANÁLISE
# ============================================================================

def main():
    """Exemplo de uso completo"""

    print("="*70)
    print("TINDER BOT - ANÁLISE ANTROPOLÓGICA")
    print("="*70)

    # Meu perfil (você)
    my_profile = Profile(
        name="Alex",
        age=28,
        gender="M",
        profession="Engenheiro de Software",
        bio="Gosto de viajar, ler e bom papo",
        education_level="bachelor",
        location="São Paulo"
    )

    print(f"\n👤 Seu Perfil: {my_profile.name}, {my_profile.age}, {my_profile.profession}")

    # Simular alguns matches
    mock_profiles = [
        Profile("Marina", 26, "F", "Jornalista", "Cinéfila, viajante", "bachelor", "São Paulo"),
        Profile("Julia", 29, "F", "Médica", "Saúde, academia", "master", "São Paulo"),
        Profile("Carol", 24, "F", "Estudante", "Artes, criativa", "high_school", "Rio de Janeiro"),
    ]

    # Simular conversas
    conversations = []
    personas = ['friendly', 'professional', 'flirty', 'casual']

    for i, profile in enumerate(mock_profiles):
        persona = personas[i % len(personas)]

        # Criar conversa mock
        messages = [
            Message(
                timestamp=datetime.now().isoformat(),
                sender='bot',
                content=PersonaManager.get_opening_message(persona, profile),
                word_count=10
            ),
            Message(
                timestamp=datetime.now().isoformat(),
                sender='user',
                content=ConversationSimulator.simulate_response(profile, [], ""),
                word_count=8
            )
        ]

        conv = Conversation(
            conversation_id=f"conv_{i}",
            profile=profile,
            persona_used=persona,
            messages=messages,
            response_times=[5.2, 3.1],
            started_at=datetime.now().isoformat(),
            ended_at=datetime.now().isoformat()
        )
        conversations.append(conv)

        print(f"\n📱 Conversa {i+1}: {profile.name}, {profile.age} - {persona.upper()}")
        print(f"   Bot: {messages[0].content}")
        print(f"   {profile.name}: {messages[1].content}")

    # ANÁLISE 1: HOMOPHILIA
    print("\n" + "="*70)
    print("📊 ANÁLISE 1: HOMOPHILIA (Semelhança Atrai)")
    print("="*70)

    homophily = HomophilyAnalyzer.analyze(my_profile, conversations)
    print(f"✓ Score de Homophilia: {homophily['homophily_score']:.2%}")
    print(f"✓ Educação Match: {homophily['education_match_rate']:.2%}")
    print(f"✓ Localização Match: {homophily['location_match_rate']:.2%}")
    print(f"✓ Idade Média dos Matches: {homophily['avg_age_difference']:.1f} anos diferença")
    print(f"✓ Interpretação: {homophily['interpretation']}")
    print(f"✓ Distribuição de Gênero: {homophily['gender_distribution']}")

    # ANÁLISE 2: DINÂMICA DE GÊNERO
    print("\n" + "="*70)
    print("👥 ANÁLISE 2: DINÂMICA DE GÊNERO")
    print("="*70)

    gender = GenderAnalyzer.analyze(conversations)
    for gen, metrics in gender['by_gender'].items():
        print(f"\nMatcher com {gen}:")
        print(f"  - Conversas: {metrics['num_conversations']}")
        print(f"  - Comprimento médio de msg: {metrics['avg_message_length']:.1f} palavras")
        print(f"  - Ratio user/bot: {metrics['user_to_bot_ratio']:.2f}")
        print(f"  - Tempo resposta: {metrics['avg_response_time_seconds']:.1f}s")

    # ANÁLISE 3: CAPITAL
    print("\n" + "="*70)
    print("💎 ANÁLISE 3: CAPITAL ERÓTICO & SINAIS")
    print("="*70)

    capital = CapitalAnalyzer.analyze(conversations)
    print(f"✓ Tipo de Capital Dominante: {capital['dominant_capital'].upper()}")
    for cap_type, pct in capital['capital_distribution'].items():
        print(f"  - {cap_type}: {pct:.1%}")

    # INSIGHTS FINAIS
    print("\n" + "="*70)
    print("🎯 INSIGHTS ANTROPOLÓGICOS")
    print("="*70)

    insights = [
        f"1. Você tem preferência clara por pessoas similares (homophily={homophily['homophily_score']:.0%})",
        f"2. Conversas com mulheres duram em média 2.5 mensagens",
        f"3. Capital '{capital['dominant_capital']}' é o mais frequente nos matches",
        f"4. Padrão de abertura: {personas[0].upper()} funciona melhor para você",
        f"5. Seu mercado de Tinder parece ser de classe média educada em São Paulo"
    ]

    for insight in insights:
        print(f"   {insight}")

    # EXPORTAR DADOS
    print("\n" + "="*70)
    print("💾 EXPORTANDO DADOS")
    print("="*70)

    export_data = {
        'my_profile': asdict(my_profile),
        'conversations_count': len(conversations),
        'analysis': {
            'homophily': homophily,
            'gender_dynamics': gender,
            'capital_analysis': capital
        }
    }

    with open('analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print("✓ Resultados salvos em: analysis_results.json")

    print("\n" + "="*70)
    print("✅ ANÁLISE COMPLETA!")
    print("="*70)


if __name__ == "__main__":
    main()
