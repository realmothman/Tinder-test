# 🔍 Como Avaliar Repositórios para Pesquisa Acadêmica

## Critérios de Avaliação Técnica

### 1. **Funcionalidade Comprovada**

#### Sinais Positivos ✅
- [ ] Código compila/roda sem erros maiores
- [ ] Exemplos funcionais de uso (not just "hello world")
- [ ] Screenshots ou vídeos demonstrando funcionalidade
- [ ] Issues resolvidas sobre funcionalidade
- [ ] Commits recentes mostrando manutenção
- [ ] Testes automatizados (unit/integration)
- [ ] CI/CD pipeline configurado (GitHub Actions, Travis, etc)

#### Sinais de Alerta ⚠️
- [ ] Última atualização > 2 anos atrás
- [ ] Muitos issues abertos sem resposta
- [ ] Documentação desatualizada
- [ ] Dependências vulneráveis (outdated)
- [ ] Código com muitos TODOs/FIXMEs
- [ ] Sem exemplos executáveis
- [ ] Requisitos não documentados

#### Teste Prático
```bash
# Para cada repo:
1. git clone <url>
2. Seguir README exatamente
3. Executar exemplos
4. Documentar quais funcionam/falham
5. Verificar últimas issues abertas
```

---

### 2. **Qualidade de Código**

#### Arquitetura
```
Questões:
├─ Classes bem definidas? (OOP)
├─ Funções com responsabilidade única? (SRP)
├─ Padrões de design? (Factory, Strategy, Observer)
├─ Separação de concerns? (API vs Business vs Persistence)
└─ Testabilidade? (Dependency injection, mocks)
```

#### Métricas Específicas
```python
# Analisar:
1. Cyclomatic complexity (ideal < 10 por função)
2. Code duplication (ideal < 5%)
3. Comment ratio (ideal 15-30%)
4. Function length (ideal < 50 linhas)
5. Class cohesion
```

#### Tools
```bash
# Python
pip install radon pylint pycodestyle
radon cc repo.py -a  # Cyclomatic complexity
pylint *.py          # Análise estática

# JavaScript
npm install eslint
eslint .

# Java
java -jar checkstyle-*-all.jar
```

---

### 3. **Comunidade & Manutenção**

#### Métricas GitHub
```
Indicadores de Saúde:
├─ ⭐ Stars: 100+ = validação da comunidade
├─ 🍴 Forks: 10+ = reuso/confiança
├─ 👁️ Watchers: > stars/20 = interesse real
├─ 🐛 Issues: Abertas vs fechadas ratio
├─ 📝 Commits: Frequência (últimos 3 meses)
├─ 👥 Contributors: 3+ = não é projeto 1 pessoa
└─ 📅 Last update: < 6 meses = ativo
```

#### Análise de Atividade
```bash
# Ver commits recentes
git log --oneline --all | head -20

# Frequência de commits
git log --oneline --all | wc -l

# Últimas atualizações
git log -1 --format=%ci

# Contributors principais
git shortlog -sn | head -10
```

#### Community Health
- README completo e atualizado
- Contributing guidelines
- Code of conduct
- License declarado
- Issues respondidas (< 1 semana)
- Pull requests review time

---

### 4. **Documentação**

#### Checklist de Documentação
```
README:
├─ [ ] Descrição clara do projeto
├─ [ ] Instalação passo-a-passo
├─ [ ] Exemplos de uso funcionais
├─ [ ] API documentation
├─ [ ] Troubleshooting
├─ [ ] License
└─ [ ] Contribuindo

Code Comments:
├─ [ ] Funções documentadas (docstrings)
├─ [ ] Algoritmos complexos explicados
├─ [ ] Configuração documentada
└─ [ ] Exemplos inline

Extras Acadêmicos:
├─ [ ] Paper/Research associated?
├─ [ ] Citações de trabalhos anteriores?
├─ [ ] Methodologia descrita?
└─ [ ] Benchmark results publicados?
```

---

### 5. **Valor Acadêmico Específico**

#### Para ML/Computer Vision
```
Avalie:
├─ Dataset transparência (treinamento/teste split)
├─ Métricas relatadas (accuracy, precision, recall, F1)
├─ Validação metodologia (cross-validation?)
├─ Bias analysis (dataset bias)
├─ Benchmarks contra SOTA
├─ Code para reproduzir resultados
└─ Ablation studies (contribuição de cada component)
```

#### Para Segurança/Bot Detection
```
Avalie:
├─ Técnicas comparadas (vs baselines?)
├─ Taxa de falsos positivos/negativos
├─ Robustness contra adversarial examples
├─ Performance metrics (latência, throughput)
├─ Evasion techniques discussed
└─ Limitations acknowledged
```

#### Para NLP/Message Generation
```
Avalie:
├─ BLEU/ROUGE/METEOR scores
├─ Human evaluation results
├─ Beam search parameters
├─ Vocabulary size/OOV handling
├─ Multilingual support
└─ Decoding strategy ablations
```

---

## Checklist de Avaliação Rápida

Para cada repositório analisar:

