# 🏦 Banco ABC - Simulación BPMN

## 📋 Descripción

Este proyecto presenta el análisis y simulación del proceso de atención al cliente del Banco ABC, utilizando técnicas de BPMN (Business Process Model and Notation) y simulación de procesos.

## 🎯 Objetivos

- Modelar el proceso de atención al cliente en BPMN
- Simular el proceso utilizando BIMP (Business Process Simulator)
- Identificar cuellos de botella y proponer mejoras

## 📊 Resultados Principales

- **Tiempo de ciclo promedio:** 1.2 días
- **Costo total:** $3.7M para 1000 clientes
- **Cuello de botella:** Administrativo de Préstamos (99.71% utilización)

## 🛠️ Tecnologías utilizadas

- [Streamlit](https://streamlit.io/) - Framework para la aplicación web
- [bpmn-js](https://bpmn.io/) - Visualizador de diagramas BPMN
- [BIMP](https://bimp.cs.ut.ee/) - Simulador de procesos BPMN

## 🚀 Cómo ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
