import streamlit as st
import numpy as np

# Definimos la función mround
def mround(number, multiple):
    if multiple == 0:
        return 0
    else:
        return np.floor((number + multiple / 2) / multiple) * multiple

# Definimos la función para calcular los KT requeridos para un punto de habilidad
def kt_required_single_skill_point(current_skill, step_factor, ln_factor, speed_evolution):
    log_argument = max(current_skill - ln_factor, 1)
    kt_required = mround((step_factor ** np.log(log_argument) + 2048) / speed_evolution, 2)
    return kt_required

# Definimos la función para calcular el total de KT requeridos desde la habilidad actual hasta la habilidad objetivo
def calculate_total_kt(current_skill, target_skill, step_factor, ln_factor, speed_evolution):
    total_kt = 0
    for skill in range(current_skill, target_skill):
        total_kt += kt_required_single_skill_point(skill, step_factor, ln_factor, speed_evolution)
    return total_kt

# Definimos las constantes
STEP_FACTOR = 32
LN_FACTOR = 42
SPEED_EVOLUTION = {'K1': 48, 'K2': 24, 'K3': 12, 'K4': 12}

# Título de la aplicación
st.title('Calculadora de Fichas de Conocimiento para Scouts')

# Entradas del usuario para los niveles de habilidad
current_skill = st.number_input('Nivel de habilidad actual', min_value=1, value=42)
target_skill = st.number_input('Nivel de habilidad objetivo', min_value=current_skill+1, value=70)

# Botón para calcular los KT
if st.button('Calcular KT'):
    kt_k1 = calculate_total_kt(current_skill, target_skill, STEP_FACTOR, LN_FACTOR, SPEED_EVOLUTION['K1'])
    kt_k2 = calculate_total_kt(current_skill, target_skill, STEP_FACTOR, LN_FACTOR, SPEED_EVOLUTION['K2'])
    kt_k3 = calculate_total_kt(current_skill, target_skill, STEP_FACTOR, LN_FACTOR, SPEED_EVOLUTION['K3'])
    kt_k4 = calculate_total_kt(current_skill, target_skill, STEP_FACTOR, LN_FACTOR, SPEED_EVOLUTION['K4'])

    # Mostrar los resultados
    st.subheader('Fichas de Conocimiento necesarias:')
    st.write(f'K1: {kt_k1} KT')
    st.write(f'K2: {kt_k2} KT')
    st.write(f'K3: {kt_k3} KT')
    st.write(f'K4: {kt_k4} KT')
