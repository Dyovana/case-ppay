# Como Rodar a Aplicação e os Testes

---

## Pré-requisitos

Para rodar a aplicação, você precisará dos seguintes **requisitos**:

* **Python 3.10+**
* **Docker**

---

## Como Rodar Localmente

Siga estes passos para configurar e executar a aplicação em sua máquina local:

1.  **Crie e Ative um Ambiente Virtual:**
    Abra seu terminal na raiz do projeto e execute os seguintes comandos:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2.  **Instale as Dependências:**
    Com o ambiente virtual ativado, instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Inicie o Banco de Dados com Docker Compose:**
    Navegue até a pasta `dev/` e inicie o Docker Compose para subir o banco de dados necessário para o funcionamento correto da aplicação:
    ```bash
    docker compose up -d
    ```

4.  **Execute a Aplicação:**
    Na raiz do projeto você pode iniciar a aplicação principal:
    ```bash
    python -m src.main
    ```

---

## Como Rodar os Testes

1.  **Instale as Dependências:**
    ```bash
    pip install -r requirements-dev.txt
    ```

2.  **Inicie o Docker Compose para Testes:**
    Este passo é essencial para testar serviços que interagem com o banco de dados. Navegue até a pasta de testes e inicie o Docker Compose específico:
    ```bash
    cd tests/dev-test
    docker compose up -d
    ```

3.  **Execute os Testes Unitários:**

---

# Escolhas Técnicas e Justificativas

---

## Framework Web: FastAPI

**FastAPI** foi a escolha natural para o desenvolvimento da API. Minha **familiaridade e experiência diária** com o framework me permitem desenvolver de forma **rápida**. Além disso, o FastAPI é conhecido por seu **alto desempenho**, **validação de dados automática** (com Pydantic) e **documentação interativa** (Swagger UI e ReDoc) gerada automaticamente, o que agiliza tanto o desenvolvimento quanto a utilização da API.

---

## Estrutura do Código: Services com Responsabilidades Únicas

A arquitetura do código foi pensada para promover a **modularidade e a clareza**. Adotei a criação de **"services" com responsabilidades únicas e simples**. Esse design facilita a **manutenção**, a **leitura** e a **extensibilidade** do código, uma vez que cada serviço é focado em uma tarefa específica e bem definida, minimizando acoplamentos.

---

## ORM: SQLAlchemy

A escolha do **SQLAlchemy** como Object-Relational Mapper (ORM) se deu por diversos motivos. Sua **abstração** permite interagir com o banco de dados utilizando objetos Python, eliminando a necessidade de escrever SQL manualmente. Isso não só **acelera o desenvolvimento** como também **reduz a probabilidade de erros**. Um ponto crucial é a **segurança** proporcionada pelo SQLAlchemy: ele **trata automaticamente as entradas para prevenir ataques de SQL Injection**, o que é fundamental para a integridade dos dados da aplicação.

---

## Banco de Dados: PostgreSQL

O **PostgreSQL** foi selecionado para armazenar os logs da aplicação. As principais razões para essa escolha incluem:

* **Confiabilidade e Robustez:** O PostgreSQL é um banco de dados **confiável** e **maduro**, amplamente utilizado em ambientes de produção.
* **Open Source:** Sendo de código aberto, oferece **flexibilidade** e uma **grande comunidade** de suporte.
* **Fácil Integração:** Sua compatibilidade e facilidade de integração com diversas aplicações e linguagens de programação são um diferencial.
* **Simplicidade para o Caso:** Para este caso específico, onde a tabela de logs é relativamente simples

---

## Docker

A utilização do **Docker** pois facilita bastante o desenvolvimento de apps que precisam de services terceiros, ex: bando de dados, etc...

---

# Propostas de Melhoria para a Aplicação

---

## Banco de Dados

* **Otimização para Dados Semi-Estruturados e Logs:** Uma melhoria seria a transição para um banco de dados mais adequado para dados semi-estruturados e eficiente no gerenciamento de logs, como **Elasticsearch** ou **MongoDB**. Esses bancos de dados são projetados para lidar com a flexibilidade e o volume de logs, oferecendo melhor desempenho para buscas e ingestão de dados.
* **Buscas Assíncronas:** Implementar o uso de **bibliotecas que suportem operações assíncronas** para acesso ao banco de dados. Isso tornará as buscas de dados mais eficientes e não bloqueantes, diminuindo a latência e melhorando significativamente a performance geral da aplicação.
* Recuperar informações sensíveis, como usuário e senha do banco de dados, a partir de uma fonte segura.
---

## Aplicação

* **Autenticação de Usuários:** É crucial implementar um sistema de autenticação para garantir que apenas usuários autorizados acessem a aplicação. A utilização de **JSON Web Tokens (JWT)** é uma opção robusta e flexível para gerenciar a autenticação de forma segura.

---

## Escalabilidade

* **Processamento Assíncrono Completo:** Transformar todas as rotas da aplicação e os processos que interagem com o banco de dados em **assíncronos**. Essa abordagem aumentará a eficiência da aplicação, permitindo que ela lide com um maior volume de requisições simultaneamente sem gargalos.
* **Infraestrutura Cloud e Kubernetes:** Adotar uma **infraestrutura em nuvem** combinada com **Kubernetes** para gerenciar a escalabilidade horizontal. Isso permitirá a alocação automática de mais instâncias e recursos conforme a demanda, além de garantir o balanceamento de tráfego uniforme entre as instâncias, otimizando a disponibilidade e o desempenho.

---

## Observabilidade

* **Tracing e Spans com OpenTelemetry:** Implementar **logs de traces/spans** em todas as rotas e serviços da aplicação. Isso permitirá visualizar o fluxo completo das requisições, entender como os dados são processados e modificados, e facilitar o debug rápido em caso de falhas, identificando o trecho exato que causou o problema. Ferramentas como **Grafana Tempo** e **OpenTelemetry** são ideais para essa finalidade.
* **Métricas e Alertas Abrangentes:** Estabelecer um sistema de **métricas** para monitorar a saúde da aplicação, incluindo o número de requisições com erro, latência e uso de recursos. Além disso, configurar **alertas** para qualquer anomalia nessas métricas permitirá a detecção e resolução rápida de problemas, minimizando o impacto nos usuários.

---