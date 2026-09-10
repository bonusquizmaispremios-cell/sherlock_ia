import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SHERLOCK IA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_sherlock():
    return {"perfis": {}}

_cache = get_cache_sherlock()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_casos', 'casos_salvos',
    'caso_padrao', 'diario_investigador', 'desafio_pontuacao', 'desafio_nivel_atual',
    'casos_resolvidos_count', 'evidencias_cadastradas_count',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_caso(modulo: str, tema: str, conteudo: str):
    st.session_state.historico_casos.append({
        'data': datetime.now().strftime('%d/%m %H:%M'), 'modulo': modulo, 'tema': tema, 'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_casos': [], 'casos_salvos': [],
    'caso_padrao': "", 'diario_investigador': [], 'desafio_pontuacao': 0, 'desafio_nivel_atual': "Iniciante",
    'casos_resolvidos_count': 0, 'evidencias_cadastradas_count': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

NIVEIS_DESAFIO = ["Iniciante", "Investigador", "Inspetor", "Mestre", "Sherlock"]
CLASSES_NIVEL = {"Iniciante":"badge-nivel-iniciante","Investigador":"badge-nivel-investigador","Inspetor":"badge-nivel-inspetor","Mestre":"badge-nivel-mestre","Sherlock":"badge-nivel-sherlock"}

# --- PRINCÍPIO DE RIGOR LÓGICO E RESPONSABILIDADE — compartilhado ---
PRINCIPIO_RIGOR = """
PRINCÍPIO OBRIGATÓRIO DE RIGOR LÓGICO E RESPONSABILIDADE — siga isso em TODA resposta:
- Você é um consultor de raciocínio lógico e investigação, inspirado no método de observação, dedução e eliminação
  de hipóteses — mas você NÃO é perito forense oficial, detetive licenciado, psicólogo ou advogado
- Trabalhe SEMPRE a partir do que foi descrito em texto pela pessoa — você não recebe fotos, vídeos ou áudios reais,
  então para "análise de imagem" trabalhe com a descrição detalhada que a pessoa fornecer
- NUNCA afirme com certeza absoluta que algo é verdade sobre uma pessoa real e terceira (ex: "ele está mentindo",
  "ela está tendo um caso") — use sempre linguagem de hipótese: "isso poderia indicar", "um padrão possível seria",
  "vale considerar, mas não é conclusivo"
- Para Perfil Comportamental e Análise de Conversas envolvendo pessoas reais: trate tudo como HIPÓTESES para reflexão
  do próprio usuário, nunca como diagnóstico ou prova. Lembre, quando relevante, que ler demais nas entrelinhas de
  mensagens reais tem limites — más interpretações são comuns e a melhor fonte de verdade é conversar diretamente
  com a pessoa envolvida
- Para o Laboratório Forense Educativo: explique COMO a ciência forense funciona em princípio (conceitos, método,
  cadeia de custódia) — isso é educativo. NUNCA forneça instruções operacionais sobre como evitar, burlar ou enganar
  uma perícia real (remover vestígios, burlar coleta de DNA, etc) — se a pergunta pedir isso, redirecione para o
  aspecto educativo de como a perícia funciona, sem fornecer o "como evitar ser detectado"
- Para Fraudes e Golpes / Investigação Digital: foco é proteção e reconhecimento, nunca como executar um golpe
- Casos, mistérios e desafios do Simulador, Sala de Casos Impossíveis e Academia Sherlock são sempre FICTÍCIOS —
  invente livremente, com boa qualidade narrativa e lógica consistente
- Você pode e deve ser envolvente, dramático e didático no tom — isso é parte da experiência — mas a responsabilidade
  com fatos reais e pessoas reais é inegociável
- Português do Brasil
"""

DISCLAIMER_PADRAO = """
<div class="disclaimer">
⚠️ <strong>Importante:</strong> esta análise é um exercício de raciocínio lógico para apoiar sua reflexão — não é uma
prova, diagnóstico ou conclusão definitiva. Hipóteses geradas por IA podem estar erradas; a melhor fonte de verdade
sobre uma situação real é sempre investigação cuidadosa e, quando envolve outra pessoa, conversa direta com ela.
</div>
"""

DISCLAIMER_COMPORTAMENTAL = """
<div class="disclaimer-comportamental">
🧠 <strong>Sobre esta análise comportamental:</strong> isso é uma hipótese especulativa para reflexão, nunca um
diagnóstico psicológico ou prova de intenção. Comportamentos têm múltiplas explicações possíveis, e interpretações
à distância são frequentemente erradas. Use isso como ponto de partida para pensar, não como conclusão.
</div>
"""

DISCLAIMER_FORENSE = """
<div class="disclaimer-forense">
🧪 <strong>Conteúdo educativo:</strong> esta seção explica princípios gerais de ciência forense para fins de
aprendizado — não é um manual operacional, não substitui peritos reais, e não deve ser usada para interferir em
investigações ou evidências reais.
</div>
"""

# --- MOTOR DE IA ---
def sherlock_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é Sherlock IA — um consultor de investigação lógica, raciocínio dedutivo e pensamento
crítico, inspirado nos grandes métodos investigativos clássicos.
Usuário: {st.session_state.usuario}. Caso atual: {st.session_state.caso_padrao or 'não informado'}.
{PRINCIPIO_RIGOR}
{system_extra}"""
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def renderizar_indice(texto: str, titulo_indice: str = "CONSISTÊNCIA"):
    percentuais = re.findall(r'(\d+)\s*/\s*100|(\d+)%', texto)
    valores = [int(a or b) for a, b in percentuais if a or b]
    indice = valores[0] if valores else 50

    if indice >= 70:
        classe, emoji, label = "indice-alto", "🟢", "ALTA"
    elif indice >= 40:
        classe, emoji, label = "indice-medio", "🟡", "MÉDIA"
    else:
        classe, emoji, label = "indice-baixo", "🔴", "BAIXA"

    st.markdown(f"""
    <div class="indice-box {classe}">
        <div style="font-size:2.2em;">{emoji}</div>
        <div class="indice-titulo">{titulo_indice}: {indice}/100</div>
        <div style="font-size:0.95em;color:#444;font-weight:600;">Nível: {label}</div>
        <div style="font-size:0.82em;color:#555;margin-top:6px;">Estimativa baseada nas informações fornecidas</div>
    </div>
    """, unsafe_allow_html=True)

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_casos)
    diario = len(st.session_state.diario_investigador)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F1F5F9;border:1px solid #334155;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} análises geradas · {diario} casos no diário</span>"
            f"</div>", unsafe_allow_html=True
        )
    with col_btn:
        st.download_button("💾 SALVAR MEUS DADOS (.json)", data=gerar_json_sessao(),
            file_name=f"sherlock_ia_{nome_usuario}.json", mime="application/json", use_container_width=True, key="sherlock16")
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'caso_padrao' not in st.session_state: st.session_state['caso_padrao'] = None
if 'casos_resolvidos_count' not in st.session_state: st.session_state['casos_resolvidos_count'] = None
if 'casos_salvos' not in st.session_state: st.session_state['casos_salvos'] = None
if 'desafio_nivel_atual' not in st.session_state: st.session_state['desafio_nivel_atual'] = None
if 'desafio_pontuacao' not in st.session_state: st.session_state['desafio_pontuacao'] = None
if 'diario_investigador' not in st.session_state: st.session_state['diario_investigador'] = None
if 'evidencias_cadastradas_count' not in st.session_state: st.session_state['evidencias_cadastradas_count'] = None
if 'historico_casos' not in st.session_state: st.session_state['historico_casos'] = []

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 SHERLOCK IA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 quizcompremios.com.br</div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS
    _tab_Home, _tab_Investigacao, _tab_Hipoteses, _tab_Evidencias, _tab_Timeline, _tab_Contradicoes, _tab_Perfil, _tab_Conversas, _tab_Imagens, _tab_Domestica, _tab_Digital, _tab_Fraudes, _tab_Padroes, _tab_Probabilidades, _tab_Perguntas, _tab_Critico, _tab_Metodo, _tab_Forense, _tab_Casos, _tab_Simulador, _tab_Diario, _tab_Painel, _tab_Academia, _tab_Desafio, _tab_Sherlock24, _tab_CasosImpossiveis, _tab_Biblioteca = st.tabs(['🏠 Painel Principal', '🔎 Investigação Geral', '🧩 Construção de Hipó', '📋 Organizador de Evi', '📄 Timeline', '📄 Contradicoes', '📄 Perfil', '📄 Conversas', '📄 Imagens', '📄 Domestica', '📄 Digital', '📄 Fraudes', '📄 Padroes', '📄 Probabilidades', '📄 Perguntas', '📄 Critico', '📄 Metodo', '📄 Forense', '📄 Casos', '📄 Simulador', '📄 Diario', '📄 Painel', '📄 Academia', '📄 Desafio', '📄 Sherlock24', '📄 CasosImpossiveis', '📄 Biblioteca'])


    # TABS — navegação nativa (16 + Ferramentas)
    (_tab_Home, _tab_Investigacao, _tab_Hipoteses, _tab_Evidencias, _tab_Timeline, _tab_Simulador, _tab_Diario, _tab_Painel, _tab_Academia, _tab_Desafio, _tab_Sherlock24, _tab_CasosImpossiveis, _tab_Biblioteca, _tab_Forense, _tab_Casos, _tab_Ferramentas) = st.tabs(['🏠 Home', '🔍 Investigação', '💡 Hipóteses', '🔬 Evidências', '⏱️ Timeline', '🎯 Simulador', '📖 Diário', '📈 Painel', '🎓 Academia', '🏆 Desafio', '🤖 Sherlock 24h', '💎 Casos Impossíveis', '📚 Biblioteca', '🧪 Lab Forense', '📋 Casos Históricos', '🛠️ Ferramentas'])

    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 🕵️")
            nivel_atual = st.session_state.desafio_nivel_atual
            st.markdown(f"<span class='{CLASSES_NIVEL.get(nivel_atual,'badge')}'>{nivel_atual}</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="sherlock3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_casos) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        st.session_state.caso_padrao = st.text_area("🔎 Caso/situação que você está investigando:",
            value=st.session_state.caso_padrao, height=80,
            placeholder="ex: Estou tentando entender um problema estranho que aconteceu no trabalho...", key="sherlock15")


        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_casos)}</div><div>Análises geradas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.casos_resolvidos_count}</div><div>Casos resolvidos</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.evidencias_cadastradas_count}</div><div>Evidências cadastradas</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.desafio_pontuacao}</div><div>Pontos no Desafio</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>🕵️ <em>'Quando você elimina o impossível, o que restar, ainda que improvável, deve ser a verdade.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada módulo faz")
        guia = {
            "🔎 Investigação Geral": "Descreva qualquer situação — fatos, pessoas, linha do tempo e hipóteses organizados",
            "🧩 Construção de Hipóteses": "Cenários possíveis com probabilidade, pontos a favor e contra",
            "📋 Organizador de Evidências": "Cadastre fotos, documentos, locais, datas e pessoas de um caso",
            "⏳ Linha do Tempo": "Reconstrói a sequência dos acontecimentos e identifica lacunas",
            "🎭 Detector de Contradições": "Cole relatos e identifique mudanças de versão e conflitos",
            "👤 Perfil Comportamental": "Hipóteses sobre padrões de comportamento — nunca diagnóstico",
            "💬 Análise de Conversas": "Tom, contradições, assuntos evitados em conversas que você já tem",
            "📸 Análise de Imagens": "Descreva uma cena em detalhes para análise investigativa",
            "🏠 Investigação Doméstica": "Vazamentos, ruídos, cheiros, infiltrações — descubra a causa",
            "💻 Investigação Digital": "Sites suspeitos, perfis falsos, engenharia social",
            "💰 Fraudes e Golpes": "Como funcionam, como identificar e como se proteger",
            "🔍 Detector de Padrões": "Relações escondidas entre datas, pessoas, lugares e eventos",
            "📊 Análise de Probabilidades": "Quais hipóteses são mais consistentes com as evidências",
            "❓ Perguntas Inteligentes": "As perguntas que um investigador faria e você talvez não pensou",
            "⚖️ Pensamento Crítico": "Identifique vieses, generalizações e julgamentos precipitados",
            "🧠 Método Sherlock": "Dedução, indução, abdução e eliminação de hipóteses",
            "🧪 Laboratório Forense": "Como funcionam impressões digitais, DNA, balística — educativo",
            "📚 Casos Históricos": "Investigações famosas e o raciocínio usado para resolvê-las",
            "🎯 Simulador de Investigação": "Casos fictícios por categoria e nível de dificuldade",
            "📖 Diário do Investigador": "Salve casos, hipóteses e conclusões",
            "📈 Painel Investigativo": "Acompanhe sua evolução como investigador",
            "🎓 Academia Sherlock": "30 aulas práticas de raciocínio investigativo",
            "🏆 Desafio Sherlock": "5 níveis de dificuldade — de Iniciante a Sherlock",
            "🤖 Sherlock 24h": "Converse livremente sobre qualquer investigação",
            "💎 Sala de Casos Impossíveis": "Dossiês complexos que se revelam por etapas",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_casos:
            st.markdown("### 🕐 Últimas Análises")
            for item in reversed(st.session_state.historico_casos[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item.get('modulo', '')}</span> <small style='color:#888'>{item['data']}</small><br><small>{item.get('tema', '')[:80]}</small></div>", unsafe_allow_html=True)

        # ========================
        # INVESTIGAÇÃO GERAL
        # ========================

    with _tab_Investigacao:
        st.header("🔎 Investigação Geral")
        st.markdown("Descreva a situação. A IA organiza fatos, hipóteses e próximos passos.")

        situacao_inv = st.text_area("📝 Descreva a situação:", height=180, value=st.session_state.caso_padrao,
            placeholder="ex: Notei que um objeto da minha casa desapareceu, e três pessoas estiveram aqui na última semana...", key="sherlock14")

        if st.button("🔎 INVESTIGAR", key="sherlock4"):
            if situacao_inv.strip():
                with st.spinner("Organizando a investigação..."):
                    prompt = (
                        f"Organize uma investigação completa para esta situação.\n"
                        f"Situação: {situacao_inv}\n\n"
                        f"FORMATO:\n\n"
                        f"🔎 INVESTIGAÇÃO — {situacao_inv[:50].upper()}\n\n"
                        f"✅ FATOS CONHECIDOS:\n[liste o que é certo, com base no que foi descrito]\n\n"
                        f"❓ FATOS DESCONHECIDOS:\n[o que ainda não se sabe]\n\n"
                        f"👥 PESSOAS ENVOLVIDAS:\n[liste com o papel de cada uma na situação, se mencionadas]\n\n"
                        f"📅 LINHA DO TEMPO PRELIMINAR:\n[ordene os eventos descritos]\n\n"
                        f"🔍 EVIDÊNCIAS DISPONÍVEIS:\n[o que já se tem para analisar]\n\n"
                        f"🧩 HIPÓTESES INICIAIS:\n[2-4 possibilidades, todas como hipóteses, não conclusões]\n\n"
                        f"❓ PERGUNTAS IMPORTANTES:\n[o que precisa ser perguntado/descoberto a seguir]\n\n"
                        f"✅ PRÓXIMOS PASSOS DA INVESTIGAÇÃO:\n[ações concretas para avançar]"
                    )
                    res = sherlock_ia(prompt)
                    salvar_caso("Investigacao", situacao_inv[:60], res)
                    st.session_state['inv_temp'] = res
                    st.session_state.caso_padrao = situacao_inv
            else:
                st.warning("Descreva a situação.")

        if st.session_state.get('inv_temp'):
            st.markdown(f"<div class='card'>{st.session_state['inv_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['inv_temp'], file_name="investigacao.txt", mime="text/plain", use_container_width=True, key="sherlock5")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_inv", use_container_width=True):
                    st.session_state.casos_salvos.append({'modulo':'Investigacao','tema':situacao_inv[:60] if 'situacao_inv' in dir() else '','conteudo':st.session_state['inv_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # CONSTRUÇÃO DE HIPÓTESES
        # ========================

    with _tab_Hipoteses:
        st.header("🧩 Construção de Hipóteses")

        situacao_hip = st.text_area("📝 Descreva a situação:", height=120, value=st.session_state.caso_padrao, key="situacao_hip")
        qtd_hip = st.slider("Quantas hipóteses gerar:", 2, 6, 3, key="sherlock1")

        if st.button("🧩 GERAR HIPÓTESES", key="sherlock6"):
            if situacao_hip.strip():
                with st.spinner("Construindo hipóteses..."):
                    prompt = (
                        f"Crie {qtd_hip} hipóteses distintas para explicar esta situação.\n"
                        f"Situação: {situacao_hip}\n\n"
                        f"Para CADA hipótese:\n\n"
                        f"🧩 HIPÓTESE [N]: [nome curto]\n"
                        f"[Descrição da hipótese]\n"
                        f"📊 Probabilidade estimada: [Baixa/Média/Alta]\n"
                        f"✔ Pontos favoráveis: [o que sustenta essa hipótese]\n"
                        f"✘ Pontos contrários: [o que a contradiz ou fragiliza]\n"
                        f"🔍 Evidências necessárias para confirmar: [o que ajudaria a provar isso]\n"
                        f"❓ O que ainda precisa ser descoberto:\n\n"
                        f"[Repita para as {qtd_hip} hipóteses]\n\n"
                        f"🎯 HIPÓTESE MAIS CONSISTENTE ATÉ AGORA:\n[qual parece mais provável com base no que foi descrito, e por quê — sem afirmar certeza]"
                    )
                    res = sherlock_ia(prompt)
                    salvar_caso("Hipoteses", situacao_hip[:60], res)
                    st.session_state['hip_temp'] = res
            else:
                st.warning("Descreva a situação.")

        if st.session_state.get('hip_temp'):
            st.markdown(f"<div class='card'>{st.session_state['hip_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['hip_temp'], file_name="hipoteses.txt", mime="text/plain", use_container_width=True, key="sherlock7")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_hip", use_container_width=True):
                    st.session_state.casos_salvos.append({'modulo':'Hipoteses','tema':situacao_hip[:60] if 'situacao_hip' in dir() else '','conteudo':st.session_state['hip_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # ORGANIZADOR DE EVIDÊNCIAS
        # ========================

    with _tab_Evidencias:
        st.header("📋 Organizador de Evidências")
        st.markdown("Cadastre evidências do seu caso — tudo fica organizado automaticamente.")

        col1, col2 = st.columns(2)
        with col1:
            tipo_evid = st.selectbox("Tipo de evidência:", ["📸 Foto (descrição)","🎥 Vídeo (descrição)","🎙 Áudio (descrição)","📄 Documento","💬 Conversa","📍 Local","📅 Data/Horário","👥 Pessoa"], key="sherlock8")
            descricao_evid = st.text_area("📝 Descrição da evidência:", height=100, placeholder="ex: Mensagem recebida às 14h32 dizendo que estava no trabalho...", key="sherlock9")
        with col2:
            relevancia_evid = st.selectbox("Relevância:", ["Alta","Média","Baixa","A determinar"], key="sherlock10")
            notas_evid = st.text_input("Notas adicionais (opcional):", placeholder="ex: confirmar com testemunha...", key="sherlock11")

        if st.button("📋 ADICIONAR EVIDÊNCIA", key="sherlock12"):
            if descricao_evid.strip():
                if 'evidencias_lista' not in st.session_state:
                    st.session_state.evidencias_lista = []
                st.session_state.evidencias_lista.append({
                    'tipo': tipo_evid, 'descricao': descricao_evid, 'relevancia': relevancia_evid,
                    'notas': notas_evid, 'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                })
                st.session_state.evidencias_cadastradas_count += 1
                st.success("✅ Evidência cadastrada!")
                st.rerun()
            else:
                st.warning("Descreva a evidência.")

        if st.session_state.get('evidencias_lista'):
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown(f"### 📂 Evidências Cadastradas ({len(st.session_state.evidencias_lista)})")
            for i, ev in enumerate(reversed(st.session_state.evidencias_lista)):
                idx_real = len(st.session_state.evidencias_lista) - 1 - i
                cor_rel = "badge-vermelho" if ev.get('relevancia', 0)=="Alta" else ("badge-amarelo" if ev.get('relevancia', 0)=="Média" else "badge")
                with st.expander(f"{ev['tipo']} — {ev['descricao'][:50]} — {ev['data']}"):
                    st.markdown(f"<span class='{cor_rel}'>Relevância: {ev.get('relevancia', 0)}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Descrição:** {ev['descricao']}")
                    if ev.get('notas'):
                        st.markdown(f"**Notas:** {ev.get('notas', 0)}")
                    if st.button("🗑️ Remover", key=f"del_evid_{i}"):
                        st.session_state.evidencias_lista.pop(idx_real)
                        st.session_state.evidencias_cadastradas_count = max(0, st.session_state.evidencias_cadastradas_count - 1)
                        st.rerun()

            if st.button("🤖 ANALISAR TODAS AS EVIDÊNCIAS JUNTAS", key="sherlock13"):
                with st.spinner("Analisando o conjunto..."):
                    evid_txt = "\n".join([f"- [{e['tipo']}] {e['descricao']} (relevância: {e['relevancia']})" for e in st.session_state.evidencias_lista])
                    prompt = (
                        f"Analise este conjunto de evidências de forma integrada.\n"
                        f"Evidências:\n{evid_txt}\n\n"
                        f"FORMATO:\n\n"
                        f"📋 ANÁLISE DO CONJUNTO DE EVIDÊNCIAS\n\n"
                        f"🔗 CONEXÕES ENTRE AS EVIDÊNCIAS:\n[como elas se relacionam]\n\n"
                        f"🧩 O QUE O CONJUNTO SUGERE:\n[hipóteses que emergem ao olhar tudo junto]\n\n"
                        f"⚠️ LACUNAS:\n[que tipo de evidência ainda falta]\n\n"
                        f"🎯 EVIDÊNCIA MAIS DECISIVA:\n[qual delas mais pesa, e por quê]"
                    )
                    res = sherlock_ia(prompt)
                    st.session_state['evid_analise_temp'] = res

            if st.session_state.get('evid_analise_temp'):
                st.markdown(f"<div class='card-dark'>{st.session_state['evid_analise_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # LINHA DO TEMPO INTELIGENTE
        # ========================

    with _tab_Timeline:
        st.header("⏳ Linha do Tempo Inteligente")

        eventos_time = st.text_area("📝 Liste os eventos que você conhece (com horários/datas se possível):", height=180,
            placeholder="ex: 14h - mensagem enviada\n15h30 - chegou em casa\n16h - notou o problema\n...", key="sherlock13_d2")

        if st.button("⏳ RECONSTRUIR LINHA DO TEMPO", key="sherlock14_d2"):
            if eventos_time.strip():
                with st.spinner("Reconstruindo..."):
                    prompt = (
                        f"Reconstrua e analise esta linha do tempo.\n"
                        f"Eventos: {eventos_time}\n\n"
                        f"FORMATO:\n\n"
                        f"⏳ LINHA DO TEMPO RECONSTRUÍDA\n\n"
                        f"📅 SEQUÊNCIA ORDENADA:\n[eventos em ordem cronológica clara]\n\n"
                        f"⏱️ INTERVALOS DE TEMPO:\n[tempo entre eventos relevantes]\n\n"
                        f"⚠️ POSSÍVEIS LACUNAS:\n[períodos sem informação que merecem atenção]\n\n"
                        f"🎭 CONTRADIÇÕES CRONOLÓGICAS:\n[se houver algo que não bate na sequência temporal]\n\n"
                        f"🎯 PONTO MAIS CRÍTICO DA LINHA DO TEMPO:\n[o momento que merece mais investigação]"
                    )
                    res = sherlock_ia(prompt)
                    salvar_caso("Timeline", "Linha do tempo", res)
                    st.session_state['time_temp'] = res
            else:
                st.warning("Liste os eventos.")

        if st.session_state.get('time_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['time_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['time_temp'], file_name="linha_do_tempo.txt", mime="text/plain", key="sherlock15_d2")

        # ========================
        # DETECTOR DE CONTRADIÇÕES
        # ========================

    with _tab_Simulador:
        st.header("🎯 Simulador de Investigação")
        st.markdown("Casos fictícios para você resolver.")

        col1, col2 = st.columns(2)
        with col1:
            categoria_sim = st.selectbox("Categoria:", ["🏠 Mistérios domésticos","💰 Fraudes","🏢 Empresas","🔐 Segurança","🧩 Mistérios clássicos"], key="sherlock49")
        with col2:
            dificuldade_sim = st.selectbox("Dificuldade:", ["Fácil","Médio","Difícil","Muito difícil"], key="sherlock50")

        if st.button("🎯 GERAR CASO", key="sherlock51"):
            with st.spinner("Criando o caso..."):
                prompt = (
                    f"Crie um caso investigativo FICTÍCIO para o usuário resolver.\n"
                    f"Categoria: {categoria_sim}. Dificuldade: {dificuldade_sim}\n\n"
                    f"FORMATO:\n\n"
                    f"🎯 CASO: [NOME DRAMÁTICO DO CASO]\n"
                    f"Categoria: {categoria_sim} | Dificuldade: {dificuldade_sim}\n\n"
                    f"📖 SITUAÇÃO:\n[contexto do mistério, envolvente e bem narrado]\n\n"
                    f"🔍 PISTAS DISPONÍVEIS:\n[3-6 pistas, com nível de detalhe proporcional à dificuldade]\n\n"
                    f"👥 PERSONAGENS ENVOLVIDOS:\n[breve descrição de cada um]\n\n"
                    f"❓ A PERGUNTA QUE VOCÊ PRECISA RESPONDER:\n[o que o jogador precisa descobrir]\n\n"
                    f"🔒 [NÃO REVELE A SOLUÇÃO AINDA — isso vem só se o usuário pedir a resposta depois]"
                )
                res = sherlock_ia(prompt)
                st.session_state['sim_caso_temp'] = res
                st.session_state['sim_caso_categoria'] = categoria_sim
                st.session_state['sim_solucao_revelada'] = False

        if st.session_state.get('sim_caso_temp'):
            st.markdown(f"<div class='dossie-box'>{st.session_state['sim_caso_temp']}</div>", unsafe_allow_html=True)

            if not st.session_state.get('sim_solucao_revelada'):
                sua_solucao = st.text_area("🕵️ Sua solução para o caso:", height=100, key="input_solucao_sim")
                if st.button("🔓 VER A SOLUÇÃO E COMPARAR", key="sherlock52"):
                    with st.spinner("Revelando a solução..."):
                        prompt_solucao = (
                            f"Aqui está o caso que você criou antes:\n{st.session_state['sim_caso_temp']}\n\n"
                            f"O usuário propôs esta solução: {sua_solucao or 'não informou uma solução'}\n\n"
                            f"Revele a solução completa do caso e compare com a tentativa do usuário.\n\n"
                            f"FORMATO:\n\n"
                            f"🔓 SOLUÇÃO DO CASO\n\n"
                            f"✅ O QUE REALMENTE ACONTECEU:\n[solução completa e lógica]\n\n"
                            f"🧩 RACIOCÍNIO CORRETO:\n[como as pistas levavam à solução]\n\n"
                            f"📊 SUA TENTATIVA:\n[comentário sobre a proposta do usuário, reconhecendo acertos]\n\n"
                            f"🎯 NOTA: [X]/10\n[avaliação do raciocínio do usuário]"
                        )
                        res_sol = sherlock_ia(prompt_solucao)
                        st.session_state['sim_solucao_temp'] = res_sol
                        st.session_state['sim_solucao_revelada'] = True
                        st.session_state.casos_resolvidos_count += 1
                        st.rerun()

            if st.session_state.get('sim_solucao_temp'):
                st.markdown(f"<div class='card-gold'>{st.session_state['sim_solucao_temp']}</div>", unsafe_allow_html=True)
                if st.button("🔄 Novo caso", key="sherlock53"):
                    for k in ['sim_caso_temp','sim_solucao_temp','sim_solucao_revelada','sim_caso_categoria']:
                        st.session_state.pop(k, None)
                    st.rerun()

        # ========================
        # DIÁRIO DO INVESTIGADOR
        # ========================

    with _tab_Diario:
        st.header("📖 Diário do Investigador")

        col1, col2 = st.columns(2)
        with col1:
            nome_caso_diario = st.text_input("🔍 Nome do caso:", placeholder="ex: O Mistério do Objeto Desaparecido", key="sherlock54")
            status_diario = st.selectbox("Status:", ["Em andamento","Resolvido","Arquivado","Aguardando mais informações"], key="sherlock55")
        with col2:
            hipotese_diario = st.text_input("🧩 Hipótese principal atual:", placeholder="ex: Alguém pegou por engano...", key="sherlock56")

        conclusao_diario = st.text_area("📝 Notas/conclusões:", height=120, placeholder="ex: Conversei com todos, a evidência mais forte aponta para...", key="sherlock57")

        if st.button("📖 SALVAR NO DIÁRIO", key="sherlock58"):
            if nome_caso_diario.strip():
                st.session_state.diario_investigador.append({
                    'data': datetime.now().strftime('%d/%m/%Y'),
                    'caso': nome_caso_diario, 'status': status_diario,
                    'hipotese': hipotese_diario, 'conclusao': conclusao_diario,
                })
                if status_diario == "Resolvido":
                    st.session_state.casos_resolvidos_count += 1
                st.success("✅ Registrado no diário!")
                st.rerun()
            else:
                st.warning("Nomeie o caso.")

        if st.session_state.diario_investigador:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown(f"### 📚 Seus Casos ({len(st.session_state.diario_investigador)})")
            for i, caso in enumerate(reversed(st.session_state.diario_investigador)):
                idx_real = len(st.session_state.diario_investigador) - 1 - i
                cor_status = "badge-verde" if caso['status']=="Resolvido" else ("badge-amarelo" if caso['status']=="Em andamento" else "badge")
                with st.expander(f"🔍 {caso['caso']} — {caso['data']}"):
                    st.markdown(f"<span class='{cor_status}'>{caso['status']}</span>", unsafe_allow_html=True)
                    if caso.get('hipotese'): st.markdown(f"**Hipótese:** {caso['hipotese']}")
                    if caso.get('conclusao'): st.markdown(f"**Notas:** {caso['conclusao']}")
                    if st.button("🗑️ Remover", key=f"del_diario_{i}"):
                        st.session_state.diario_investigador.pop(idx_real)
                        st.rerun()

        # ========================
        # PAINEL INVESTIGATIVO
        # ========================

    with _tab_Painel:
        st.header("📈 Painel Investigativo")

        total_casos = len(st.session_state.historico_casos)
        modulos_count = {}
        for c in st.session_state.historico_casos:
            modulos_count[c['modulo']] = modulos_count.get(c['modulo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.casos_resolvidos_count}</div><div>Casos resolvidos</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.evidencias_cadastradas_count}</div><div>Evidências cadastradas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_casos}</div><div>Análises totais</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.diario_investigador)}</div><div>Casos no diário</div></div>", unsafe_allow_html=True)

        if modulos_count:
            st.markdown("### 📊 Áreas onde você mais investigou")
            ranking = sorted(modulos_count.items(), key=lambda x: x[1], reverse=True)
            for i, (modulo, count) in enumerate(ranking[:8]):
                pct = round(count / total_casos * 100) if total_casos else 0
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.85em;font-weight:600;"><span>{i+1}. {modulo}</span><span>{count}x</span></div>
                    <div style="background:#E2E8F0;border-radius:999px;height:10px;overflow:hidden;"><div style="height:100%;border-radius:999px;background:#0F172A;width:{pct}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)

        # ========================
        # ACADEMIA SHERLOCK
        # ========================

    with _tab_Academia:
        st.header("🎓 Academia Sherlock")
        st.markdown("30 aulas de aprofundamento real — observação, dedução e método investigativo aplicado.")

        aulas = [
            "Aula 1 — O Poder da Observação", "Aula 2 — A Arte da Dedução", "Aula 3 — Fato x Opinião x Evidência",
            "Aula 4 — Como Pensam os Grandes Investigadores", "Aula 5 — Psicologia do Comportamento",
            "Aula 6 — Como Fazer Perguntas Inteligentes", "Aula 7 — Montando o Quebra-Cabeça",
            "Aula 8 — Encontrando Padrões", "Aula 9 — Os Maiores Erros da Mente", "Aula 10 — Organização Profissional",
            "Aula 11 — Memória de Investigador", "Aula 12 — Atenção aos Pequenos Detalhes",
            "Aula 13 — Como Observar Fotografias", "Aula 14 — Investigação no Dia a Dia",
            "Aula 15 — Investigação Digital", "Aula 16 — Introdução à Ciência Forense",
            "Aula 17 — Grandes Casos da História", "Aula 18 — Desafios de Lógica", "Aula 19 — Caça aos Detalhes",
            "Aula 20 — Método Sherlock Holmes",
        ]
        aulas += [
            "Aula 21 — Linguagem Corporal e Microexpressões (com cautela)", "Aula 22 — Investigação de Ausências (o que NÃO está lá)",
            "Aula 23 — Raciocínio Probabilístico no Dia a Dia", "Aula 24 — Como Documentar uma Investigação",
            "Aula 25 — Entrevistas e Como Conduzir Conversas Investigativas", "Aula 26 — Cadeia de Custódia e Preservação de Evidências",
            "Aula 27 — Investigação Colaborativa (trabalhando em equipe)", "Aula 28 — Ética na Investigação",
            "Aula 29 — Quando Parar de Investigar", "Aula 30 — Construindo seu Próprio Método",
        ]

        col_aula, col_nivel = st.columns([3, 1])
        with col_aula:
            aula_escolhida = st.selectbox("Escolha a aula:", aulas, key="select_aula_academia")
        with col_nivel:
            profundidade_aula = st.selectbox("Profundidade:", ["Padrão", "Aprofundada"], key="select_profundidade_aula")

        if st.button("🎓 INICIAR AULA", key="sherlock59"):
            with st.spinner("Preparando uma aula de verdade, com profundidade..."):
                nivel_instrucao = (
                    "Esta deve ser uma aula EXTENSA e densa, no nível de um curso universitário de elite ou de um seminário "
                    "avançado de investigação — não um resumo de blog."
                    if profundidade_aula == "Aprofundada" else
                    "Esta deve ser uma aula completa e rica, mas objetiva."
                )
                prompt = (
                    f"Você está escrevendo uma aula para a Academia Sherlock — um curso de altíssimo nível sobre raciocínio "
                    f"investigativo, no espírito do método de observação e dedução de Sherlock Holmes, mas aplicado a contextos "
                    f"reais e modernos. {nivel_instrucao}\n\n"
                    f"Tema da aula: {aula_escolhida}\n\n"
                    f"EXIGÊNCIAS DE QUALIDADE — leia com atenção antes de escrever:\n"
                    f"- PROIBIDO ser superficial, genérico ou usar frases de efeito vazias. Cada afirmação deve ser sustentada "
                    f"por um exemplo concreto, um mecanismo explicado, ou um caso ilustrativo.\n"
                    f"- Use pelo menos 2 exemplos NARRADOS EM DETALHE (não apenas citados de passagem) — podem ser cenários "
                    f"fictícios elaborados, casos históricos genéricos (sem inventar fatos verificáveis específicos que você não "
                    f"tenha certeza), ou situações do cotidiano levadas a um nível de análise que a maioria das pessoas não faz.\n"
                    f"- Demonstre o RACIOCÍNIO PASSO A PASSO, não apenas a conclusão. Mostre o 'como se pensa', não só o 'o que pensar'.\n"
                    f"- Inclua nuances, contra-exemplos e limites do método ensinado — uma aula de elite reconhece onde a técnica falha.\n"
                    f"- O exercício final deve ser desafiador, específico e ter um gabarito comentado explicando o raciocínio "
                    f"correto, não apenas a resposta.\n\n"
                    f"FORMATO OBRIGATÓRIO:\n\n"
                    f"🎓 {aula_escolhida.upper()}\n\n"
                    f"📖 ABERTURA — POR QUE ISSO IMPORTA:\n"
                    f"[3-5 linhas que conectem o tema a uma situação real e mostrem por que dominar isso muda a qualidade do "
                    f"raciocínio de quem está aprendendo. Evite frases motivacionais genéricas — seja específico sobre a vantagem prática.]\n\n"
                    f"💡 OS CONCEITOS FUNDAMENTAIS:\n"
                    f"[3-5 conceitos centrais, cada um com: definição precisa, por que costuma ser mal compreendido ou ignorado, "
                    f"e um exemplo curto que fixe a ideia]\n\n"
                    f"🔍 ESTUDO DE CASO 1 — NARRATIVA COMPLETA:\n"
                    f"[Narre uma situação (fictícia ou genérica, bem construída) onde o conceito da aula é aplicado do início ao fim. "
                    f"Mostre as observações feitas, o raciocínio encadeado, e a conclusão. Pelo menos 8-10 linhas de narrativa real, "
                    f"não um resumo de 2 linhas.]\n\n"
                    f"🔍 ESTUDO DE CASO 2 — UM ÂNGULO DIFERENTE:\n"
                    f"[Um segundo exemplo que mostre uma faceta diferente do mesmo conceito — outro contexto, outra complexidade, "
                    f"ou um caso em que a aplicação ingênua do método levaria a erro, e como corrigir isso]\n\n"
                    f"⚙️ O MÉTODO PASSO A PASSO:\n"
                    f"[Decomponha a técnica em etapas concretas e replicáveis — numeradas, específicas, sem vagueza. "
                    f"Esta é a parte 'manual de instruções' da aula]\n\n"
                    f"⚠️ ARMADILHAS E LIMITES DO MÉTODO:\n"
                    f"[Onde essa técnica costuma ser usada mal, que erros ela não resolve, e quando confiar demais nela é perigoso. "
                    f"Uma aula de elite é honesta sobre os limites do que está ensinando]\n\n"
                    f"🧠 CONEXÃO COM OUTRAS AULAS/CONCEITOS:\n"
                    f"[Como esse tema se conecta com outros princípios investigativos — mostre que o conhecimento é uma rede, não peças isoladas]\n\n"
                    f"🏋️ EXERCÍCIO PRÁTICO DESAFIADOR:\n"
                    f"[Um exercício elaborado e específico — um mini-caso, um cenário com dados reais para analisar, ou um "
                    f"desafio de observação. Deve exigir aplicação real do conceito, não só recordação]\n\n"
                    f"✅ GABARITO COMENTADO:\n"
                    f"[A resposta esperada do exercício, COM o raciocínio explicado passo a passo — não apenas 'a resposta é X', "
                    f"mas 'a resposta é X porque, ao observar Y, deduzimos Z, e isso elimina a hipótese W']\n\n"
                    f"📚 SÍNTESE MAGISTRAL:\n"
                    f"[2-4 linhas que cristalizem a essência da aula em uma ideia memorável e aplicável — a frase que o aluno "
                    f"deveria lembrar meses depois]"
                )
                res = sherlock_ia(prompt, "Você está escrevendo a melhor aula possível sobre este tema. Imagine que está escrevendo para uma pessoa inteligente e exigente que vai notar e se decepcionar com qualquer superficialidade, clichê vazio, ou exemplo fraco. Densidade e precisão acima de tudo — mas sem perder a clareza didática.")
                salvar_caso("Academia", aula_escolhida, res)
                st.session_state['aula_temp'] = res

        if st.session_state.get('aula_temp'):
            try:
                st.markdown(f"<div class='card'>{st.session_state['aula_temp']}</div>", unsafe_allow_html=True)
            except:
                st.markdown(st.session_state['aula_temp'])
            st.download_button("📋 Baixar aula (.txt)", data=st.session_state['aula_temp'], file_name="aula_academia.txt", mime="text/plain", key="sherlock60")

        # ========================
        # DESAFIO SHERLOCK
        # ========================

    with _tab_Desafio:
        st.header("🏆 Desafio Sherlock")
        nivel_atual = st.session_state.desafio_nivel_atual
        st.markdown(f"Pontuação: **{st.session_state.desafio_pontuacao} pontos** | Nível atual: <span class='{CLASSES_NIVEL.get(nivel_atual)}'>{nivel_atual}</span>", unsafe_allow_html=True)

        nivel_desafio = st.selectbox("Escolha o nível do desafio:", NIVEIS_DESAFIO, key="select_nivel_desafio")

        if st.button("🏆 GERAR DESAFIO", key="sherlock61"):
            with st.spinner("Criando o desafio..."):
                prompt = (
                    f"Crie um mini-desafio de lógica/investigação no nível: {nivel_desafio}\n\n"
                    f"FORMATO:\n\n"
                    f"🏆 DESAFIO {nivel_desafio.upper()}\n\n"
                    f"📖 SITUAÇÃO:\n[um mini-mistério ou quebra-cabeça lógico, complexidade adequada ao nível]\n\n"
                    f"❓ O QUE VOCÊ PRECISA DESCOBRIR:\n[a pergunta do desafio]\n\n"
                    f"💡 DICA (opcional, oculta até pedir):\n[uma dica que ajuda sem entregar a resposta]\n\n"
                    f"✅ RESPOSTA: [a solução, mas marque claramente como RESPOSTA para o app esconder até o usuário clicar]"
                )
                res = sherlock_ia(prompt)
                st.session_state['desafio_temp'] = res
                st.session_state['desafio_revelado'] = False
                st.session_state['desafio_nivel_jogado'] = nivel_desafio

        if st.session_state.get('desafio_temp'):
            partes_desafio = st.session_state['desafio_temp'].split('✅ RESPOSTA')
            st.markdown(f"<div class='dossie-box'>{partes_desafio[0]}</div>", unsafe_allow_html=True)

            if not st.session_state.get('desafio_revelado'):
                if st.button("👁️ VER RESPOSTA", key="sherlock62"):
                    st.session_state['desafio_revelado'] = True
                    st.rerun()
            else:
                st.markdown(f"<div class='card-gold'>✅ RESPOSTA{partes_desafio[1] if len(partes_desafio)>1 else ''}</div>", unsafe_allow_html=True)
                col_acertei, col_errei = st.columns(2)
                with col_acertei:
                    if st.button("✅ Acertei!", key="sherlock63"):
                        pontos = {"Iniciante":5,"Investigador":10,"Inspetor":15,"Mestre":20,"Sherlock":30}
                        nivel_jogado = st.session_state.get('desafio_nivel_jogado', nivel_desafio)
                        st.session_state.desafio_pontuacao += pontos.get(nivel_jogado, 10)
                        st.session_state.desafio_nivel_atual = nivel_jogado
                        st.session_state.casos_resolvidos_count += 1
                        st.success(f"🎉 +{pontos.get(nivel_jogado,10)} pontos!")
                with col_errei:
                    if st.button("❌ Errei", key="sherlock64"):
                        st.info("Sem problema, a prática leva à perfeição. Próximo desafio!")

        # ========================
        # SHERLOCK 24 HORAS
        # ========================

    with _tab_Sherlock24:
        st.header("🤖 Sherlock 24 Horas")
        st.markdown("Converse livremente sobre qualquer investigação.")

        if 'chat_sherlock' not in st.session_state:
            st.session_state.chat_sherlock = []
        if 'sherlock_key' not in st.session_state:
            st.session_state.sherlock_key = 0

        if st.session_state.chat_sherlock:
            for msg in st.session_state.chat_sherlock:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#F1F5F9;border:1px solid #334155;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-dark' style='margin:8px 0;'><b>🕵️ Sherlock:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#F1F5F9;border:1px dashed #334155;border-radius:12px;padding:16px;text-align:center;">
            🤖 <strong>Pergunte qualquer coisa!</strong> Ex: "Como eu organizaria uma investigação sobre X?",
            "Quais perguntas eu deveria fazer nessa situação?"
            </div>""", unsafe_allow_html=True)

        pergunta_sherlock = st.text_input("Sua pergunta:", key=f"sherlock_input_{st.session_state.sherlock_key}", placeholder="Pergunte qualquer coisa sobre investigação...")

        col_env, col_limpar = st.columns([3, 1])
        with col_env:
            if st.button("📤 PERGUNTAR", key="sherlock65"):
                if pergunta_sherlock.strip():
                    with st.spinner("Investigando..."):
                        resp = sherlock_ia(pergunta_sherlock, "Responda como um detetive consultor experiente, lógico e didático.")
                    st.session_state.chat_sherlock.append({"role": "user", "content": pergunta_sherlock})
                    st.session_state.chat_sherlock.append({"role": "assistant", "content": resp})
                    st.session_state.sherlock_key += 1
                    salvar_caso("Sherlock24", pergunta_sherlock[:60], resp)
                    st.rerun()
                else:
                    st.warning("Digite sua pergunta.")
        with col_limpar:
            if st.button("🗑️ Limpar", key="sherlock66"):
                st.session_state.chat_sherlock = []
                st.rerun()

        # ========================
        # SALA DE CASOS IMPOSSÍVEIS
        # ========================

    with _tab_CasosImpossiveis:
        st.header("💎 Sala de Casos Impossíveis")
        st.markdown("Mistérios complexos que se revelam por etapas. A IA é sua mentora — não entrega a resposta.")

        if 'dossie_etapa' not in st.session_state:
            st.session_state.dossie_etapa = 0

        if st.session_state.dossie_etapa == 0:
            dificuldade_dossie = st.selectbox("Nível de complexidade:", ["Inspetor","Mestre","Sherlock"], key="sherlock67")
            if st.button("💎 ABRIR NOVO DOSSIÊ", key="sherlock68"):
                with st.spinner("Montando o dossiê..."):
                    prompt = (
                        f"Crie um caso investigativo complexo e envolvente, nível {dificuldade_dossie}, "
                        f"para ser revelado em etapas (dossiê).\n\n"
                        f"FORMATO:\n\n"
                        f"💎 DOSSIÊ: [NOME DRAMÁTICO DO CASO]\n"
                        f"Nível: {dificuldade_dossie}\n\n"
                        f"📖 CONTEXTO INICIAL:\n[a situação inicial, intrigante]\n\n"
                        f"📸 ELEMENTOS DISPONÍVEIS NESTA ETAPA:\n[2-3 evidências/depoimentos iniciais]\n\n"
                        f"❓ SUA MISSÃO:\n[o que o investigador precisa descobrir]\n\n"
                        f"[NÃO REVELE MAIS NADA AINDA — isso é só a primeira etapa do dossiê]"
                    )
                    res = sherlock_ia(prompt)
                    st.session_state['dossie_conteudo'] = [res]
                    st.session_state['dossie_dificuldade'] = dificuldade_dossie
                    st.session_state.dossie_etapa = 1
                    st.rerun()
        else:
            for i, parte in enumerate(st.session_state.get('dossie_conteudo', [])):
                st.markdown(f"<div class='dossie-box'>{parte}</div>", unsafe_allow_html=True)

            st.markdown("#### 🧩 Sua análise / próxima pergunta para a mentora:")
            analise_dossie = st.text_area("Escreva sua hipótese atual ou pergunta:", height=100, key="input_analise_dossie")

            col_continuar, col_revelar = st.columns(2)
            with col_continuar:
                if st.button("➡️ DESBLOQUEAR PRÓXIMO ELEMENTO", key="sherlock69"):
                    if analise_dossie.strip():
                        with st.spinner("A mentora está analisando..."):
                            historico_dossie = "\n\n".join(st.session_state['dossie_conteudo'])
                            prompt = (
                                f"Você é a mentora de um caso investigativo em andamento (dossiê nível {st.session_state.get('dossie_dificuldade','Inspetor')}).\n"
                                f"Conteúdo já revelado:\n{historico_dossie}\n\n"
                                f"O investigador (usuário) disse: {analise_dossie}\n\n"
                                f"Responda como mentora: faça uma pergunta estratégica sobre o raciocínio dele, aponte SUTILMENTE "
                                f"se algo parece incompleto (sem entregar a resposta), e então revele UM novo elemento do dossiê "
                                f"(uma nova evidência, depoimento ou pista) que avança a investigação.\n\n"
                                f"FORMATO:\n\n"
                                f"🕵️ COMENTÁRIO DA MENTORA:\n[reação ao raciocínio do investigador — perguntas estratégicas, sem entregar a resposta]\n\n"
                                f"📂 NOVO ELEMENTO DESBLOQUEADO:\n[uma nova peça do dossiê — evidência, depoimento, documento]"
                            )
                            res = sherlock_ia(prompt)
                            st.session_state['dossie_conteudo'].append(res)
                            st.rerun()
                    else:
                        st.warning("Escreva sua hipótese ou pergunta antes de avançar.")
            with col_revelar:
                if st.button("🔓 REVELAR SOLUÇÃO COMPLETA", key="sherlock70"):
                    with st.spinner("Revelando a lógica completa..."):
                        historico_dossie = "\n\n".join(st.session_state['dossie_conteudo'])
                        prompt = (
                            f"Revele a solução completa deste caso investigativo, explicando toda a lógica.\n"
                            f"Conteúdo do dossiê até agora:\n{historico_dossie}\n\n"
                            f"FORMATO:\n\n"
                            f"🔓 SOLUÇÃO COMPLETA DO CASO\n\n"
                            f"✅ O QUE REALMENTE ACONTECEU:\n[a solução completa]\n\n"
                            f"🧩 LÓGICA UTILIZADA:\n[como cada pista levava à solução, passo a passo]\n\n"
                            f"🎯 A PISTA MAIS DECISIVA:\n[qual elemento foi crucial]\n\n"
                            f"🏆 PARABÉNS POR INVESTIGAR ATÉ O FIM!"
                        )
                        res_final = sherlock_ia(prompt)
                        st.session_state['dossie_solucao'] = res_final
                        st.session_state.casos_resolvidos_count += 1
                        st.rerun()

            if st.session_state.get('dossie_solucao'):
                st.markdown(f"<div class='card-gold'>{st.session_state['dossie_solucao']}</div>", unsafe_allow_html=True)
                if st.button("🔄 Abrir novo dossiê", key="sherlock71"):
                    for k in ['dossie_etapa','dossie_conteudo','dossie_dificuldade','dossie_solucao']:
                        st.session_state.pop(k, None)
                    st.rerun()

        # ========================
        # BIBLIOTECA
        # ========================

    with _tab_Biblioteca:
        st.header("📚 Biblioteca de Casos")

        if not st.session_state.casos_salvos:
            st.info("Biblioteca vazia. Gere análises nos módulos e salve as importantes aqui!")
        else:
            modulos_bib = list(set(c['modulo'] for c in st.session_state.casos_salvos))
            filtro = st.selectbox("Filtrar por módulo:", ["Todos"] + modulos_bib, key="select_filtro_bib")
            consultas_f = [c for c in st.session_state.casos_salvos if filtro == "Todos" or c['modulo'] == filtro]

            st.markdown(f"**{len(consultas_f)} análise(s) encontrada(s)**")
            for i, item in enumerate(reversed(consultas_f)):
                idx_real = len(st.session_state.casos_salvos) - 1 - i
                with st.expander(f"[{item.get('modulo', '')}] {item.get('tema', '')[:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item.get('modulo', '').lower()}.txt", mime="text/plain", key=f"dl_bib_{i}")
                    with col_del:
                        if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                            st.session_state.casos_salvos.pop(idx_real)
                            st.rerun()

        if st.session_state.historico_casos:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            historico_txt = "\n\n".join(f"[{c['data']}] {c['modulo']} — {c['tema']}\n{c['conteudo']}\n{'─'*40}" for c in st.session_state.historico_casos)
            st.download_button("⬇️ Exportar todo o histórico (.txt)", data=historico_txt, file_name="historico_sherlock.txt", mime="text/plain", key="sherlock72")
            if st.button("🗑️ Limpar Todo o Histórico", key="sherlock73"):
                st.session_state.historico_casos = []
                st.rerun()

        # --- RODAPÉ ---
        st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Sherlock IA — Consultor de Investigação Lógica com IA · Quiz Com Prêmios"
        "</div>", unsafe_allow_html=True
        )


        # --- RODAPÉ ---
        st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "</div>", unsafe_allow_html=True
        )

    with _tab_Forense:
        st.header("🧪 Laboratório Forense (Educativo)")
        st.markdown(DISCLAIMER_FORENSE, unsafe_allow_html=True)

        tema_forense = st.selectbox("Tema:", [
            "Impressões digitais", "DNA forense", "Análise de pegadas", "Vestígios e indícios",
            "Cadeia de custódia", "Balística", "Documentoscopia", "Perícia digital",
        ], key="sherlock1_d2")

        if st.button("🧪 APRENDER", key="sherlock44"):
            with st.spinner("Preparando conteúdo..."):
                prompt = (
                    f"Explique de forma educativa: {tema_forense}\n\n"
                    f"FORMATO:\n\n"
                    f"🧪 {tema_forense.upper()}\n\n"
                    f"📖 O QUE É E COMO FUNCIONA:\n[explicação científica acessível]\n\n"
                    f"🔬 PRINCÍPIOS CIENTÍFICOS ENVOLVIDOS:\n[a base científica/lógica do método]\n\n"
                    f"📋 COMO É USADO EM INVESTIGAÇÕES REAIS:\n[contexto de uso pela perícia oficial]\n\n"
                    f"💡 CURIOSIDADE HISTÓRICA:\n[1 fato interessante sobre a evolução dessa técnica]"
                )
                res = sherlock_ia(prompt, "Mantenha o conteúdo estritamente educativo e conceitual — nunca forneça instruções de como evitar ou burlar essa técnica forense.")
                salvar_caso("Forense", tema_forense, res)
                st.session_state['for_temp'] = res

        if st.session_state.get('for_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['for_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['for_temp'], file_name="forense.txt", mime="text/plain", key="sherlock45")

        # ========================
        # CASOS HISTÓRICOS
        # ========================

    with _tab_Casos:
        st.header("📚 Casos Históricos")

        caso_hist = st.text_input("🔍 Caso de interesse (ou deixe vazio para sugestão):", placeholder="ex: um caso famoso de fraude, um mistério clássico resolvido por perícia...", key="sherlock46")

        if st.button("📚 EXPLORAR CASO", key="sherlock47"):
            with st.spinner("Buscando o caso..."):
                topico_caso = caso_hist if caso_hist.strip() else "um caso histórico famoso de investigação bem documentado"
                prompt = (
                    f"Apresente um caso investigativo histórico relevante relacionado a: {topico_caso}\n\n"
                    f"FORMATO:\n\n"
                    f"📚 CASO: [NOME DO CASO]\n\n"
                    f"📖 CONTEXTO:\n[o que aconteceu]\n\n"
                    f"🔍 COMO FOI INVESTIGADO:\n[método usado pelos investigadores]\n\n"
                    f"🎯 EVIDÊNCIAS DECISIVAS:\n[o que resolveu o caso]\n\n"
                    f"⚠️ ERROS COMETIDOS NA INVESTIGAÇÃO:\n[se houver, o que poderia ter sido feito melhor]\n\n"
                    f"💡 LIÇÃO PARA INVESTIGADORES:\n[o que esse caso ensina]\n\n"
                    f"⚠️ NOTA: se não tiver certeza de detalhes específicos e verificáveis sobre um caso real, "
                    f"diga isso claramente em vez de inventar fatos."
                )
                res = sherlock_ia(prompt)
                salvar_caso("Casos", topico_caso, res)
                st.session_state['caso_hist_temp'] = res

        if st.session_state.get('caso_hist_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['caso_hist_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['caso_hist_temp'], file_name="caso_historico.txt", mime="text/plain", key="sherlock48")

        # ========================
        # SIMULADOR DE INVESTIGAÇÃO
        # ========================

    with _tab_Ferramentas:
        st.header("🛠️ Ferramentas Avançadas")
        st.markdown("*Ferramentas especializadas de investigação criminal e análise.*")
        (_sContradicoes, _sPerfil, _sConversas, _sImagens, _sDomestica, _sDigital, _sFraudes, _sPadroes, _sProbabilidades, _sPerguntas, _sCritico, _sMetodo) = st.tabs(['❌ Contradições', '👤 Perfil', '💬 Conversas', '🖼️ Imagens', '🏠 Crimes Dom.', '💻 Crimes Digitais', '💸 Fraudes', '🔗 Padrões', '📊 Probabilidades', '❓ Perguntas', '🧠 Pens. Crítico', '🔬 Método'])

        with _sContradicoes:
            st.header("🎭 Detector de Contradições")
            st.markdown("Cole relatos, mensagens ou depoimentos para identificar inconsistências.")

            relatos_contra = st.text_area("📝 Cole os relatos/depoimentos (identifique quem disse o quê):", height=200,
                placeholder="ex: Pessoa A disse: 'Eu não estava lá às 14h'. Mais tarde, Pessoa A disse: 'Cheguei por volta de 14h e já tinha gente lá'...", key="sherlock12_d2")

            if st.button("🎭 DETECTAR CONTRADIÇÕES", key="sherlock16_d2"):
                if relatos_contra.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise estes relatos identificando contradições e inconsistências.\n"
                            f"Relatos: {relatos_contra}\n\n"
                            f"FORMATO:\n\n"
                            f"🎭 ANÁLISE DE CONTRADIÇÕES\n\n"
                            f"🔄 MUDANÇAS DE VERSÃO:\n[onde a mesma pessoa disse coisas diferentes]\n\n"
                            f"⚠️ CONTRADIÇÕES ENTRE RELATOS:\n[onde diferentes pessoas se contradizem]\n\n"
                            f"❓ INFORMAÇÕES CONFLITANTES:\n[dados que não se encaixam]\n\n"
                            f"❓ PERGUNTAS AINDA NÃO RESPONDIDAS:\n[o que precisa ser esclarecido]\n\n"
                            f"🎯 CONTRADIÇÃO MAIS SIGNIFICATIVA:\n[qual merece mais atenção, e por quê]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Contradicoes", relatos_contra[:60], res)
                        st.session_state['contra_temp'] = res
                else:
                    st.warning("Cole os relatos.")

            if st.session_state.get('contra_temp'):
                st.markdown(f"<div class='card-red'>{st.session_state['contra_temp']}</div>", unsafe_allow_html=True)
                st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['contra_temp'], file_name="contradicoes.txt", mime="text/plain", key="sherlock17")

            # ========================
            # PERFIL COMPORTAMENTAL
            # ========================

        with _sPerfil:
            st.header("👤 Perfil Comportamental")
            st.markdown(DISCLAIMER_COMPORTAMENTAL, unsafe_allow_html=True)

            comportamento_perfil = st.text_area("📝 Descreva os comportamentos observados:", height=150,
                placeholder="ex: A pessoa começou a chegar mais tarde no trabalho, ficou mais quieta nas reuniões, e parou de almoçar com a equipe...", key="sherlock11_d2")

            if st.button("👤 ANALISAR PADRÕES", key="sherlock18"):
                if comportamento_perfil.strip():
                    with st.spinner("Analisando padrões..."):
                        prompt = (
                            f"Analise estes comportamentos descritos, gerando hipóteses (nunca diagnósticos).\n"
                            f"Comportamentos: {comportamento_perfil}\n\n"
                            f"FORMATO:\n\n"
                            f"👤 ANÁLISE DE PADRÕES COMPORTAMENTAIS\n\n"
                            f"🔄 MUDANÇAS IDENTIFICADAS:\n[o que mudou, com base no relato]\n\n"
                            f"💭 POSSÍVEIS MOTIVAÇÕES (hipóteses, não certezas):\n[3-4 explicações possíveis, incluindo motivos benignos e neutros]\n\n"
                            f"📊 PADRÕES E HÁBITOS:\n[o que parece ser recorrente]\n\n"
                            f"❤️ FATORES EMOCIONAIS POSSÍVEIS:\n[hipóteses sobre estado emocional, com cautela]\n\n"
                            f"❓ O QUE AINDA NÃO SE SABE:\n[informação que falta para entender melhor]\n\n"
                            f"💬 SUGESTÃO:\n[1 frase recomendando, quando aplicável, conversar diretamente com a pessoa em vez de apenas inferir]"
                        )
                        res = sherlock_ia(prompt, "Gere hipóteses variadas, incluindo explicações neutras e benignas — não foque só em explicações negativas ou suspeitas.")
                        salvar_caso("Perfil", comportamento_perfil[:60], res)
                        st.session_state['perfil_temp'] = res
                else:
                    st.warning("Descreva os comportamentos.")

            if st.session_state.get('perfil_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['perfil_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['perfil_temp'], file_name="perfil_comportamental.txt", mime="text/plain", key="sherlock19")

            # ========================
            # ANÁLISE DE CONVERSAS
            # ========================

        with _sConversas:
            st.header("💬 Análise de Conversas")
            st.markdown(DISCLAIMER_COMPORTAMENTAL, unsafe_allow_html=True)

            conversa_analise = st.text_area("📝 Cole a conversa que você quer analisar:", height=200,
                placeholder="Cole aqui a conversa, identificando quem disse cada parte...", key="sherlock10_d2")

            if st.button("💬 ANALISAR CONVERSA", key="sherlock20"):
                if conversa_analise.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise esta conversa.\n"
                            f"Conversa: {conversa_analise}\n\n"
                            f"FORMATO:\n\n"
                            f"💬 ANÁLISE DA CONVERSA\n\n"
                            f"🎭 MUDANÇAS DE TOM:\n[onde o tom muda e o que isso pode sugerir]\n\n"
                            f"⚠️ POSSÍVEIS CONTRADIÇÕES:\n[inconsistências no que foi dito]\n\n"
                            f"🙈 ASSUNTOS EVITADOS:\n[temas que parecem ser desviados ou evitados]\n\n"
                            f"🔄 COMUNICAÇÃO INDIRETA:\n[onde algo parece estar sendo dito sem ser dito diretamente]\n\n"
                            f"❓ PERGUNTAS SEM RESPOSTA:\n[o que foi perguntado mas não respondido claramente]\n\n"
                            f"✅ COERÊNCIA GERAL: [Alta/Média/Baixa]\n[avaliação geral de quão consistente é a conversa]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Conversas", conversa_analise[:60], res)
                        st.session_state['conv_temp'] = res
                else:
                    st.warning("Cole a conversa.")

            if st.session_state.get('conv_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['conv_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['conv_temp'], file_name="analise_conversa.txt", mime="text/plain", key="sherlock21")

            # ========================
            # ANÁLISE DE IMAGENS (DESCRITIVA)
            # ========================

        with _sImagens:
            st.header("📸 Análise de Imagens")
            st.info("📝 Este app trabalha por descrição em texto — descreva a cena com o máximo de detalhes possível.")

            descricao_imagem = st.text_area("📝 Descreva detalhadamente o que você vê na imagem/cena:", height=180,
                placeholder="ex: Sala com a janela aberta, uma cadeira fora do lugar normal, papéis no chão perto da mesa, luz apagada...", key="sherlock9_d2")

            if st.button("📸 ANALISAR DESCRIÇÃO", key="sherlock22"):
                if descricao_imagem.strip():
                    with st.spinner("Analisando os detalhes..."):
                        prompt = (
                            f"Analise esta descrição de cena/imagem com olhar investigativo.\n"
                            f"Descrição: {descricao_imagem}\n\n"
                            f"FORMATO:\n\n"
                            f"📸 ANÁLISE DA CENA DESCRITA\n\n"
                            f"🔍 OBJETOS RELEVANTES:\n[itens mencionados que podem ter importância]\n\n"
                            f"🏠 AMBIENTE E ORGANIZAÇÃO:\n[o que o estado do ambiente sugere]\n\n"
                            f"👣 POSSÍVEIS VESTÍGIOS:\n[sinais que indicam o que pode ter acontecido]\n\n"
                            f"⚠️ ELEMENTOS QUE CHAMAM ATENÇÃO:\n[o que parece fora do normal ou inconsistente]\n\n"
                            f"👀 DETALHES QUE PODEM TER SIDO IGNORADOS:\n[perguntas sobre o que mais observar]\n\n"
                            f"🧩 O QUE ESSA CENA PODE SUGERIR:\n[hipóteses, sempre como possibilidades]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Imagens", descricao_imagem[:60], res)
                        st.session_state['img_temp'] = res
                else:
                    st.warning("Descreva a cena.")

            if st.session_state.get('img_temp'):
                st.markdown(f"<div class='card'>{st.session_state['img_temp']}</div>", unsafe_allow_html=True)
                st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['img_temp'], file_name="analise_imagem.txt", mime="text/plain", key="sherlock23")

            # ========================
            # INVESTIGAÇÃO DOMÉSTICA
            # ========================

        with _sDomestica:
            st.header("🏠 Investigação Doméstica")

            tipo_dom = st.selectbox("Tipo de problema:", ["Vazamento de água","Ruído estranho","Cheiro incomum","Infiltração","Defeito elétrico","Outro"], key="sherlock24")
            descricao_dom = st.text_area("📝 Descreva o problema com detalhes:", height=150,
                placeholder="ex: Aparece uma mancha de umidade no canto do teto da sala, principalmente depois de chover...", key="sherlock8_d2")

            if st.button("🏠 INVESTIGAR PROBLEMA", key="sherlock25"):
                if descricao_dom.strip():
                    with st.spinner("Investigando..."):
                        prompt = (
                            f"Investigue este problema doméstico.\n"
                            f"Tipo: {tipo_dom}. Descrição: {descricao_dom}\n\n"
                            f"FORMATO:\n\n"
                            f"🏠 INVESTIGAÇÃO — {tipo_dom.upper()}\n\n"
                            f"🔍 POSSÍVEIS CAUSAS (da mais para a menos provável):\n[liste com lógica]\n\n"
                            f"🧪 TESTES QUE VOCÊ PODE FAZER:\n[ações simples para isolar a causa]\n\n"
                            f"⚠️ SINAIS DE URGÊNCIA:\n[quando isso indica um problema que precisa de atenção rápida]\n\n"
                            f"🔧 QUANDO CHAMAR UM PROFISSIONAL:\n[a partir de que ponto vale a pena]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Domestica", f"{tipo_dom}: {descricao_dom[:40]}", res)
                        st.session_state['dom_temp'] = res
                else:
                    st.warning("Descreva o problema.")

            if st.session_state.get('dom_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['dom_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['dom_temp'], file_name="investigacao_domestica.txt", mime="text/plain", key="sherlock26")

            # ========================
            # INVESTIGAÇÃO DIGITAL
            # ========================

        with _sDigital:
            st.header("💻 Investigação Digital")

            tipo_dig = st.selectbox("O que você quer investigar:", ["Site suspeito","Mensagem/e-mail estranho","Perfil possivelmente falso","Link suspeito","Possível engenharia social","Outro"], key="sherlock27")
            descricao_dig = st.text_area("📝 Descreva o que você está vendo:", height=150,
                placeholder="ex: Recebi uma mensagem dizendo que ganhei um prêmio e pedindo para clicar em um link...", key="sherlock7_d2")

            if st.button("💻 ANALISAR", key="sherlock28"):
                if descricao_dig.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise esta situação digital suspeita.\n"
                            f"Tipo: {tipo_dig}. Descrição: {descricao_dig}\n\n"
                            f"FORMATO:\n\n"
                            f"💻 ANÁLISE DIGITAL — {tipo_dig.upper()}\n\n"
                            f"🚩 SINAIS DE ALERTA IDENTIFICADOS:\n[com base na descrição]\n\n"
                            f"🎭 TÉCNICA PROVÁVEL UTILIZADA:\n[se for um golpe, qual técnica é essa]\n\n"
                            f"📊 NÍVEL DE SUSPEITA: [Baixo/Médio/Alto]\n[justificativa]\n\n"
                            f"🛡️ O QUE FAZER:\n[ações recomendadas — não clicar, verificar, bloquear, etc]\n\n"
                            f"📚 COMO RECONHECER ISSO NO FUTURO:\n[padrão geral para identificar esse tipo de ameaça]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Digital", f"{tipo_dig}: {descricao_dig[:40]}", res)
                        st.session_state['dig_temp'] = res
                else:
                    st.warning("Descreva a situação.")

            if st.session_state.get('dig_temp'):
                st.markdown(f"<div class='card-red'>{st.session_state['dig_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['dig_temp'], file_name="investigacao_digital.txt", mime="text/plain", key="sherlock29")

            # ========================
            # FRAUDES E GOLPES
            # ========================

        with _sFraudes:
            st.header("💰 Fraudes e Golpes")

            golpe_select = st.selectbox("Golpe que você quer entender:", [
                "Golpe do Pix", "Golpe da falsa central bancária", "Golpe do falso boleto",
                "Golpe do amor (romance scam)", "Pirâmide financeira", "Golpe do falso emprego",
                "Investimento fraudulento", "Outro (descrever)",
            ], key="sherlock6_d2")
            descricao_golpe = ""
            if golpe_select == "Outro (descrever)":
                descricao_golpe = st.text_input("Descreva a situação:", key="sherlock30")

            if st.button("💰 ENTENDER ESSE GOLPE", key="sherlock31"):
                topico = descricao_golpe if golpe_select == "Outro (descrever)" and descricao_golpe.strip() else golpe_select
                if topico.strip():
                    with st.spinner("Preparando explicação..."):
                        prompt = (
                            f"Explique detalhadamente: {topico}\n\n"
                            f"FORMATO:\n\n"
                            f"💰 {topico.upper()}\n\n"
                            f"🎭 COMO FUNCIONA:\n[passo a passo de como os criminosos aplicam isso]\n\n"
                            f"🚩 SINAIS DE ALERTA:\n[como reconhecer]\n\n"
                            f"🛡️ COMO SE PROTEGER:\n[ações preventivas]\n\n"
                            f"⚡ COMO AGIR SE JÁ CAIU NESSE GOLPE:\n[passos imediatos]\n\n"
                            f"📂 INFORMAÇÕES IMPORTANTES A REUNIR:\n[o que documentar para denúncia/recuperação]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Fraudes", topico, res)
                        st.session_state['fraude_temp'] = res
                else:
                    st.warning("Escolha ou descreva o golpe.")

            if st.session_state.get('fraude_temp'):
                st.markdown(f"<div class='card-dark'>{st.session_state['fraude_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['fraude_temp'], file_name="fraudes_golpes.txt", mime="text/plain", key="sherlock32")

            # ========================
            # DETECTOR DE PADRÕES
            # ========================

        with _sPadroes:
            st.header("🔍 Detector de Padrões")

            dados_padroes = st.text_area("📝 Liste os dados (datas, pessoas, lugares, eventos):", height=180,
                placeholder="ex: Segunda - encontro com João no café X\nQuarta - mensagem de Maria sobre o mesmo assunto\n...", key="sherlock5_d2")

            if st.button("🔍 ENCONTRAR PADRÕES", key="sherlock33"):
                if dados_padroes.strip():
                    with st.spinner("Procurando padrões..."):
                        prompt = (
                            f"Analise estes dados procurando padrões e relações escondidas.\n"
                            f"Dados: {dados_padroes}\n\n"
                            f"FORMATO:\n\n"
                            f"🔍 PADRÕES IDENTIFICADOS\n\n"
                            f"🔗 RELAÇÕES ENTRE OS ELEMENTOS:\n[conexões encontradas entre datas, pessoas, lugares]\n\n"
                            f"📊 PADRÕES DE FREQUÊNCIA:\n[o que se repete e com que regularidade]\n\n"
                            f"⏰ PADRÕES TEMPORAIS:\n[horários ou dias que se destacam]\n\n"
                            f"🎯 PADRÃO MAIS SIGNIFICATIVO:\n[o que mais chama atenção, e por quê]\n\n"
                            f"❓ O QUE ISSO PODE SUGERIR:\n[hipóteses derivadas do padrão]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Padroes", "Detecção de padrões", res)
                        st.session_state['pad_temp'] = res
                else:
                    st.warning("Liste os dados.")

            if st.session_state.get('pad_temp'):
                st.markdown(f"<div class='card-teal'>{st.session_state['pad_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['pad_temp'], file_name="padroes.txt", mime="text/plain", key="sherlock34")

            # ========================
            # ANÁLISE DE PROBABILIDADES
            # ========================

        with _sProbabilidades:
            st.header("📊 Análise de Probabilidades")

            hipoteses_prob = st.text_area("📝 Liste as hipóteses que você já tem (uma por linha):", height=150,
                placeholder="ex: A pessoa esqueceu o compromisso\nA pessoa teve um imprevisto\nA pessoa evitou de propósito...", key="sherlock4_d2")
            evidencias_prob = st.text_area("📝 Evidências disponíveis:", height=100,
                placeholder="ex: Ela respondeu mensagens normalmente outras vezes...", key="sherlock3_d2")

            if st.button("📊 ANALISAR PROBABILIDADES", key="sherlock35"):
                if hipoteses_prob.strip():
                    with st.spinner("Calculando consistência..."):
                        prompt = (
                            f"Analise a consistência destas hipóteses com as evidências.\n"
                            f"Hipóteses: {hipoteses_prob}\n"
                            f"Evidências: {evidencias_prob or 'não informadas'}\n\n"
                            f"FORMATO:\n\n"
                            f"📊 ANÁLISE DE PROBABILIDADES\n\n"
                            f"[Para cada hipótese listada:]\n"
                            f"🧩 [HIPÓTESE]\n"
                            f"Consistência com as evidências: [X]/100\n"
                            f"Justificativa: [por quê]\n\n"
                            f"🎯 HIPÓTESE MAIS CONSISTENTE:\n[qual tem maior consistência com as evidências, e por quê — sem afirmar certeza absoluta]\n\n"
                            f"⚠️ LIMITAÇÃO DESTA ANÁLISE:\n[o que ainda impede uma conclusão definitiva]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Probabilidades", "Análise de probabilidades", res)
                        st.session_state['prob_temp'] = res
                else:
                    st.warning("Liste as hipóteses.")

            if st.session_state.get('prob_temp'):
                renderizar_indice(st.session_state['prob_temp'], "CONSISTÊNCIA GERAL")
                st.markdown(f"<div class='card'>{st.session_state['prob_temp']}</div>", unsafe_allow_html=True)
                st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['prob_temp'], file_name="probabilidades.txt", mime="text/plain", key="sherlock36")

            # ========================
            # PERGUNTAS INTELIGENTES
            # ========================

        with _sPerguntas:
            st.header("❓ Perguntas Inteligentes")

            situacao_perg = st.text_area("📝 Descreva a situação:", height=150, value=st.session_state.caso_padrao, key="situacao_perg")

            if st.button("❓ GERAR PERGUNTAS", key="sherlock37"):
                if situacao_perg.strip():
                    with st.spinner("Pensando nas perguntas certas..."):
                        prompt = (
                            f"Gere as perguntas que um investigador experiente faria sobre esta situação.\n"
                            f"Situação: {situacao_perg}\n\n"
                            f"FORMATO:\n\n"
                            f"❓ PERGUNTAS QUE UM INVESTIGADOR FARIA\n\n"
                            f"🎯 PERGUNTAS FUNDAMENTAIS:\n[5-7 perguntas essenciais que ainda não foram respondidas]\n\n"
                            f"🔍 PERGUNTAS QUE NINGUÉM PENSOU EM FAZER:\n[2-3 perguntas não óbvias mas potencialmente decisivas]\n\n"
                            f"💡 POR QUE ESSAS PERGUNTAS IMPORTAM:\n[explicação de como cada uma pode destravar a investigação]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Perguntas", situacao_perg[:60], res)
                        st.session_state['perg_temp'] = res
                else:
                    st.warning("Descreva a situação.")

            if st.session_state.get('perg_temp'):
                st.markdown(f"<div class='card-gold'>{st.session_state['perg_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['perg_temp'], file_name="perguntas.txt", mime="text/plain", key="sherlock38")

            # ========================
            # PENSAMENTO CRÍTICO
            # ========================

        with _sCritico:
            st.header("⚖️ Pensamento Crítico")

            raciocinio_critico = st.text_area("📝 Cole seu raciocínio ou conclusão sobre algo:", height=150,
                placeholder="ex: Acho que ela está escondendo algo porque ficou nervosa quando perguntei sobre o fim de semana...", key="sherlock2")

            if st.button("⚖️ ANALISAR MEU RACIOCÍNIO", key="sherlock39"):
                if raciocinio_critico.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise este raciocínio identificando possíveis vieses e erros de interpretação.\n"
                            f"Raciocínio: {raciocinio_critico}\n\n"
                            f"FORMATO:\n\n"
                            f"⚖️ ANÁLISE DO RACIOCÍNIO\n\n"
                            f"🧠 VIESES POSSÍVEIS IDENTIFICADOS:\n[viés de confirmação, ancoragem, etc — se aplicável]\n\n"
                            f"⚠️ POSSÍVEIS ERROS DE INTERPRETAÇÃO:\n[onde a conclusão pode estar pulando etapas]\n\n"
                            f"📊 GENERALIZAÇÕES:\n[se há generalização apressada]\n\n"
                            f"❓ FALTA DE EVIDÊNCIAS:\n[onde a conclusão se apoia em suposição, não fato]\n\n"
                            f"✅ COMO FORTALECER ESSE RACIOCÍNIO:\n[o que ajudaria a confirmar ou refutar com mais solidez]"
                        )
                        res = sherlock_ia(prompt)
                        salvar_caso("Critico", raciocinio_critico[:60], res)
                        st.session_state['crit_temp'] = res
                else:
                    st.warning("Cole seu raciocínio.")

            if st.session_state.get('crit_temp'):
                st.markdown(f"<div class='card-dark'>{st.session_state['crit_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['crit_temp'], file_name="pensamento_critico.txt", mime="text/plain", key="sherlock40")

            # ========================
            # MÉTODO SHERLOCK
            # ========================

        with _sMetodo:
            st.header("🧠 Método Sherlock")

            tecnica_metodo = st.selectbox("Técnica:", ["Dedução","Indução","Abdução","Observação","Eliminação de hipóteses","Raciocínio lógico","Investigação científica"], key="sherlock41")

            if st.button("🧠 APRENDER", key="sherlock42"):
                with st.spinner("Preparando explicação..."):
                    prompt = (
                        f"Explique de forma didática a técnica: {tecnica_metodo}\n\n"
                        f"FORMATO:\n\n"
                        f"🧠 {tecnica_metodo.upper()}\n\n"
                        f"📖 O QUE É:\n[definição clara]\n\n"
                        f"🔍 COMO FUNCIONA:\n[mecanismo passo a passo]\n\n"
                        f"💡 EXEMPLO PRÁTICO:\n[exemplo ilustrativo, fictício]\n\n"
                        f"🎯 QUANDO USAR:\n[situações onde essa técnica é mais útil]\n\n"
                        f"🏋️ EXERCÍCIO PARA TREINAR:\n[1 exercício prático]"
                    )
                    res = sherlock_ia(prompt)
                    salvar_caso("Metodo", tecnica_metodo, res)
                    st.session_state['metodo_temp'] = res

            if st.session_state.get('metodo_temp'):
                st.markdown(f"<div class='card'>{st.session_state['metodo_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['metodo_temp'], file_name="metodo.txt", mime="text/plain", key="sherlock43")

            # ========================
            # LABORATÓRIO FORENSE (EDUCATIVO)
            # ========================

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)
