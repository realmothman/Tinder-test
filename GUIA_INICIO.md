# 🚀 Guia Rápido - Comece aqui!

Bem-vindo ao repositório de estudo de automação Tinder! Este guia te ajuda a começar.

## 📋 Estrutura do Repositório

```
/
├── README.md                    ← Visão geral (LEIA PRIMEIRO)
├── GUIA_INICIO.md              ← Você está aqui
├── python/
│   ├── exemplo_basico.py       ← Padrões Python
│   └── .gitkeep
├── javascript/
│   ├── exemplo_basico.js       ← Padrões JavaScript
│   └── .gitkeep
├── java/
│   ├── TinderAutomation.java   ← Padrões Java
│   └── .gitkeep
└── research/
    ├── RECURSOS.md             ← Repositórios, libs, tutoriais
    └── COMPARACAO_LINGUAGENS.md ← Python vs JS vs Java
```

---

## 🎯 Passo 1: Escolha sua Linguagem

### Para Iniciantes
**→ Comece com Python** 🐍

Por quê?
- Sintaxe fácil de entender
- Comunidade enorme (mais exemplos)
- Perfeito para aprender conceitos
- Rápido ver resultados

### Para Produção Pequena
**→ Use JavaScript/Node.js** 📍

Por quê?
- Melhor performance que Python
- Setup mais rápido
- Async nativa
- Deploy simples

### Para Escala Grande
**→ Escolha Java** ☕

Por quê?
- Escalabilidade comprovada
- Performance 10x melhor
- Multi-threading nativo
- Pronto para produção

**→ Leia [COMPARACAO_LINGUAGENS.md](research/COMPARACAO_LINGUAGENS.md) para mais detalhes**

---

## 🐍 Início Rápido: Python

### 1. Setup
```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` no Windows

# Instalar dependências
pip install selenium requests aiohttp python-dotenv
```

### 2. Entender a Estrutura
```bash
# Abrir exemplo
cat python/exemplo_basico.py
```

Estude os padrões:
1. **TinderAPIWrapper** - Chamadas diretas à API
2. **TinderWebAutomation** - Browser automation com Selenium
3. **SmartSwiperAI** - IA para decisões
4. **MessageAutomation** - Gerar mensagens com ChatGPT
5. **MultiAccountManager** - Múltiplas contas

### 3. Criar seu Primeiro Bot
```python
# bot_simples.py
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://tinder.com")

# Login (manual por enquanto)
input("Pressione Enter após fazer login...")

# Fazer swipes
while True:
    try:
        like_button = driver.find_element("xpath", "//button[@aria-label='Like']")
        like_button.click()
        print("❤️ Like!")
    except:
        print("❌ Sem mais perfis")
        break

driver.quit()
```

### 4. Próximos Passos
```
1. ✅ Entender API do Tinder (veja RECURSOS.md)
2. ⏳ Adicionar delays aleatórios (2-5 segundos)
3. ⏳ Implementar login automático
4. ⏳ Armazenar dados em CSV/SQLite
5. ⏳ Adicionar message generation
```

**→ Veja [python/exemplo_basico.py](python/exemplo_basico.py) para código completo**

---

## 📍 Início Rápido: JavaScript/Node.js

### 1. Setup
```bash
# Criar projeto
mkdir tinder-bot
cd tinder-bot
npm init -y

# Instalar dependências
npm install puppeteer axios dotenv lodash
npm install --save-dev typescript ts-node @types/node
```

### 2. Entender a Estrutura
```bash
# Abrir exemplo
cat javascript/exemplo_basico.js
```

Estude os padrões:
1. **TinderAPIClient** - Fetch API wrapper com async/await
2. **TinderWebAutomation** - Puppeteer automation
3. **SmartMessenger** - OpenAI ChatGPT integration
4. **TinderBot** - Bot principal com auto-swiping

### 3. Criar seu Primeiro Bot
```javascript
// bot_simples.js
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: false, // Ver navegador
  });
  
  const page = await browser.newPage();
  await page.goto('https://tinder.com');
  
  console.log('Faça login manualmente...');
  await page.waitForNavigation(); // Aguarda login
  
  // Fazer swipes
  for (let i = 0; i < 10; i++) {
    try {
      await page.click('[data-testid="like-button"]');
      console.log('❤️ Like!');
      await page.waitForTimeout(2000);
    } catch (e) {
      console.log('❌ Erro:', e.message);
      break;
    }
  }
  
  await browser.close();
})();
```

### 4. Próximos Passos
```
1. ✅ Entender Puppeteer
2. ⏳ Implementar API calls com axios
3. ⏳ Adicionar error handling
4. ⏳ Integrar ChatGPT para messages
5. ⏳ Setup com Bull para background jobs
```

**→ Veja [javascript/exemplo_basico.js](javascript/exemplo_basico.js) para código completo**

---

## ☕ Início Rápido: Java

### 1. Setup
```bash
# Com Spring Boot CLI
spring boot new --type gradle tinder-bot
cd tinder-bot

