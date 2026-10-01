"""
Integrated Tinder Bot System
Combina automação + análise antropológica + aprendizado adaptativo

Pipeline Completo:
1. Carrega histórico de conversas
2. Treina gerador adaptativo
3. Para cada novo match: gera opening inteligente
4. Simula conversa com personas
5. Coleta dados para análise
6. Realiza análise antropológica
7. Feedback loop: atualiza modelo
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import random

# Importa componentes do bot
from tinder_bot_example import (
    Profile, Message, Conversation,
    PersonaManager, ConversationSimulator,
    HomophilyAnalyzer, GenderAnalyzer, CapitalAnalyzer
)
from adaptive_opening_generator import AdaptiveOpeningMessageGenerator, SuccessfulOpening


class IntegratedBotSystem:
    """
    Sistema integrado que combina:
    - Automação (sending messages)
    - Conversation generation (personas)
    - Adaptive learning (opening generator)
    - Anthropological analysis (homophilia, gender, capital)
    """

    def __init__(self, my_profile: Profile, historical_conversations: List[Dict] = None):
        """
        Inicializa sistema completo

        Args:
            my_profile: Seu perfil (Profile dataclass)
            historical_conversations: Conversas passadas para treinar gerador
        """
        self.my_profile = my_profile
        self.historical_conversations = historical_conversations or []

        # Inicializar componentes
        self.adaptive_generator = AdaptiveOpeningMessageGenerator(historical_conversations)
        self.conversation_history: List[Conversation] = []
        self.analysis_results = {}

        print(f"✓ Sistema inicializado com perfil: {my_profile.name}")
        print(f"✓ Histórico carregado: {len(historical_conversations)} conversas")

    def process_new_match(self, match_profile: Profile, persona: str = 'auto') -> Dict:
        """
        Processa novo match completo: opening -> conversa -> análise

        Args:
            match_profile: Perfil do novo match
            persona: 'auto' (adaptativo) ou 'friendly'/'professional'/'flirty'/'casual'

        Returns:
            Dict com resultados da conversa e análise
        """
        print(f"\n{'='*70}")
        print(f"🎯 PROCESSANDO NOVO MATCH: {match_profile.name}, {match_profile.age}")
        print(f"{'='*70}")

        # Step 1: Gerar opening inteligente
        print(f"\n📝 Step 1: Gerar Opening Inteligente")
        opening_message, opening_metadata = self._generate_opening(match_profile)
        print(f"   Mensagem: {opening_message}")
        print(f"   Confiança: {opening_metadata['confidence']:.0%}")
        print(f"   Estratégia: {opening_metadata['strategy']}")

        # Step 2: Selecionar persona
        print(f"\n🎭 Step 2: Selecionar Persona")
        selected_persona = self._select_persona(persona, match_profile, opening_metadata)
        print(f"   Persona selecionada: {selected_persona}")

        # Step 3: Simular conversa
        print(f"\n💬 Step 3: Simular Conversa")
        conversation = self._simulate_conversation(
            match_profile, opening_message, selected_persona
        )
        self.conversation_history.append(conversation)
        print(f"   Mensagens: {len(conversation.messages)}")
        print(f"   Duração: {conversation.response_times}")

        # Step 4: Análise antropológica
        print(f"\n📊 Step 4: Análise Antropológica")
        analysis = self._anthropological_analysis(conversation)

        # Step 5: Feedback & atualização
        print(f"\n🔄 Step 5: Feedback Loop")
        self._update_adaptive_model(conversation, opening_metadata)

        result = {
            'match': asdict(match_profile),
            'opening': {
                'message': opening_message,
                'metadata': opening_metadata
            },
            'persona': selected_persona,
            'conversation': {
                'messages': [asdict(m) for m in conversation.messages],
                'length': len(conversation.messages),
                'response_times': conversation.response_times
            },
            'analysis': analysis,
            'success': self._calculate_success(conversation)
        }

        return result

    def _generate_opening(self, match_profile: Profile) -> Tuple[str, Dict]:
        """Gera opening usando gerador adaptativo"""
        profile_dict = asdict(match_profile)
        message, metadata = self.adaptive_generator.generate_opening(profile_dict)
        return message, metadata

    def _select_persona(self, persona: str, profile: Profile, opening_metadata: Dict) -> str:
        """
        Seleciona melhor persona para este match

        - 'auto': baseado em profile + opening_metadata confidence
        - específica: usa a escolhida
        """
        if persona != 'auto':
            return persona

        # Auto-select baseado em perfil
        if profile.education_level in ['master', 'phd']:
            return 'professional'
        elif profile.gender == 'F' and opening_metadata['confidence'] > 0.7:
            return 'flirty'
        else:
            return 'friendly'

    def _simulate_conversation(
        self, profile: Profile, opening: str, persona: str
    ) -> Conversation:
        """Simula conversa completa"""
        messages = [
            Message(
                timestamp=datetime.now().isoformat(),
                sender='bot',
                content=opening,
                word_count=len(opening.split())
            )
        ]

        # Simular resposta do match
        response = ConversationSimulator.simulate_response(profile, messages, opening)
        messages.append(Message(
            timestamp=datetime.now().isoformat(),
            sender='user',
            content=response,
            word_count=len(response.split())
        ))

        # Simular 1-2 turnos adicionais
        for _ in range(random.randint(1, 2)):
            persona_obj = PersonaManager.get_persona(persona)
            bot_response = f"Que legal! {response}"  # Simplified simulation
            messages.append(Message(
                timestamp=datetime.now().isoformat(),
                sender='bot',
                content=bot_response,
                word_count=len(bot_response.split())
            ))

            # Resposta do match
            final_response = ConversationSimulator.simulate_response(profile, messages, bot_response)
            messages.append(Message(
                timestamp=datetime.now().isoformat(),
                sender='user',
                content=final_response,
                word_count=len(final_response.split())
            ))

        return Conversation(
            conversation_id=f"conv_{len(self.conversation_history)}",
            profile=profile,
            persona_used=persona,
            messages=messages,
            response_times=[random.uniform(3, 120) for _ in range(len(messages) - 1)],
            started_at=datetime.now().isoformat(),
            ended_at=datetime.now().isoformat()
        )

    def _anthropological_analysis(self, conversation: Conversation) -> Dict:
        """Executa análises antropológicas"""
        # Homophilia
        homophily = HomophilyAnalyzer.analyze(self.my_profile, [conversation])

        # Gender (apenas se há múltiplas conversas para comparar)
        gender_analysis = {}
        if len(self.conversation_history) > 1:
            gender_analysis = GenderAnalyzer.analyze(self.conversation_history)

        # Capital
        capital = CapitalAnalyzer.analyze([conversation])

        return {
            'homophily': homophily,
            'gender_dynamics': gender_analysis,
            'capital_signals': capital
        }

    def _update_adaptive_model(self, conversation: Conversation, opening_metadata: Dict):
        """Atualiza modelo adaptativo com feedback da conversa"""
        # Determinar sucesso
        got_response = len(conversation.messages) > 1
        response_time = conversation.response_times[0] if got_response else 999
        conv_length = len(conversation.messages)

        # Calcular success score
        success_score = 0.0
        if got_response:
            response_score = max(0, 1 - (response_time / 300))  # max 5 min
            length_score = min(1, conv_length / 10)
            success_score = (response_score + length_score) / 2

        # Criar opening bem-sucedida
        if success_score > 0.5:
            successful = SuccessfulOpening(
                message=conversation.messages[0].content,
                response_received=got_response,
                response_time=response_time,
                conversation_length=conv_length,
                match_profile=asdict(conversation.profile),
                success_score=success_score
            )
            self.adaptive_generator.successful_openings.append(successful)
            print(f"   ✓ Adicionado ao histórico de sucesso (score: {success_score:.2f})")
        else:
            self.adaptive_generator.failed_openings.append(
                conversation.messages[0].content
            )
            print(f"   ✗ Registrado como tentativa (score: {success_score:.2f})")

    def _calculate_success(self, conversation: Conversation) -> Dict:
        """Calcula métrica de sucesso para a conversa"""
        num_turns = len([m for m in conversation.messages if m.sender == 'user'])
        got_response = num_turns > 0

        return {
            'got_response': got_response,
            'number_of_turns': num_turns,
            'total_messages': len(conversation.messages),
            'success_level': 'high' if num_turns >= 3 else 'medium' if num_turns >= 1 else 'low'
        }

    def generate_report(self, filename: str = 'bot_session_report.json') -> Dict:
        """Gera relatório completo da sessão"""
        report = {
            'session_timestamp': datetime.now().isoformat(),
            'my_profile': asdict(self.my_profile),
            'conversations_processed': len(self.conversation_history),
            'adaptive_generator_stats': {
                'successful_openings': len(self.adaptive_generator.successful_openings),
                'failed_openings': len(self.adaptive_generator.failed_openings),
                'success_rate': len(self.adaptive_generator.successful_openings) / (
                    len(self.adaptive_generator.successful_openings) +
                    len(self.adaptive_generator.failed_openings)
                ) if (self.adaptive_generator.successful_openings or
                      self.adaptive_generator.failed_openings) else 0,
                'patterns': self.adaptive_generator.get_patterns(),
                'common_topics': self.adaptive_generator.extract_common_topics(),
            },
            'aggregate_analysis': self._aggregate_analysis() if self.conversation_history else {},
            'individual_results': [
                self._conversation_to_dict(conv) for conv in self.conversation_history
            ]
        }

        # Salvar
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

    def _aggregate_analysis(self) -> Dict:
        """Análise agregada de todas as conversas"""
        if not self.conversation_history:
            return {}

        # Homophilia agregada
        homophily = HomophilyAnalyzer.analyze(self.my_profile, self.conversation_history)

        # Gender agregada
        gender = GenderAnalyzer.analyze(self.conversation_history)

        # Capital agregada
        capital = CapitalAnalyzer.analyze(self.conversation_history)

        return {
            'homophily': homophily,
            'gender_dynamics': gender,
            'capital': capital
        }

    def _conversation_to_dict(self, conversation: Conversation) -> Dict:
        """Converte Conversation para Dict"""
        return {
            'id': conversation.conversation_id,
            'profile': asdict(conversation.profile),
            'persona': conversation.persona_used,
            'messages': [asdict(m) for m in conversation.messages],
            'response_times': conversation.response_times,
            'total_duration': sum(conversation.response_times)
        }

    def export_insights(self, filename: str = 'adaptive_insights.json'):
        """Exporta insights do sistema adaptativo"""
        self.adaptive_generator.export_insights(filename)
        print(f"✓ Insights exportados para: {filename}")


# ============================================================================
# EXEMPLO DE USO COMPLETO
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("🤖 INTEGRATED TINDER BOT SYSTEM - COMPLETE DEMO")
    print("="*70)

    # Seu perfil
    my_profile = Profile(
        name="Alex",
        age=28,
        gender="M",
        profession="Engenheiro de Software",
        bio="Gosto de viajar, ler e bom papo",
        education_level="bachelor",
        location="São Paulo"
    )

    # Histórico simulado (primeiros matches)
    historical = [
        {
            'messages': [
                {'content': 'Oi Marina! Vi que você curte cinema, qual é seu favorito? 🎬'},
                {'content': 'Truffaut! Você tem bom gosto'},
            ],
            'response_times': [45.0],
            'profile': {
                'name': 'Marina',
                'age': 28,
                'gender': 'F',
                'profession': 'Jornalista',
                'bio': 'Cinema, viagens',
                'education_level': 'bachelor',
                'location': 'São Paulo'
            }
        }
    ]

    # Inicializar sistema
    bot = IntegratedBotSystem(my_profile, historical)

    # Novos matches para processar
    new_matches = [
        Profile("Ana", 27, "F", "Arquiteta", "Design, viagens, bom papo", "master", "São Paulo"),
        Profile("Julia", 29, "F", "Médica", "Saúde, academia", "master", "São Paulo"),
    ]

    # Processar cada match
    results = []
    for match in new_matches:
        result = bot.process_new_match(match, persona='auto')
        results.append(result)

    # Gerar relatório
    print(f"\n{'='*70}")
    print("📊 GERANDO RELATÓRIO FINAL")
    print(f"{'='*70}")
    report = bot.generate_report('integrated_bot_report.json')
    bot.export_insights('adaptive_insights_final.json')

    print(f"\n✓ Relatório gerado: integrated_bot_report.json")
    print(f"✓ Total de conversas: {len(bot.conversation_history)}")
    print(f"✓ Sucesso adaptativo: {len(bot.adaptive_generator.successful_openings)} openings bem-sucedidas")

    print(f"\n{'='*70}")
    print("🎯 SISTEMA PRONTO PARA PRODUÇÃO!")
    print(f"{'='*70}")
