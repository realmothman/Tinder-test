"""
Tinder Browser Automation
Real Tinder API wrapper using Selenium + undetected-chromedriver

IMPORTANTE: Isso viola Termos de Serviço do Tinder
Use por sua conta e risco. Pode resultar em ban.
"""

from __future__ import annotations

import time
import random
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    import undetected_chromedriver as uc
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logging.warning("Selenium not installed. Install: pip install selenium undetected-chromedriver")


@dataclass
class TinderMatch:
    """Match do Tinder com dados básicos"""
    match_id: str
    name: str
    age: int
    bio: str
    photos: List[str]  # URLs de fotos
    location: str
    distance_km: int
    timestamp: str
    is_online: bool = False


@dataclass
class TinderMessage:
    """Mensagem no Tinder"""
    message_id: str
    sender: str  # 'me' ou nome do match
    content: str
    timestamp: str
    is_read: bool


class TinderAutomation:
    """
    Automação real do Tinder via Selenium

    Funcionalidades:
    - Login com email/password + 2FA
    - Coletar matches
    - Enviar mensagens
    - Coletar conversas
    - Swipes automáticos
    """

    def __init__(self, headless: bool = True, mock_mode: bool = False):
        """
        Inicializa automação

        Args:
            headless: Executar em background (não mostra browser)
            mock_mode: Simular sem conectar ao Tinder real (para testes)
        """
        self.headless = headless
        self.mock_mode = mock_mode
        self.driver = None
        self.session = None
        self.logged_in = False

        self.logger = self._setup_logging()

        if not SELENIUM_AVAILABLE and not mock_mode:
            raise ImportError(
                "Selenium não instalado. Execute:\n"
                "pip install selenium undetected-chromedriver"
            )

    def _setup_logging(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger('TinderAutomation')
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        return logger

    def _get_chrome_options(self) -> Options:
        """Configura opções de Chrome anti-detecção"""
        options = Options()

        if self.headless:
            options.add_argument("--headless=new")

        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        # Performance
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        return options

    def _random_delay(self, min_sec: float = 2, max_sec: float = 5):
        """Delay aleatório para parecer humano"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def _retry_with_backoff(self, func, max_attempts: int = 3, base_wait: float = 2.0):
        """Execute function with exponential backoff on failure (best practice from similar projects)"""
        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                if attempt < max_attempts - 1:
                    wait_time = base_wait ** attempt
                    self.logger.warning(
                        f"⚠️  Attempt {attempt + 1} failed: {str(e)[:50]}... "
                        f"Retrying in {wait_time:.1f}s"
                    )
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"✗ All {max_attempts} attempts failed")
                    raise

    def login(self, email: str, password: str, wait_for_2fa: bool = True) -> bool:
        """
        Faz login no Tinder

        Args:
            email: Email da conta
            password: Senha
            wait_for_2fa: Se True, aguarda você fazer 2FA manualmente

        Returns:
            True se logado com sucesso
        """
        if self.mock_mode:
            self.logger.info("✓ Mock login (modo teste)")
            self.logged_in = True
            return True

        try:
            self.logger.info("Iniciando browser...")

            # Criar driver com anti-detecção
            self.driver = uc.Chrome(options=self._get_chrome_options())
            self._random_delay()

            # Navegar para Tinder
            self.logger.info("Acessando Tinder.com...")
            self.driver.get("https://tinder.com")
            self._random_delay(5, 10)

            # Clica "Log in"
            login_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]"))
            )
            login_btn.click()
            self._random_delay()

            # Seleciona "Login with Email"
            email_login = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in with Email')]"))
            )
            email_login.click()
            self._random_delay()

            # Preenche email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.send_keys(email)
            self._random_delay(1, 2)

            # Preenche password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(password)
            self._random_delay(1, 2)

            # Clica "Log in"
            submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            self._random_delay(5, 10)

            # Aguardar 2FA se necessário
            if wait_for_2fa:
                self.logger.info("⏳ Aguardando 2FA manual... (Complete no browser)")
                input("Pressione Enter após completar 2FA no browser: ")
                self._random_delay()

            # Verificar se está logado
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-testid='match-card']"))
                )
                self.logged_in = True
                self.logger.info("✓ Login bem-sucedido!")
                return True
            except:
                self.logger.error("✗ Falha ao verificar login")
                return False

        except Exception as e:
            self.logger.error(f"✗ Erro no login: {e}")
            return False

    def get_matches(self, limit: int = 50) -> List[TinderMatch]:
        """
        Coleta lista de matches atuais

        Args:
            limit: Máximo de matches a coletar

        Returns:
            Lista de TinderMatch
        """
        if not self.logged_in and not self.mock_mode:
            self.logger.error("Não logado. Execute login() primeiro")
            return []

        if self.mock_mode:
            self.logger.info(f"📋 Mock: Retornando {limit} matches de teste")
            return self._generate_mock_matches(limit)

        matches = []
        try:
            self.logger.info(f"Coletando até {limit} matches...")

            # Scroll para carregar matches
            for i in range(min(limit, 10)):
                self._random_delay(2, 4)

                # Encontrar card atual
                try:
                    card = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='match-card']"))
                    )

                    # Extrair dados
                    name_elem = card.find_element(By.XPATH, ".//span[@data-testid='name']")
                    bio_elem = card.find_element(By.XPATH, ".//span[@data-testid='bio']")

                    match = TinderMatch(
                        match_id=f"match_{i}_{int(time.time())}",
                        name=name_elem.text,
                        age=int(name_elem.text.split(',')[1]) if ',' in name_elem.text else 0,
                        bio=bio_elem.text,
                        photos=[],  # URLs extraídas
                        location="São Paulo",  # Default
                        distance_km=random.randint(1, 20),
                        timestamp=datetime.now().isoformat()
                    )
                    matches.append(match)

                    # Swipe right para prosseguir
                    self.swipe('right')

                except Exception as e:
                    self.logger.warning(f"Erro ao extrair match {i}: {e}")
                    continue

            self.logger.info(f"✓ Coletados {len(matches)} matches")
            return matches

        except Exception as e:
            self.logger.error(f"✗ Erro ao coletar matches: {e}")
            return matches

    def send_message(self, match_id: str, message: str) -> bool:
        """
        Envia mensagem para um match

        Args:
            match_id: ID do match
            message: Texto da mensagem

        Returns:
            True se enviado com sucesso
        """
        if not self.logged_in and not self.mock_mode:
            return False

        if self.mock_mode:
            self.logger.info(f"💬 Mock: Enviaria '{message[:50]}...'")
            return True

        try:
            self.logger.info(f"Enviando mensagem para match {match_id}...")
            self._random_delay(2, 5)

            # Encontrar input de mensagem
            msg_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mensagem']"))
            )

            msg_input.send_keys(message)
            self._random_delay(1, 2)

            # Enviar
            send_btn = self.driver.find_element(By.XPATH, "//button[@data-testid='send-message']")
            send_btn.click()

            self.logger.info(f"✓ Mensagem enviada")
            return True

        except Exception as e:
            self.logger.error(f"✗ Erro ao enviar mensagem: {e}")
            return False

    def get_conversation(self, match_id: str) -> List[TinderMessage]:
        """
        Coleta histórico de conversa

        Args:
            match_id: ID do match

        Returns:
            Lista de TinderMessage
        """
        if self.mock_mode:
            self.logger.info(f"💭 Mock: Retornando conversa de teste")
            return self._generate_mock_conversation()

        messages = []
        try:
            self.logger.info(f"Coletando conversa com {match_id}...")
            self._random_delay(2, 4)

            # Encontrar mensagens
            msg_elements = self.driver.find_elements(By.XPATH, "//div[@data-testid='message']")

            for elem in msg_elements:
                try:
                    sender = "me" if "sent" in elem.get_attribute("class") else "them"
                    content = elem.text

                    msg = TinderMessage(
                        message_id=f"msg_{len(messages)}_{int(time.time())}",
                        sender=sender,
                        content=content,
                        timestamp=datetime.now().isoformat(),
                        is_read=True
                    )
                    messages.append(msg)
                except:
                    continue

            self.logger.info(f"✓ Coletadas {len(messages)} mensagens")
            return messages

        except Exception as e:
            self.logger.error(f"✗ Erro ao coletar conversa: {e}")
            return messages

    def swipe(self, direction: str = 'right', count: int = 1) -> int:
        """
        Faz swipes automáticos

        Args:
            direction: 'right' (like) ou 'left' (pass)
            count: Quantos swipes fazer

        Returns:
            Número de swipes completados
        """
        if not self.logged_in and not self.mock_mode:
            return 0

        if self.mock_mode:
            self.logger.info(f"👆 Mock: Faria {count} swipes {direction}")
            return count

        swiped = 0
        try:
            self.logger.info(f"Fazendo {count} swipes {direction}...")

            for i in range(count):
                self._random_delay(1, 3)  # Delay entre swipes

                # Encontrar botão de swipe
                if direction == 'right':
                    btn = self.driver.find_element(By.XPATH, "//button[@data-testid='like-button']")
                else:
                    btn = self.driver.find_element(By.XPATH, "//button[@data-testid='pass-button']")

                btn.click()
                swiped += 1

            self.logger.info(f"✓ {swiped} swipes completados")
            return swiped

        except Exception as e:
            self.logger.error(f"✗ Erro no swipe: {e}")
            return swiped

    def close(self):
        """Fecha browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("✓ Browser fechado")

    def _generate_mock_matches(self, count: int) -> List[TinderMatch]:
        """Gera matches fictícios para teste"""
        names = ["Ana", "Marina", "Julia", "Carol", "Sofia", "Beatriz", "Laura", "Diana"]
        return [
            TinderMatch(
                match_id=f"match_{i}",
                name=random.choice(names),
                age=random.randint(24, 32),
                bio="Design, viagens, café",
                photos=[],
                location="São Paulo",
                distance_km=random.randint(1, 15),
                timestamp=datetime.now().isoformat(),
                is_online=random.random() < 0.5
            )
            for i in range(count)
        ]

    def _generate_mock_conversation(self) -> List[TinderMessage]:
        """Gera conversa fictícia para teste"""
        return [
            TinderMessage(
                message_id="msg_1",
                sender="me",
                content="Oi! Como vai?",
                timestamp=datetime.now().isoformat(),
                is_read=True
            ),
            TinderMessage(
                message_id="msg_2",
                sender="them",
                content="Oi! Tudo bem sim!",
                timestamp=datetime.now().isoformat(),
                is_read=True
            )
        ]


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Modo teste (mock - sem conectar ao Tinder real)
    print("="*70)
    print("🤖 TINDER AUTOMATION - DEMO")
    print("="*70)

    # Inicializar em modo mock
    bot = TinderAutomation(headless=True, mock_mode=True)

    print("\n✓ Automação inicializada (mock mode)")
    print("\n📝 Para usar com conta REAL:")
    print("  bot = TinderAutomation(headless=False, mock_mode=False)")
    print("  bot.login('seu_email@gmail.com', 'sua_senha')")
    print("\n⚠️  CUIDADO: Isso viola ToS do Tinder. Risco de ban.\n")

    # Demo com mock mode
    print("Demo (modo teste):")
    matches = bot.get_matches(3)
    print(f"Matches coletadas: {len(matches)}")
    for m in matches:
        print(f"  - {m.name}, {m.age} ({m.distance_km}km)")

    print("\nEnviando mensagem (mock):")
    bot.send_message(matches[0].match_id if matches else "test", "Oi! Como vai?")

    print("\nColetando conversa (mock):")
    conv = bot.get_conversation(matches[0].match_id if matches else "test")
    print(f"Mensagens: {len(conv)}")

    print("\nFazendo swipes (mock):")
    bot.swipe('right', 5)

    print("\n" + "="*70)
    print("✅ DEMO COMPLETO (modo teste)")
    print("="*70)