# Ou com Maven
mvn archetype:generate -DgroupId=com.tinder -DartifactId=tinder-bot
```

### 2. Adicionar Dependências
```gradle
// build.gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'mysql:mysql-connector-java:8.0.33'
    implementation 'org.projectlombok:lombok'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}
```

### 3. Entender a Estrutura
```bash
# Abrir exemplo
cat java/TinderAutomation.java
```

Estude os padrões:
1. **Modelos (Entities)** - TinderProfile, TinderMatch, AutomationLog
2. **Repositories** - CrudRepository para persistência
3. **Services** - TinderAPIService, TinderAutomationService
4. **Controllers** - REST endpoints

### 4. Criar sua Primeira Classe
```java
// TinderBotApplication.java
@SpringBootApplication
@EnableScheduling
public class TinderBotApplication {
    public static void main(String[] args) {
        SpringApplication.run(TinderBotApplication.class, args);
    }
}

// AutomationService.java
@Service
class AutomationService {
    @Scheduled(cron = "0 0 * * * *") // A cada hora
    public void autoSwipe() {
        System.out.println("🤖 Bot running...");
        // Implementar
    }
}
```

### 5. Próximos Passos
```
1. ✅ Setup Spring Boot
2. ⏳ Implementar API calls com WebClient
3. ⏳ Criar database schema
4. ⏳ Setup agendamento com @Scheduled
5. ⏳ Implementar REST API para monitoring
```

**→ Veja [java/TinderAutomation.java](java/TinderAutomation.java) para código completo**

---

## 📚 Recursos Essenciais

### Para Todas as Linguagens

1. **Entender a API do Tinder**
   - Veja [research/RECURSOS.md](research/RECURSOS.md#api-endpoints-comuns)
   - Endpoints principais: GET /recs, POST /like, POST /pass

2. **Conhecer Técnicas Anti-Detecção**
   - Delays aleatórios (2-5 segundos)
   - User-agent rotation
   - Proxy rotation (premium)
   - undetected-chromedriver (Python)

3. **Segurança**
   - Armazenar tokens em .env
   - Nunca commitar secrets
   - Usar HTTPS
   - Rate limiting

### Por Linguagem

#### Python
- [Selenium Documentation](https://selenium.dev/documentation/)
- [Real Python - Web Scraping](https://realpython.com/python-web-scraping/)
- [TensorFlow Getting Started](https://www.tensorflow.org/tutorials/quickstart/beginner)

#### JavaScript
- [Puppeteer Guide](https://pptr.dev/)
- [Modern JavaScript](https://javascript.info/)
- [Node.js Best Practices](https://nodejs.org/en/docs/guides/)

#### Java
- [Spring Boot Reference](https://spring.io/projects/spring-boot)
- [Java Concurrency](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [WebClient Guide](https://www.baeldung.com/spring-webflux-webclient)

---

## ⚠️ Aviso Importante

### O que é Educacional ✅
- Estudar código open source
- Entender padrões de automação
- Aprender web scraping
- Pesquisa acadêmica

### O que Viola ToS ❌
- Usar automação não autorizada
- Criar múltiplas contas
- Spam de mensagens
- Scraping em massa

**Este repositório é apenas educacional. Implementação real viola os Termos de Serviço do Tinder.**

---

## 🔗 Próximas Leituras

1. **README.md** - Visão geral do projeto
2. **research/RECURSOS.md** - Repositórios, libs, tutoriais
3. **research/COMPARACAO_LINGUAGENS.md** - Comparação detalhada
4. **python/exemplo_basico.py** - Padrões Python
5. **javascript/exemplo_basico.js** - Padrões JavaScript
6. **java/TinderAutomation.java** - Padrões Java

---

## 💬 Dúvidas?

1. Veja os exemplos no repositório
2. Leia RECURSOS.md para links
3. Estude repositórios populares listados
4. Experimente com código simples primeiro

---

## 🎓 Próximas Etapas

```
Semana 1: Entendimento
├─ Ler README.md
├─ Escolher linguagem
├─ Estudar exemplo correspondente
└─ Entender conceitos básicos

Semana 2-3: Implementação
├─ Criar projeto
├─ Setup environment
├─ Implementar API wrapper
└─ Fazer primeiro swipe automático

Semana 4+: Avançado
├─ Adicionar IA/ML
├─ Message generation
├─ Persistência de dados
└─ Monitoramento
```

---

**Boa sorte no seu aprendizado! 🚀**

**Data criação**: 2026-10-01  
**Branch**: ccr-ebd74371-257wzl  
**Status**: Ready for study ✅