```
BÁSICO (5 min)
- [ ] Último commit: quantos meses atrás?
- [ ] Stars: 100+? 500+? 1000+?
- [ ] README: claro e detalhado?
- [ ] Issues: proporção aberto/fechado?
- [ ] Código: 100+ linhas de lógica real?

FUNCIONALIDADE (15 min)
- [ ] Clone, install, execute
- [ ] Exemplos funcionam?
- [ ] Erros significativos?
- [ ] Performance aceitável?
- [ ] Configuração fácil?

CÓDIGO (15 min)
- [ ] Arquitetura clara?
- [ ] Padrões reconhecíveis?
- [ ] Código duplicado?
- [ ] Funções curtas e claras?
- [ ] Nomes de variáveis significativos?

VALOR ACADÊMICO (15 min)
- [ ] Técnica inovadora?
- [ ] Paper associado?
- [ ] Métodos científicos?
- [ ] Benchmarks? Baselines?
- [ ] Reproduzibilidade?

TOTAL: 50 minutos por repo
```

---

## Scorecard Proposto

### Scoring Rubric (0-5 scale)

```
FUNCIONALIDADE (0-5)
5 = Funciona perfeitamente, pronto para produção
4 = Funciona bem, poucos bugs menores
3 = Funciona, mas com limitações conhecidas
2 = Funciona parcialmente, bugs significativos
1 = Funciona mal, muitos problemas
0 = Não funciona

CÓDIGO (0-5)
5 = Excelente arquitetura, muito legível, patterns claros
4 = Bom código, alguns problemas menores
3 = Código OK, problemas de organização
2 = Código confuso, arquitetura pobre
1 = Código ruim, muito acoplado
0 = Indecifrável

DOCUMENTAÇÃO (0-5)
5 = Documentação completa, exemplos funcionais
4 = Boa documentação, alguns gaps
3 = Documentação OK, faltam exemplos
2 = Documentação mínima
1 = Quase sem documentação
0 = Sem documentação

COMUNIDADE (0-5)
5 = Ativo, muitos contributors, respostas rápidas
4 = Razoavelmente ativo, boa comunidade
3 = Minimamente mantido, algumas issues
2 = Pouca atividade, respostas lentas
1 = Praticamente abandonado
0 = Completamente abandonado

INOVAÇÃO ACADÊMICA (0-5)
5 = Técnica novel, paper publicado, SOTA
4 = Boa contribuição, útil para pesquisa
3 = Implementa técnicas conhecidas bem
2 = Implementação básica de conceitos existentes
1 = Cópia simples de outro projeto
0 = Nenhuma inovação

SCORE TOTAL: __/25
```

### Interpretação
- **20-25**: ⭐⭐⭐⭐⭐ Excelente para tese (ESTUDE PROFUNDAMENTE)
- **15-19**: ⭐⭐⭐⭐ Muito bom (considere como estudo)
- **10-14**: ⭐⭐⭐ Bom (útil para referência)
- **5-9**: ⭐⭐ OK (maybe inspiração)
- **0-4**: ⭐ Pobre (skip)

---

## Recursos Úteis para Avaliação

### Análise de GitHub
```bash
# Instalar
pip install ghapi pandas

# Analisar repositório
from ghapi.all import GhApi
api = GhApi()
repo = api.repos.get("owner", "repo")
print(f"Stars: {repo.stargazers_count}")
print(f"Watchers: {repo.watchers_count}")
print(f"Forks: {repo.forks_count}")
```

### Code Quality Tools
- **SonarQube**: Code smell detection
- **Codecov**: Coverage analysis
- **Dependabot**: Dependency updates
- **LGTM**: Code review automation

### Repositórios Acadêmicos
- **arXiv.org**: Buscar papers sobre técnicas
- **Google Scholar**: Citações de artigos
- **Papers with Code**: Implementações de papers
- **ResearchGate**: Conexão com autores

---

## Red Flags - Quando NÃO Usar um Repo

🚩 Abandonado (sem commits > 2 anos)
🚩 Sem documentação real
🚩 Muitas vulnerabilidades não resolvidas
🚩 Código ilegível/desorganizado
🚩 Single person project sem testes
🚩 Violação de privacidade óbvia
🚩 Funcionalidade não provada
🚩 Padrões antiéticos ou ilegais
🚩 Sem license ou license restritiva

---

## Green Flags - Sinais Positivos

✅ Ativo (commits últimos 3 meses)
✅ 500+ stars
✅ Tests automatizados
✅ Documentação clara
✅ Múltiplos contributors
✅ Issues respondidas rapidamente
✅ Padrões de design aplicados
✅ Inovação acadêmica clara
✅ Reproduzibilidade comprovada
✅ Comunidade engajada

---

## Template para Documentar Repos

```markdown
# Repo Name
**URL**: https://github.com/...
**Stars**: XXX | **Forks**: XX | **Last Update**: YYYY-MM-DD

## Resumo
[Uma frase sobre o quê faz]

## Funcionalidade
- [ ] Funciona pronto (confirm com teste)
- [ ] Requer setup específico
- [ ] Parcialmente implementado

## Qualidade de Código
Arquitetura: ⭐⭐⭐⭐⭐
Legibilidade: ⭐⭐⭐⭐⭐
Padrões: ⭐⭐⭐⭐⭐

## Documentação
README: ⭐⭐⭐⭐⭐
Exemplos: ⭐⭐⭐⭐⭐
API Docs: ⭐⭐⭐⭐⭐

## Valor para Tese
Técnica: [Novel/Standard/Hybrid]
Aplicabilidade: [Alta/Média/Baixa]
Score: __/25

## Conclusão
[Vale a pena estudar profundamente? Por quê?]

## Próximos Passos
[ ] Clone e teste
[ ] Estude código principal
[ ] Reproduza exemplos
[ ] Verifique performance
[ ] Cite em tese (se aplicável)
```

---

**Aplique este framework a cada repositório para avaliar objetivamente sua relevância para sua tese.**
