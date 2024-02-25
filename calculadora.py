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

# Definimos la función para calcular el Overall Knowledge Skill basado en las habilidades objetivo
def calculate_overall_knowledge(k1, k2, k3, k4):
    return 0.7 * k1 + 0.2 * k2 + 0.05 * k3 + 0.05 * k4

# Definimos las constantes
STEP_FACTOR = 32
LN_FACTOR = 42
SPEED_EVOLUTION = {'K1': 48, 'K2': 24, 'K3': 12, 'K4': 12}

# Título de la aplicación
st.title('Calculadora de Fichas de Conocimiento para Scouts')

# Entradas del usuario para los niveles de habilidad de origen y destino
st.subheader("Niveles de habilidad de origen y destino")
skills = ['K1', 'K2', 'K3', 'K4']
current_skills = {}
target_skills = {}
total_kt_cost = 0

for skill in skills:
    current_skills[skill] = st.number_input(f'Nivel actual de {skill}', min_value=0, value=50, key=f'current_{skill}')
    target_skills[skill] = st.number_input(f'Nivel objetivo de {skill}', min_value=current_skills[skill]+1, value=80, key=f'target_{skill}')

# Botón para calcular los KT y el Overall Knowledge Skill
if st.button('Calcular KT y Overall Knowledge Skill'):
    total_kt_by_skill = {}
    for skill in skills:
        total_kt_by_skill[skill] = calculate_total_kt(current_skills[skill], target_skills[skill], STEP_FACTOR, LN_FACTOR, SPEED_EVOLUTION[skill])
        total_kt_cost += total_kt_by_skill[skill]

    # Mostrar los resultados individuales y el costo total de KT
    st.subheader('Fichas de Conocimiento necesarias por habilidad y total:')
    for skill, kt in total_kt_by_skill.items():
        st.write(f'{skill}: {kt} KT')
    st.write(f'Total KT necesario: {total_kt_cost} KT')

    # Calcular y mostrar el Overall Knowledge Skill con las habilidades objetivo
    overall_knowledge = calculate_overall_knowledge(target_skills['K1'], target_skills['K2'], target_skills['K3'], target_skills['K4'])
    st.subheader('Nivel de habilidad general con las habilidades objetivo:')
    st.write(f'Overall Knowledge Skill: {overall_knowledge}')

# Agregamos los enlaces al final del script
st.markdown('Consulta cuáles son los K de tu Scout aquí: [Whitepaper MetaSoccer](https://whitepaper.metasoccer.com/metasoccer/game-assets/youth-scout#knowledge)')
st.markdown('Calculadora en desarrollo por [elrepre77](https://twitter.com/elrepre77)')

