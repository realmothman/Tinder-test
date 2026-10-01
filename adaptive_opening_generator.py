"""
Adaptive Opening Message Generator
Analisa mensagens bem-sucedidas e gera aberturas inteligentes para novos matches
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import Counter, defaultdict
import re


@dataclass
class SuccessfulOpening:
    """Registro de opening message bem-sucedida"""
    message: str
    response_received: bool
    response_time: float  # segundos
    conversation_length: int  # quantas mensagens tiveram
    match_profile: Dict  # age, gender, profession, bio, education, location
    success_score: float  # 0-1


class AdaptiveOpeningMessageGenerator:
    """
    Gera opening messages adaptativas baseadas no histórico de sucesso
    """

    def __init__(self, conversation_history: List[Dict] = None):
        """
        Args:
            conversation_history: Lista de conversas passadas com metadados
        """
        self.successful_openings: List[SuccessfulOpening] = []
        self.failed_openings: List[str] = []
        self.conversation_history = conversation_history or []
        self._analyze_history()

    def _analyze_history(self):
        """Analisa histórico para extrair padrões bem-sucedidos"""
        for conv in self.conversation_history:
            if not conv.get('messages'):
                continue

            # Primeira mensagem é o opening
            opening = conv['messages'][0].get('content', '')

            # Sucesso = recebeu resposta rápida e conversa prolongada
            got_response = len(conv['messages']) > 1
            response_time = conv.get('response_times', [999])[0] if got_response else 999
            conv_length = len(conv['messages'])

            # Score: resposta rápida (< 5 min) + conversa longa (> 5 msgs)
            success_score = 0.0
            if got_response:
                response_score = max(0, 1 - (response_time / 300))  # max 5 min
                length_score = min(1, conv_length / 10)  # 10+ msgs é perfeito
                success_score = (response_score + length_score) / 2

            if success_score > 0.5:  # Threshold de sucesso
                opening_obj = SuccessfulOpening(
                    message=opening,
                    response_received=got_response,
                    response_time=response_time,
                    conversation_length=conv_length,
                    match_profile=conv.get('profile', {}),
                    success_score=success_score
                )
                self.successful_openings.append(opening_obj)
            else:
                self.failed_openings.append(opening)

    def get_patterns(self) -> Dict:
        """
        Extrai padrões das mensagens bem-sucedidas

        Returns:
            Dict com padrões: opening_length, emoji_usage, question_rate, etc
        """
        if not self.successful_openings:
            return {}

        patterns = {
            'avg_length': 0,
            'emoji_usage': 0,  # % de mensagens com emoji
            'question_rate': 0,  # % de mensagens com ?
            'mention_profile': 0,  # % que mencionam nome/profissão
            'common_topics': [],
            'avg_success_score': 0,
            'top_performers': []
        }

        lengths = []
        emojis_count = 0
        questions_count = 0
        mentions_count = 0

        for opening in self.successful_openings:
            msg = opening.message
            lengths.append(len(msg))

            # Contadores
            if any(ord(c) > 127 for c in msg):  # Emoji detection
                emojis_count += 1
            if '?' in msg:
                questions_count += 1
            if opening.match_profile.get('name') in msg or \
               opening.match_profile.get('profession') in msg:
                mentions_count += 1

        total = len(self.successful_openings)
        patterns['avg_length'] = sum(lengths) / len(lengths) if lengths else 0
        patterns['emoji_usage'] = emojis_count / total if total > 0 else 0
        patterns['question_rate'] = questions_count / total if total > 0 else 0
        patterns['mention_profile'] = mentions_count / total if total > 0 else 0
        patterns['avg_success_score'] = sum(o.success_score for o in self.successful_openings) / total
        patterns['top_performers'] = [
            o.message for o in sorted(
                self.successful_openings,
                key=lambda x: x.success_score,
                reverse=True
            )[:3]
        ]

        return patterns

    def extract_common_topics(self) -> List[str]:
        """Extrai tópicos comuns das opening messages bem-sucedidas"""
        topics = []
        keywords = ['viaj', 'livr', 'film', 'musica', 'arte', 'esporte',
                   'tecnolog', 'comida', 'amistad', 'risada', 'aventur']

        for opening in self.successful_openings:
            for keyword in keywords:
                if keyword.lower() in opening.message.lower():
                    topics.append(keyword)

        # Retorna tópicos mais frequentes
        counter = Counter(topics)
        return [topic for topic, _ in counter.most_common(5)]

    def get_profile_success_mapping(self) -> Dict[str, float]:
        """
        Mapeia qual tipo de perfil responde melhor

        Returns:
            Dict: {'age_group': score, 'gender': score, 'education': score}
        """
        mapping = defaultdict(list)

        for opening in self.successful_openings:
            profile = opening.match_profile

            # Agrupar por características
            if profile.get('age'):
                age_group = f"{(profile['age'] // 5) * 5}-{(profile['age'] // 5) * 5 + 5}"
                mapping[f"age:{age_group}"].append(opening.success_score)

            if profile.get('gender'):
                mapping[f"gender:{profile['gender']}"].append(opening.success_score)

            if profile.get('education_level'):
                mapping[f"edu:{profile['education_level']}"].append(opening.success_score)

        # Calcular média por grupo
        result = {}
        for key, scores in mapping.items():
            result[key] = sum(scores) / len(scores) if scores else 0

        return result

    def generate_opening(self, new_match_profile: Dict) -> Tuple[str, Dict]:
        """
        Gera opening message inteligente para novo match

        Args:
            new_match_profile: Dict com name, age, gender, profession, bio, education, location

        Returns:
            Tuple[message, metadata] onde metadata contém score de confiança
        """
        if not self.successful_openings:
            return self._fallback_opening(new_match_profile)

        patterns = self.get_patterns()
        common_topics = self.extract_common_topics()
        profile_success = self.get_profile_success_mapping()

        # Estratégia: combinar opening bem-sucedida + adaptação ao perfil
        best_template = self._select_best_template(new_match_profile, profile_success)
        adapted_message = self._adapt_template(best_template, new_match_profile)

        metadata = {
            'strategy': 'adaptive',
            'confidence': patterns['avg_success_score'],
            'template_used': best_template,
            'topics_included': common_topics[:2],
            'expected_response_rate': patterns['question_rate'],
            'profile_match_score': profile_success.get(
                f"gender:{new_match_profile.get('gender')}", 0.5
            )
        }

        return adapted_message, metadata

    def _select_best_template(self, profile: Dict, profile_success: Dict) -> str:
        """Seleciona melhor opening template para este perfil"""
        # Score profiles similares
        best_opening = None
        best_score = -1

        for opening in self.successful_openings:
            similarity = self._profile_similarity(
                opening.match_profile, profile
            )
            combined_score = similarity * opening.success_score

            if combined_score > best_score:
                best_score = combined_score
                best_opening = opening.message

        return best_opening or self.successful_openings[0].message

    def _profile_similarity(self, profile1: Dict, profile2: Dict) -> float:
        """Calcula similaridade entre dois perfis (0-1)"""
        similarities = []

        # Idade
        if profile1.get('age') and profile2.get('age'):
            age_diff = abs(profile1['age'] - profile2['age'])
            age_sim = max(0, 1 - (age_diff / 20))  # Max 20 anos de diferença
            similarities.append(age_sim)

        # Educação
        if profile1.get('education_level') and profile2.get('education_level'):
            edu_sim = 1.0 if profile1['education_level'] == profile2['education_level'] else 0.5
            similarities.append(edu_sim)

        # Gênero
        if profile1.get('gender') and profile2.get('gender'):
            gen_sim = 1.0 if profile1['gender'] == profile2['gender'] else 0.8
            similarities.append(gen_sim)

        # Localização
        if profile1.get('location') and profile2.get('location'):
            loc_sim = 1.0 if profile1['location'] == profile2['location'] else 0.6
            similarities.append(loc_sim)

        return sum(similarities) / len(similarities) if similarities else 0.5

    def _adapt_template(self, template: str, profile: Dict) -> str:
        """
        Adapta template para o perfil específico

        Substitui placeholders com dados reais do match
        """
        adapted = template

        # Substituir placeholders
        if '{name}' in adapted and profile.get('name'):
            adapted = adapted.replace('{name}', profile['name'])

        if '{profession}' in adapted and profile.get('profession'):
            adapted = adapted.replace('{profession}', profile['profession'])

        # Se bio menciona tópicos, extrair
        if '{topic}' in adapted and profile.get('bio'):
            bio_words = profile['bio'].lower().split()
            topic = bio_words[0] if bio_words else 'isso'
            adapted = adapted.replace('{topic}', topic)

        # Adicionar tópicos relevantes se não estão no template
        if not any(topic in adapted.lower() for topic in self.extract_common_topics()):
            topics = self.extract_common_topics()
            if topics and '{' not in adapted:  # Se template foi totalmente resolvido
                # Adicionar menção a tópico relevante
                adapted += f" Vi que combina com {topics[0]}! 😊"

        return adapted

    def _fallback_opening(self, profile: Dict) -> Tuple[str, Dict]:
        """Fallback quando não há histórico"""
        name = profile.get('name', 'você')
        profession = profile.get('profession', 'seu trabalho')

        message = f"Oi {name}! Percebi que trabalha em {profession}. Como sua experiência tem sido? 😊"

        return message, {
            'strategy': 'fallback',
            'confidence': 0.5,
            'reason': 'no_history'
        }

    def export_insights(self, filename: str = 'opening_insights.json'):
        """Exporta insights sobre as opening messages"""
        insights = {
            'total_successful': len(self.successful_openings),
            'total_failed': len(self.failed_openings),
            'success_rate': len(self.successful_openings) / (
                len(self.successful_openings) + len(self.failed_openings)
            ) if self.successful_openings or self.failed_openings else 0,
            'patterns': self.get_patterns(),
            'common_topics': self.extract_common_topics(),
            'profile_success_mapping': dict(self.get_profile_success_mapping()),
            'top_performing_messages': [o.message for o in sorted(
                self.successful_openings,
                key=lambda x: x.success_score,
                reverse=True
            )[:5]]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(insights, f, indent=2, ensure_ascii=False)

        return insights


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Simular histórico de conversas
    mock_history = [
        {
            'messages': [
                {'content': 'Oi Marina! Vi que você curte cinema francês, qual é seu favorito? 🎬'},
                {'content': 'Truffaut! Você tem bom gosto 😊'},
                {'content': 'Nossa, que legal!'},
            ],
            'response_times': [45.0],
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
        {
            'messages': [
                {'content': 'Qual é teu livro favorito? Pareço alguém legal 😄'},
                {'content': 'Curtir!! Me tira do meu padrão'},
            ],
            'response_times': [120.0],
            'profile': {
                'name': 'Julia',
                'age': 26,
                'gender': 'F',
                'profession': 'Designer',
                'bio': 'Literatura, arte, natureza',
                'education_level': 'bachelor',
                'location': 'Rio de Janeiro'
            }
        },
        {
            'messages': [
                {'content': 'Oi! Como seu dia está?'},
                # Sem resposta = falha
            ],
            'response_times': [999.0],
            'profile': {
                'name': 'Carol',
                'age': 24,
                'gender': 'F',
                'profession': 'Estudante',
                'bio': 'Artes, criativa',
                'education_level': 'high_school',
                'location': 'Brasília'
            }
        }
    ]

    # Criar gerador
    generator = AdaptiveOpeningMessageGenerator(mock_history)

    # Novo match
    new_match = {
        'name': 'Ana',
        'age': 27,
        'gender': 'F',
        'profession': 'Arquiteta',
        'bio': 'Design, viagens, bom papo',
        'education_level': 'master',
        'location': 'São Paulo'
    }

    # Gerar opening inteligente
    message, metadata = generator.generate_opening(new_match)

    print("\n" + "="*70)
    print("🤖 ADAPTIVE OPENING MESSAGE GENERATOR")
    print("="*70)
    print(f"\n✓ Histórico: {len(mock_history)} conversas analisadas")
    print(f"✓ Taxa de sucesso: {len(generator.successful_openings)} bem-sucedidas")
    print(f"\n📊 PADRÕES DETECTADOS:")
    patterns = generator.get_patterns()
    print(f"  - Comprimento médio: {patterns['avg_length']:.0f} caracteres")
    print(f"  - Taxa de emojis: {patterns['emoji_usage']:.0%}")
    print(f"  - Taxa de perguntas: {patterns['question_rate']:.0%}")
    print(f"  - Taxa de menção de perfil: {patterns['mention_profile']:.0%}")
    print(f"  - Score médio de sucesso: {patterns['avg_success_score']:.2f}")

    print(f"\n💬 TÓPICOS COMUNS: {', '.join(generator.extract_common_topics())}")

    print(f"\n👤 NOVO MATCH: {new_match['name']}, {new_match['age']}, {new_match['profession']}")
    print(f"\n📝 OPENING GERADA:")
    print(f"   {message}")
    print(f"\n📈 METADATA:")
    print(f"   - Estratégia: {metadata['strategy']}")
    print(f"   - Confiança: {metadata['confidence']:.2%}")
    print(f"   - Score de compatibilidade: {metadata['profile_match_score']:.2f}")
    print(f"   - Taxa esperada de resposta: {metadata['expected_response_rate']:.0%}")

    # Exportar insights
    insights = generator.export_insights()
    print(f"\n💾 Insights exportados para: opening_insights.json")
    print("="*70)
