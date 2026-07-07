import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Primeira versão do CultivAI",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
        /* Hide streamlit defaults */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Main styling */
        body {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        }
        
        .main {
            background: #f5f5f5;
            border-radius: 20px;
        }
        
        /* Phone frame styling */
        .phone-container {
            max-width: 380px;
            margin: 0 auto;
            background: white;
            border-radius: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            border: 12px solid #000;
        }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
            color: white;
            padding: 20px;
            text-align: left;
            border-radius: 0;
        }
        
        .header-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .header-greeting {
            font-size: 14px;
            opacity: 0.95;
            margin-bottom: 4px;
        }
        
        .header-alert {
            font-size: 13px;
            opacity: 0.85;
        }
        
        /* Cards */
        .plant-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .plant-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        /* Status badges */
        .status-badge {
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            white-space: nowrap;
            display: inline-block;
        }
        
        .status-warning {
            background: #FFF3CD;
            color: #856404;
        }
        
        .status-success {
            background: #D4EDDA;
            color: #155724;
        }
        
        .status-info {
            background: #D1ECF1;
            color: #0C5460;
        }
        
        /* Buttons */
        .btn-primary {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            border: none;
            font-weight: 500;
            cursor: pointer;
            width: 100%;
            margin-top: 16px;
            transition: all 0.3s ease;
        }
        
        .btn-primary:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        /* Quiz section */
        .quiz-progress {
            background: linear-gradient(135deg, #2E7D32 0%, #F57C00 100%);
            color: white;
            padding: 20px;
            border-radius: 12px 12px 0 0;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .quiz-progress-bar {
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 3px;
            margin: 12px 0;
            overflow: hidden;
        }
        
        .quiz-progress-fill {
            height: 100%;
            background: white;
            border-radius: 3px;
        }
        
        /* Problem alert */
        .problem-alert {
            background: #FFF3CD;
            border-left: 4px solid #FFC107;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 16px;
        }
        
        .alert-title {
            font-weight: 600;
            color: #856404;
            margin-bottom: 4px;
        }
        
        .alert-content {
            color: #856404;
        }
        
        /* Solution card */
        .solution-card {
            background: white;
            border: 1px solid #E8F5E9;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }
        
        .solution-title {
            font-weight: 600;
            color: #2E7D32;
            margin-bottom: 12px;
        }
        
        .solution-step {
            margin-bottom: 12px;
            font-size: 14px;
        }
        
        .step-number {
            font-weight: 600;
            color: #2E7D32;
            margin-right: 8px;
        }
        
        /* Section title */
        .section-title {
            font-size: 13px;
            font-weight: 500;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'home'
if 'quiz_question' not in st.session_state:
    st.session_state.quiz_question = 0
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = {}

# Quiz questions data
quiz_data = [
    {
        'question': 'Qual é seu tipo de espaço?',
        'options': ['🏢 Apartamento (sem varanda)', '🏠 Casa / Varanda (com espaço aberto)', '🌳 Quintal / Jardim (espaço grande)']
    },
    {
        'question': 'Quanto tempo você tem para cuidar?',
        'options': ['⏱️ Menos de 30 minutos/semana', '⏱️ 30-60 minutos/semana', '⏱️ Mais de 1 hora/semana']
    },
    {
        'question': 'Qual é seu clima?',
        'options': ['☀️ Tropical/Quente', '🌤️ Temperado', '❄️ Frio']
    },
    {
        'question': 'Você tem pets?',
        'options': ['🐕 Sim (cachorro)', '🐈 Sim (gato)', '❌ Não']
    },
    {
        'question': 'Qual é sua experiência?',
        'options': ['🌱 Iniciante', '🌿 Intermediário', '🌳 Experiente']
    },
    {
        'question': 'Qual tipo de planta interessa?',
        'options': ['🌸 Flores', '🌿 Folhagens', '🌵 Suculentas']
    }
]

# Plant data
plants_today = [
    {
        'emoji': '🌿',
        'name': 'Pothos #1',
        'status': 'Rega necessária',
        'days': 'HOJE',
        'badge_type': 'warning'
    },
    {
        'emoji': '🌱',
        'name': 'Suculenta #1',
        'status': 'Rega próxima',
        'days': '+2d',
        'badge_type': 'info'
    },
    {
        'emoji': '🌻',
        'name': 'Girassol #1',
        'status': 'Bem hidratado',
        'days': '✓ OK',
        'badge_type': 'success'
    }
]

# ===== HOME SCREEN =====
def show_home():
    st.markdown("""
        <div class="header">
            <div class="header-title">🌿 CultivAI</div>
            <div class="header-greeting">Bom dia, Maria!</div>
            <div class="header-alert">Suas plantas hoje: ⚠️ 2 precisam de água</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Quick actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('💧 Regar\n3', use_container_width=True, key='btn_water'):
            st.session_state.current_screen = 'camera'
            st.rerun()
    
    with col2:
        if st.button('📸 Foto\nPlantas', use_container_width=True, key='btn_photo'):
            st.session_state.current_screen = 'camera'
            st.rerun()
    
    st.write("")
    
    # Plants section
    st.markdown('<p class="section-title">Hoje você precisa regar:</p>', unsafe_allow_html=True)
    
    for idx, plant in enumerate(plants_today):
        col1, col2, col3 = st.columns([0.5, 3, 1])
        
        with col1:
            st.write(plant['emoji'])
        
        with col2:
            st.write(f"**{plant['name']}**  \n{plant['status']}")
        
        with col3:
            badge_class = f"status-badge status-{plant['badge_type']}"
            st.markdown(f'<span class="{badge_class}">{plant["days"]}</span>', unsafe_allow_html=True)
        
        if idx < len(plants_today) - 1:
            st.divider()
    
    st.write("")
    st.write("")
    
    # Add plant button
    if st.button('+ Adicionar Planta', use_container_width=True, key='btn_add_plant'):
        st.session_state.current_screen = 'quiz'
        st.session_state.quiz_question = 0
        st.rerun()


# ===== QUIZ SCREEN =====
def show_quiz():
    current_q = st.session_state.quiz_question
    total_q = len(quiz_data)
    progress_percent = ((current_q + 1) / total_q) * 100
    
    st.markdown(f"""
        <div class="quiz-progress">
            <div style="font-size: 13px; font-weight: 500; margin-bottom: 12px;">Pergunta {current_q + 1} de {total_q}</div>
            <div class="quiz-progress-bar">
                <div class="quiz-progress-fill" style="width: {progress_percent}%"></div>
            </div>
            <div style="font-size: 18px; font-weight: 500; margin-top: 12px;">{quiz_data[current_q]['question']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Options
    for idx, option in enumerate(quiz_data[current_q]['options']):
        if st.button(option, use_container_width=True, key=f'quiz_option_{current_q}_{idx}'):
            st.session_state.selected_options[current_q] = idx
    
    st.write("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('← Voltar', use_container_width=True, key='btn_back_quiz'):
            st.session_state.current_screen = 'home'
            st.rerun()
    
    with col2:
        if st.button('Próximo →', use_container_width=True, key='btn_next_quiz'):
            if current_q < total_q - 1:
                st.session_state.quiz_question += 1
                st.rerun()
            else:
                st.success('🎉 Parabéns! Seu perfil foi configurado!')
                st.session_state.current_screen = 'home'
                st.session_state.quiz_question = 0
                st.rerun()


# ===== CAMERA SCREEN =====
def show_camera():
    st.write("")
    st.write("")
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.3) 0%, rgba(46, 125, 50, 0.5) 100%); 
                    height: 400px; display: flex; justify-content: center; align-items: center; 
                    color: white; border-radius: 12px; margin-bottom: 16px; flex-direction: column;">
            <div style="font-size: 100px; opacity: 0.6; margin-bottom: 16px;">📸</div>
            <p style="margin: 0; opacity: 0.9; font-weight: 500;">Câmera de captura</p>
            <p style="font-size: 12px; opacity: 0.7; margin: 8px 0 0 0;">Enquadre a folha dentro do círculo</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    if st.button('🎬 CAPTURAR', use_container_width=True, key='btn_capture'):
        st.session_state.current_screen = 'diagnosis'
        st.rerun()
    
    st.write("")
    
    if st.button('← Voltar', use_container_width=True, key='btn_back_camera'):
        st.session_state.current_screen = 'home'
        st.rerun()


# ===== DIAGNOSIS SCREEN =====
def show_diagnosis():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("")
    
    with col2:
        st.markdown('<span class="status-badge" style="background: #D4EDDA; color: #155724;">94% seguro</span>', unsafe_allow_html=True)
    
    st.write("")
    
    # Plant image
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.3) 0%, rgba(46, 125, 50, 0.4) 100%); 
                    height: 240px; display: flex; justify-content: center; align-items: center; 
                    border-radius: 12px; margin-bottom: 16px; font-size: 100px;">
            🌿
        </div>
    """, unsafe_allow_html=True)
    
    # Plant info
    st.markdown("""
        <div class="solution-card">
            <div style="font-size: 16px; font-weight: 600; color: #333; margin-bottom: 8px;">🌿 Pothos (Pictus)</div>
            <div style="font-size: 13px; color: #666; margin-bottom: 8px;">
                <strong>Nível de dificuldade:</strong> <span style="color: #2E7D32; font-weight: 600;">⭐ Muito Fácil</span>
            </div>
            <div style="font-size: 13px; color: #666;">
                <strong>Frequência de rega:</strong> <span style="color: #2E7D32; font-weight: 600;">7-10 dias</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🌿 Planta", "⚠️ Problema", "✅ Solução"])
    
    with tab1:
        st.write("**Informações detalhadas sobre a planta:**")
        st.write("""
        - 🌡️ Temperatura ideal: 18-25°C
        - 💡 Luz: Indireta (sem luz solar direta)
        - 💧 Rega: A cada 7-10 dias
        - 🌍 Solo: Bem drenado
        - ⚠️ Tóxico para pets: Sim
        """)
    
    with tab2:
        # Problem alert
        st.markdown("""
            <div class="problem-alert">
                <div class="alert-title">⚠️ POSSÍVEL PROBLEMA IDENTIFICADO:</div>
                <div class="alert-content" style="font-size: 16px; font-weight: 600; margin-top: 8px;">Ácaro-aranha</div>
                <div style="font-size: 12px; color: #856404; opacity: 0.8; margin-top: 8px;">
                    <strong>Confiança:</strong> 87%<br>
                    <strong>Sintomas:</strong> Folhas com pequenas manchas e teias finas
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        # Solution
        st.markdown("""
            <div class="solution-card">
                <div class="solution-title">✅ SOLUÇÃO RÁPIDA (recomendado):</div>
                <div class="solution-step">
                    <span class="step-number">1.</span>
                    Pulverize com água + sabão neutro (1 colher em 1L de água)
                </div>
                <div class="solution-step">
                    <span class="step-number">2.</span>
                    Limpe delicadamente cada folha com algodão macio
                </div>
                <div class="solution-step">
                    <span class="step-number">3.</span>
                    Repita em 3 dias se necessário
                </div>
                <div class="solution-step">
                    <span class="step-number">4.</span>
                    Mantenha a planta isolada de outras por 1 semana
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button('📤 Compartilhar', use_container_width=True, key='btn_share')
    
    with col2:
        st.button('💾 Salvar', use_container_width=True, key='btn_save')
    
    with col3:
        st.button('Saiba mais →', use_container_width=True, key='btn_learn_more')
    
    st.write("")
    
    if st.button('← Voltar', use_container_width=True, key='btn_back_diagnosis'):
        st.session_state.current_screen = 'camera'
        st.rerun()


# ===== MAIN APP =====
def main():
    # Remove margin top
    st.markdown("""
        <style>
            .appViewContainer {
                padding-top: 0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown("""
        <h1 style="text-align: center; color: #2E7D32; margin-bottom: 20px; margin-top: 0;">
            🌿 Primeira versão do CultivAI
        </h1>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Screen routing
    if st.session_state.current_screen == 'home':
        show_home()
    elif st.session_state.current_screen == 'quiz':
        show_quiz()
    elif st.session_state.current_screen == 'camera':
        show_camera()
    elif st.session_state.current_screen == 'diagnosis':
        show_diagnosis()
    
    # Bottom navigation (info)
    st.write("")
    st.write("")
    st.markdown("""
        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0; 
                    text-align: center; font-size: 12px; color: #999;">
            <div style="display: flex; justify-content: space-around;">
                <div>🏠 Home</div>
                <div>🔍 Buscar</div>
                <div>👥 Comunidade</div>
                <div>⭐ Premium</div>
                <div>👤 Perfil</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
