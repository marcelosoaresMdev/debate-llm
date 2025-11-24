import streamlit as st
from groq import Groq
import os

# --- Configurações Iniciais ---
st.set_page_config(
    page_title="Debate de Modelos de Linguagem com Groq",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🤖 Debate Entre Modelos de Linguagem - Meta e GPT")


# --- Configuração de Modelos e Variáveis ---
try:
    # A chave da API deve estar configurada em .streamlit/secrets.toml
    GROQ_API_KEY = "COLE SUA CHAVE API GROQ AQUI"
except KeyError:
    st.error("ERRO: A chave da API da Groq não foi encontrada!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_INSTRUCTION = (
    "Você é um debatedor profissional que deve defender seu ponto de vista seguindo as regras do debate. "
    "Seja conciso, mas persuasivo, e adapte-se ao argumento do seu oponente. O nome do modelo será usado para identificá-lo."
    "Todas as repostas devem ser no idioma Porguês Brasil."
    "Você não pode gerar nenhuma resposta racista, expressões grosseiras, ofensivas, obscenas ou vulgares que causam constrangimento em ambientes formais e são inadequadas na norma culta da língua"
)

# DEFINIÇÕES: Nomes Técnicos dos Modelos (Limpo)
EMOJI_1 = "🎓" 
MODEL_1_NAME = "GPT-OSS-120B"       # Modelo no Lado Direito (GPT)
MODEL_1_ID = "openai/gpt-oss-120b" 

EMOJI_2 = "🦁" 
MODEL_2_NAME = "Llama-4-Maverick"  # Modelo no Lado Esquerdo (Meta/Llama)
MODEL_2_ID = "meta-llama/llama-4-maverick-17b-128e-instruct" 

DEFAULT_TOPIC = "A substituirá completamente o trabalho humano?"
SUGGESTED_TOPICS = [
    DEFAULT_TOPIC,
    "Deveria haver um limite para o avanço da Iinteligência Artificial",
]

if "history" not in st.session_state:
    st.session_state.history = []
if "debate_started" not in st.session_state:
    st.session_state.debate_started = False

# --- Funções de API (Inalterada) ---
def get_response(model_id: str, history: list, prompt: str, system_instruction: str) -> str:
    messages = [{"role": "system", "content": system_instruction}]
    messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=800, 
            temperature=0.7 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao obter resposta do modelo {model_id}: {e}"

# --- Funções do Debate ---

def run_debate_step(step_name: str, prompt_1: str, prompt_2: str):
    """Executa uma rodada de debate, atualiza o histórico e exibe o resultado."""
    st.markdown(f"## 🗣️ {step_name}")
    
    # Modelo 1 (GPT-OSS-20B - Direita)
    with st.spinner(f"Aguardando a resposta de {MODEL_1_NAME} ({step_name})..."):
        response_1 = get_response(MODEL_1_ID, st.session_state.history, prompt_1, SYSTEM_INSTRUCTION)
    st.session_state.history.append({"role": "assistant", "content": f"{EMOJI_1} {MODEL_1_NAME}: {response_1}"})
    
    # Modelo 2 (Llama-4-Maverick - Esquerda)
    with st.spinner(f"Aguardando a resposta de {MODEL_2_NAME} ({step_name})..."):
        response_2 = get_response(MODEL_2_ID, st.session_state.history, prompt_2, SYSTEM_INSTRUCTION)
    st.session_state.history.append({"role": "assistant", "content": f"{EMOJI_2} {MODEL_2_NAME}: {response_2}"})

    # Exibe as respostas: Llama (col1 - Esquerda) e GPT (col2 - Direita)
    col1, col2 = st.columns(2)
    with col1:
        # TÍTULO LIMPO: Apenas Emoji + Nome Técnico
        st.subheader(f"{EMOJI_2} {MODEL_2_NAME}", divider='blue')
        st.markdown(response_2)
    with col2:
        # TÍTULO LIMPO: Apenas Emoji + Nome Técnico
        st.subheader(f"{EMOJI_1} {MODEL_1_NAME}", divider='red')
        st.markdown(response_1)
        
    st.markdown("---") 

def start_debate(topic: str):
    """Inicia todo o ciclo de debate."""
    st.session_state.debate_started = True
    st.session_state.history = [] 

    st.header(f"Tema do Debate: **{topic}**")
    st.markdown("---")

    # Abertura
    run_debate_step(
        "Abertura (Introdução)",
        f"Tópico: {topic}. Defenda seu ponto de vista de forma introdutória, estabelecendo sua posição.",
        f"Tópico: {topic}. Defenda seu ponto de vista de forma introdutória, estabelecendo sua posição."
    )

    # Argumentação Principal
    run_debate_step(
        "Argumentação Principal",
        f"Desenvolva sua argumentação principal e reforce sua posição, considerando o que foi dito na abertura.",
        f"Desenvolva sua argumentação principal e reforce sua posição, considerando o que foi dito na abertura."
    )
    
    # Réplica
    last_meta_argument = st.session_state.history[-1]['content'].split(': ', 1)[1].strip()
    last_openai_argument = st.session_state.history[-2]['content'].split(': ', 1)[1].strip()

    run_debate_step(
        "Réplica (Refutação)",
        f"Refute o argumento principal de seu oponente: '{last_meta_argument}'.",
        f"Refute o argumento principal de seu oponente: '{last_openai_argument}'."
    )

    # === 4. Perguntas Cruzadas (CORRIGIDO) ===
    st.markdown("## 💬 Perguntas Cruzadas")
    
    # 4a. Pergunta do Modelo 1 (GPT)
    with st.spinner(f"Criando pergunta desafiadora de {MODEL_1_NAME}..."):
        openai_question = get_response(MODEL_1_ID, st.session_state.history, "Formule uma pergunta desafiadora baseada no debate até agora.", SYSTEM_INSTRUCTION)
    st.session_state.history.append({"role": "assistant", "content": f"{EMOJI_1} {MODEL_1_NAME} pergunta: {openai_question}"})
    
    # 4b. Resposta do Modelo 2 (Llama)
    with st.spinner(f"Aguardando a resposta de {MODEL_2_NAME} para a pergunta do {MODEL_1_NAME}..."):
        meta_answer = get_response(MODEL_2_ID, st.session_state.history, f"Responda à seguinte pergunta do seu oponente: {openai_question}", SYSTEM_INSTRUCTION)
    st.session_state.history.append({"role": "assistant", "content": f"{EMOJI_2} {MODEL_2_NAME} responde: {meta_answer}"})

    col1_q, col2_a = st.columns(2)
    
    with col1_q:
        # TÍTULO LIMPO
        st.subheader(f"{EMOJI_2} {MODEL_2_NAME}", divider='blue') 
        # CONTEÚDO LIMPO: Apenas a resposta, com um prefixo de contexto
        st.markdown(f"**Resposta à Pergunta de {MODEL_1_NAME}:**\n\n{meta_answer}")
        
    with col2_a:
        # TÍTULO LIMPO
        st.subheader(f"{EMOJI_1} {MODEL_1_NAME}", divider='red') 
        # CONTEÚDO LIMPO: Apenas a pergunta, com um prefixo de contexto
        st.markdown(f"**Pergunta para {MODEL_2_NAME}:**\n\n{openai_question}")

    st.markdown("---")

    # 4c. Pergunta do Modelo 2 (Llama)
    with st.spinner(f"Criando pergunta desafiadora de {MODEL_2_NAME}..."):
        meta_question = get_response(MODEL_2_ID, st.session_state.history, "Formule uma pergunta desafiadora baseada no debate até agora.", SYSTEM_INSTRUCTION)
    st.session_state.history.append({"role": "assistant", "content": f"{EMOJI_2} {MODEL_2_NAME} pergunta: {meta_question}"})

    # 4d. Resposta do Modelo 1 (GPT)
    with st.spinner(f"Aguardando a resposta de {MODEL_1_NAME} para a pergunta do {MODEL_2_NAME}..."):
        openai_answer = get_response(MODEL_1_ID, st.session_state.history, f"Responda à seguinte pergunta do seu oponente: {meta_question}", SYSTEM_INSTRUCTION)
    st.session_state.history.append({"role": "assistant", "content": f"{EMOJI_1} {MODEL_1_NAME} responde: {openai_answer}"})
    
    col1_a, col2_q = st.columns(2)
    
    with col1_a:
        # TÍTULO LIMPO
        st.subheader(f"{EMOJI_2} {MODEL_2_NAME}", divider='blue')
        # CONTEÚDO LIMPO
        st.markdown(f"**Pergunta para {MODEL_1_NAME}:**\n\n{meta_question}")
        
    with col2_q:
        # TÍTULO LIMPO
        st.subheader(f"{EMOJI_1} {MODEL_1_NAME}", divider='red')
        # CONTEÚDO LIMPO
        st.markdown(f"**Resposta à Pergunta de {MODEL_2_NAME}:**\n\n{openai_answer}")

    st.markdown("---")


    # Conclusão
    run_debate_step(
        "Conclusão",
        "Faça uma conclusão final e definitiva, resumindo seus melhores pontos e considerando todo o debate.",
        "Faça uma conclusão final e definitiva, resumindo seus melhores pontos e considerando todo o debate."
    )
    
    st.success("🎉 O debate foi concluído!")


# --- Configurações de Entrada no Painel Principal (Inalterado) ---

st.header("⚙️ Selecione ou digite um tópico de debate:")

selected_topic = st.selectbox(
  "",
    options=SUGGESTED_TOPICS,
    index=SUGGESTED_TOPICS.index(DEFAULT_TOPIC)
)

custom_topic = st.text_input("Ou digite seu próprio tópico:", value="")
final_topic = custom_topic if custom_topic else selected_topic

if st.button("🚀 Iniciar Novo Debate", type="primary"):
    st.session_state.history = []
    st.session_state.debate_started = False
    start_debate(final_topic)

st.markdown("---")

if st.session_state.debate_started and not st.session_state.history:
    st.info("Iniciando o debate...")
elif not st.session_state.debate_started:
    st.info("Aperte 'Iniciar Novo Debate' acima para começar.")