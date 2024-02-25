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

initial_ov = st.number_input('Nivel de habilidad general inicial', min_value=1, value=50)

# Estimamos los valores iniciales de K basados en el OV inicial
# La lógica para estimar los valores de K puede variar dependiendo de la información adicional que tengas
estimated_k2_to_k4 = initial_ov / 2
estimated_k1 = (initial_ov - 0.2 * estimated_k2_to_k4 - 0.05 * estimated_k2_to_k4 - 0.05 * estimated_k2_to_k4) / 0.7

# Asumimos que los valores de K2, K3 y K4 son iguales para simplificar
current_skills = {
    'K1': estimated_k1,
    'K2': estimated_k2_to_k4,
    'K3': estimated_k2_to_k4,
    'K4': estimated_k2_to_k4
}

# Mostramos los valores estimados de K
st.write(f'Estimación de K1: {current_skills["K1"]}')
st.write(f'Estimación de K2, K3, K4: {current_skills["K2"]}')

target_overall = st.number_input('Nivel de habilidad general objetivo', min_value=initial_ov+1, value=70)

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
