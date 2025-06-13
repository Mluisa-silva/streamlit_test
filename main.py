import streamlit as st
import pandas as pd
import streamlit as st
import google.generativeai as genai

api_key = st.secrets("API_KEY")
genai.configure(api_key=api_key)

try:
    # Utilizando o modelo especificado
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Erro ao carregar o modelo Gemini 'gemini-2.0-flash': {e}")
    st.info("Verifique se o nome do modelo está correto e se sua chave API tem acesso a ele.")
    st.stop()

def gerar_resposta_gemini(prompt_completo):
    try:
        response = model.generate_content(prompt_completo)

        if response.parts:
            return response.text
        else:
            if response.prompt_feedback:
                st.warning(f"O prompt foi bloqueado. Razão: {response.prompt_feedback.block_reason}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        st.caption(f"Categoria: {rating.category}, Probabilidade: {rating.probability}")
            return "A IA não pôde gerar uma resposta para este prompt. Verifique as mensagens acima ou tente reformular seu pedido."
    except Exception as e:
        st.error(f"Erro ao gerar resposta da IA: {str(e)}")
        if hasattr(e, 'message'): # Tenta obter mais detalhes do erro da API do Gemini
            st.error(f"Detalhe da API Gemini: {e.message}")
        return None

st.title("Exercício: CRIADOR DE HISTÓRIAS INTERATIVAS")

nome_protagonista = st.text_input("Qual o nome do seu protagonista?")

genero = st.selectbox(
    "Escolha o Gênero Literário da sua narrativa:",
    ["Fantasia", "Ficção Científica", "Mistério", "Aventura", "Romance", "Drama"]
)

local_inicial = st.radio(
    "Escolha o Local Inicial da História",
    ["Uma floresta antiga", "Uma cidade futurista", "Um castelo assombrado", "Uma nave espacial à deriva","Um barco naufragado", "Uma ilha deserta"]
)

frase_desafio = st.text_area("Adicione uma frase ou desafio inicial a história: ", height=100)

if st.button("📝 Gerar Início da História"):
    if nome_protagonista.strip() == "" or frase_desafio.strip() == "":
        st.warning("Por favor, preencha o nome do protagonista e a frase de desafio.")
    else:
        prompt = (
            f"Crie o início de uma história do gênero '{genero}' com o protagonista chamado '{nome_protagonista}'. "
            f"A história começa em '{local_inicial}'. Incorpore a seguinte frase ou desafio no início: "
            f"'{frase_desafio}'. Escreva um ou dois parágrafos envolventes e criativos."
        )

        historia_gerada = gerar_resposta_gemini(prompt)

        st.subheader("✨ Início da História Gerada")
        if historia_gerada:
            st.write(historia_gerada)
        else:
            st.error("A IA não conseguiu gerar uma resposta. Tente novamente com outro prompt.")