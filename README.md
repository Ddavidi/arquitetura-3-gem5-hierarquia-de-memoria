# Projeto Prático - Arquitetura de Computadores III

**Instituição:** PUC MINAS  
**Curso:** Engenharia da Computação  
**Disciplina:** Arquitetura de Computadores III  
**Professor:** Matheus Alcântra Souza  

## Integrantes do Grupo
- Bernardo Rodrigues Pereira
- Cauã Diniz Armani
- David Nunes Ribeiro
- Julia de Mello

---

## Estrutura do Repositório e Experimentos

Neste repositório foram realizados experimentos baseados no simulador **gem5** voltados ao estudo da hierarquia de memória, variando ao todo **6 parâmetros arquiteturais**. Os experimentos foram organizados nas pastas abaixo. Cada uma contém os resultados detalhados, os gráficos gerados e um `README` específico com as conclusões e discussões daquela etapa:

- 📁 **[Associatividade e tamanho de linha](./Associatividade%20e%20tamanho%20de%20linha/)**
- 📁 **[Latência de memória e número de núcleos](./Latência%20de%20memória%20e%20número%20de%20núcleos/)**
- 📁 **[Tamanho de cache e níveis de cache](./Tamanho%20de%20cache%20e%20níveis%20de%20cache/)**

---

## Visão Geral do Projeto

### OBJETIVOS
O objetivo deste trabalho é estudar a hierarquia de memória em arquiteturas modernas de processadores, utilizando simuladores arquiteturais de nível de pesquisa.

Através dos cenários experimentais propostos, busca-se validar conceitos fundamentais relacionados a:
- Localidade temporal e espacial;
- Comportamento de caches;
- Interação CPU–memória;
- Impacto de decisões arquiteturais no desempenho.

Diferentemente de simuladores educacionais simplificados, este trabalho desenvolve a visão de Arquitetura de Computadores como ciência experimental, com metodologias características em pesquisa acadêmica.

### SIMULADOR UTILIZADO: gem5 (✅)
Simulador arquitetural detalhado amplamente utilizado em pesquisa. Permite a simulação detalhada de caches, diferentes modelos de CPU, memória virtual, além de modos syscall ou full-system.
- **Site oficial:** [https://www.gem5.org](https://www.gem5.org)
- **Documentação:** [https://www.gem5.org/documentation/](https://www.gem5.org/documentation/)
- **Tutorial oficial:** [https://www.gem5.org/documentation/learning_gem5/](https://www.gem5.org/documentation/learning_gem5/)
- **Repositório GitHub:** [https://github.com/gem5/gem5](https://github.com/gem5/gem5)

---

## Metodologia 

#### 1. Exploração do espaço de projeto
O trabalho foca em avaliações com experimentos arquiteturais controlados.
A variação dos cenários incluiu os seguintes parâmetros: tamanho de cache, associatividade, tamanho de linha, níveis de cache, latência de memória e número de núcleos.

📌 **Regra Fundamental:** A variação de um parâmetro ocorreu mantendo os demais constantes, permitindo a análise causal precisa do impacto arquitetural provocado.

#### 2. Workloads e Traces
O workload foi definido respeitando a localidade realística do acesso à memória (evitando programas artificiais sem localidade), uma vez que o comportamento do programa manipulado influi diretamente nos resultados sobre a arquitetura explorada.

#### 3. Métricas Avaliadas
As simulações abrangeram as recomendações da disciplina de análise, englobando avaliações em cima de:
- Miss rate geral das memórias cache;
- IPC / CPI;
- Latência de memória;
- Comportamento escalável do processamento entre arquiteturas multi-núcleos.
- Entre outras métricas essenciais coletadas através do *gem5*.

#### 4. Visualização dos Resultados
Os resultados parciais e o comportamento avaliado na pesquisa se encontram em formato de comparativos diretos. Todas as seções detêm gráficos elaborados (escalas corretas e legendas), unificados com uma discussão textual interpretando os impactos de cada métrica obtida nas subpastas.

#### 5. Reprodutibilidade
O repositório abriga os scripts para reprodução e visualização das simulações (`.py`, `.sh`, etc), as saídas processadas e um ambiente pronto. Dessa maneira, as submissões documentam com rigidez cada passo do ambiente testado.
