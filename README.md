## 📄 Documentação Detalhada do Projeto Streamlit/Groq para GitHub

Este projeto apresenta um **"Debate de Modelos de Linguagem"** interativo, utilizando a plataforma **Streamlit** para a interface de usuário e a API de inferência de alta velocidade da **Groq** para orquestrar as respostas de dois modelos de linguagem distintos (simulando um **GPT-OSS** e um **Llama-4**).

O objetivo principal é simular um debate estruturado, onde os modelos respondem a um tópico proposto em rodadas sequenciais (Abertura, Argumentação Principal, Réplica, Perguntas Cruzadas e Conclusão), com o histórico de mensagens mantido para contextualizar cada resposta.

-----

### 🚀 Configuração e Pré-requisitos

Para rodar este projeto localmente, você precisará ter o **Python** instalado e uma **Chave de API da Groq**.

#### 1\. Instalação de Dependências

Instale as bibliotecas necessárias usando `pip`:

```bash
pip install streamlit groq
```

#### 2\. Configuração da Chave Groq API

Embora a chave esteja codificada diretamente no *script* (como visto no código `GROQ_API_KEY = "..."`), a **melhor prática e o método recomendado** para projetos públicos é usar o sistema de *secrets* do Streamlit para manter a chave segura.

Crie um arquivo chamado `.streamlit/secrets.toml` na raiz do seu projeto (ou configure a variável de ambiente `GROQ_API_KEY`).

**Exemplo de `.streamlit/secrets.toml`:**

```toml
GROQ_API_KEY = "SUA_CHAVE_GROQ_AQUI"
```

Se você optar por usar o método de **variável de ambiente** em um ambiente de *cloud* ou CI/CD, defina `GROQ_API_KEY`.

-----

### ⚙️ Estrutura e Componentes do Código

O script é dividido em seções lógicas, conforme detalhado abaixo:

#### 1\. Configurações Iniciais e Chave API

  * **Importações:** Importa `streamlit`, `Groq` e `os`.
  * **Configuração de Página:** `st.set_page_config` define o título da aba e o layout como `wide`.
  * **Inicialização da Groq:** A chave API é lida (ou, no seu código, codificada) e o cliente `Groq` é inicializado.

<!-- end list -->

```python
# ...
client = Groq(api_key=GROQ_API_KEY)
# ...
```

#### 2\. Definição de Modelos e Variáveis de Debate

Define as constantes usadas para identificar e configurar os "debatentes":

| Variável | Valor Simulado | Descrição |
| :--- | :--- | :--- |
| `MODEL_1_NAME` | `GPT-OSS-120B` | Nome de exibição para o modelo do lado direito (vermelho). |
| `MODEL_1_ID` | `openai/gpt-oss-120b` | ID de modelo **simulado** para a chamada à API. |
| `MODEL_2_NAME` | `Llama-4-Maverick` | Nome de exibição para o modelo do lado esquerdo (azul). |
| `MODEL_2_ID` | `meta-llama/llama-4-maverick-17b-128e-instruct` | ID de modelo **simulado** para a chamada à API. |
| `SYSTEM_INSTRUCTION` | (Texto em português) | Instrução de sistema que define o papel do modelo como "debatedor profissional". |

#### 3\. Gestão de Estado e Histórico

Utiliza o `st.session_state` do Streamlit para manter o estado da aplicação entre as interações:

  * `st.session_state.history`: Lista de dicionários no formato Groq (`{"role": "assistant", "content": "..."}`), usada para manter o **contexto** do debate.
  * `st.session_state.debate_started`: Booleano para rastrear se um debate está em andamento.

#### 4\. Função Central de API (`get_response`)

Essa função é o *wrapper* para a chamada à Groq API.

  * Ela constrói a lista de mensagens, incluindo a `SYSTEM_INSTRUCTION`, o `history` do debate e o `prompt` da rodada atual.
  * Faz a chamada `client.chat.completions.create` usando o `model_id` e parâmetros de configuração como `max_tokens` e `temperature`.

#### 5\. Funções de Orquestração do Debate

##### A. `run_debate_step`

Esta função executa uma rodada do debate, crucial para a estrutura do projeto:

1.  Recebe o nome da etapa (`step_name`) e os *prompts* individuais (`prompt_1`, `prompt_2`).
2.  Chama `get_response` para o **Modelo 1** (GPT) e, em seguida, para o **Modelo 2** (Llama).
3.  **Atualiza o Histórico:** Após cada resposta, a função *adiciona a resposta do modelo* (com seu emoji e nome) ao `st.session_state.history`. Isso garante que o próximo modelo veja a resposta do seu oponente.
4.  Exibe as respostas lado a lado usando `st.columns(2)`.

##### B. `start_debate`

Esta função orquestra o fluxo completo do debate, chamando `run_debate_step` para cada uma das etapas:

1.  **Abertura:** Definição inicial da posição.
2.  **Argumentação Principal:** Desenvolvimento e reforço da posição.
3.  **Réplica (Refutação):** Refutação direta do argumento principal do oponente (o código extrai os últimos argumentos do histórico para criar o *prompt* de refutação).
4.  **Perguntas Cruzadas:** Etapa de maior complexidade, onde:
      * Um modelo **formula** uma pergunta.
      * O oponente **responde**.
      * O histórico é atualizado após cada sub-etapa.
5.  **Conclusão:** Resumo e argumentos finais.

-----

### ▶️ Como Executar o Projeto

1.  Certifique-se de que a chave Groq API está configurada.
2.  Salve o código como um arquivo Python (ex: `debate_app.py`).
3.  Execute o Streamlit a partir do seu terminal:

<!-- end list -->

```bash
streamlit run debate_app.py
```

O aplicativo será aberto no seu navegador, permitindo que você selecione ou insira um tópico e inicie o debate.

-----

Obrigado!
