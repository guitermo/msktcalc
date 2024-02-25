# Integración de las entradas y la lógica en la interfaz de Streamlit
import streamlit as st
import numpy as np

# Definimos las funciones necesarias
def mround(number, multiple):
    return np.floor((number + multiple / 2) / multiple) * multiple

def kt_required_single_skill_point(current_skill, step_factor, ln_factor, speed_evolution):
    log_argument = max(current_skill - ln_factor, 1)
    return mround((step_factor ** np.log(log_argument) + 2048) / speed_evolution, 2)

def calculate_total_kt(current_skill, target_skill, step_factor, ln_factor, speed_evolution):
    total_kt = 0
    for skill in range(current_skill, target_skill):
        total_kt += kt_required_single_skill_point(skill, step_factor, ln_factor, speed_evolution)
    return total_kt

def calculate_overall_knowledge(k1, k2, k3, k4):
    return 0.7 * k1 + 0.2 * k2 + 0.05 * k3 + 0.05 * k4

def estimate_initial_k_values(current_ov):
    k1 = current_ov / 0.7
    k2_k3_k4_value = (current_ov - 0.7 * k1) / 0.3
    k2 = k3 = k4 = k2_k3_k4_value
    return k1, k2, k3, k4

STEP_FACTOR = 32
LN_FACTOR = 42
SPEED_EVOLUTION = {'K1': 48, 'K2': 24, 'K3': 12, 'K4': 12}

# Interfaz de usuario en Streamlit
st.title('Calculadora de Fichas de Conocimiento para Scouts')
scout_type = st.selectbox("Selecciona el tipo de scout", ["Portero", "Defensor o Mediocampista (CDM)", "Mediocampista de Cobertura", "Delantero o Mediocampista (CAM)"])

# Entrada para el OV actual y objetivo
current_ov = st.number_input('Nivel de habilidad general actual (OV)', min_value=1.0, value=29.0)
target_overall = st.number_input('Nivel de habilidad general objetivo (OV)', min_value=1.0, value=80.0)

# Estimación de los valores iniciales de K y su presentación
initial_k_values = estimate_initial_k_values(current_ov)
st.subheader('Estimación de niveles de habilidad actuales basados en el OV:')
st.write(f'K1 inicial estimado: {initial_k_values[0]:.2f}')
st.write(f'K2 inicial estimado: {initial_k_values[1]:.2f}')
st.write(f'K3 inicial estimado: {initial_k_values[2]:.2f}')
st.write(f'K4 inicial estimado: {initial_k_values[3]:.2f}')

# Botón para realizar el cálculo de KT
if st.button('Calcular KT para alcanzar el OV objetivo'):
    total_kt = {}
    for i, key in enumerate(SPEED_EVOLUTION.keys(), 1):
        k_current = initial_k_values[i-1]
        # Suponemos que el OV objetivo se alcanza mejorando K1 hasta el nivel deseado y ajustando los demás proporcionalmente
        # Esta es una simplificación y puede que necesite un enfoque diferente dependiendo de la lógica del juego
        k_target = target_overall / 0.7 if key == 'K1' else k_current
        total_kt[key] = calculate_total_kt(k_current, k_target, STEP_FACTOR, LN_FACTOR, SPEED_EVOLUTION[key])

    # Mostrar los resultados de KT necesarios
    st.subheader('Fichas de Conocimiento necesarias por habilidad para alcanzar el OV objetivo:')
    for key, value in total_kt.items():
        st.write(f'{key}: {value} KT')


