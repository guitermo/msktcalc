import streamlit as st
import numpy as np

def mround(number, multiple):
    if multiple == 0:
        return 0
    else:
        return np.floor((number + multiple / 2) / multiple) * multiple

def kt_required_single_skill_point(current_skill, step_factor, ln_factor, speed_evolution):
    log_argument = max(current_skill - ln_factor, 1)
    kt_required = mround((step_factor ** np.log(log_argument) + 2048) / speed_evolution, 2)
    return kt_required

def calculate_total_kt(current_skill, target_skill, step_factor, ln_factor, speed_evolution):
    total_kt = 0
    for skill in range(current_skill, target_skill):
        total_kt += kt_required_single_skill_point(skill, step_factor, ln_factor, speed_evolution)
    return total_kt

def calculate_overall_knowledge(k1, k2, k3, k4):
    return 0.7 * k1 + 0.2 * k2 + 0.05 * k3 + 0.05 * k4

STEP_FACTOR = 32
LN_FACTOR = 42
SPEED_EVOLUTION = {'K1': 48, 'K2': 24, 'K3': 12, 'K4': 12}

st.title('Calculadora de Fichas de Conocimiento para Scouts')

scout_type = st.selectbox("Selecciona el tipo de scout", ["Portero", "Defensor o Mediocampista (CDM)", "Mediocampista de Cobertura", "Delantero o Mediocampista (CAM)"])
current_skills = {
    'K1': st.number_input('Nivel actual de K1', min_value=1, value=50),
    'K2': st.number_input('Nivel actual de K2', min_value=1, value=50),
    'K3': st.number_input('Nivel actual de K3', min_value=1, value=50),
    'K4': st.number_input('Nivel actual de K4', min_value=1, value=50)
}
target_overall = st.number_input('Nivel de habilidad general objetivo', min_value=1, value=70)

if st.button('Calcular KT y Nivel General'):
    total_kt = {}
    for key in current_skills:
        total_kt[key] = calculate_total_kt(current_skills[key], target_overall, STEP_FACTOR, LN_FACTOR, SPEED_EVOLUTION[key])

    for key, value in total_kt.items():
        st.write(f'{key}: {value} KT')

    k_values = list(current_skills.values())
    overall_knowledge = calculate_overall_knowledge(*k_values)
    st.subheader('Nivel de habilidad general alcanzado:')
    st.write(f'Overall Knowledge Skill: {overall_knowledge}')
