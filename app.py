import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np

# =====================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================
st.set_page_config(
    page_title="📋 Simulación BPMN - Banco ABC",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Banco ABC - Análisis y Simulación de Procesos BPMN")
st.markdown("---")

# =====================================================
# 1. DIAGRAMA BPMN (cargado desde archivo fijo)
# =====================================================
st.header("📐 Diagrama BPMN del Proceso")

# Leer el archivo BPMN fijo
with open("banco_abc.bpmn", "r", encoding="utf-8") as f:
    bpmn_xml = f.read()

# HTML para visualizar el diagrama con bpmn-js
html_viewer = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://unpkg.com/bpmn-js@11.5.0/dist/bpmn-viewer.development.js"></script>
    <style>
        body {{ margin: 0; padding: 0; background: #f8f9fa; }}
        #canvas {{ height: 550px; width: 100%; background: white; border: 1px solid #ddd; border-radius: 8px; }}
    </style>
</head>
<body>
    <div id="canvas"></div>
    <script>
        const viewer = new BpmnJS({{ container: '#canvas' }});
        const bpmnXml = `{bpmn_xml}`;
        viewer.importXML(bpmnXml).catch(err => console.error(err));
    </script>
</body>
</html>
"""

st.components.v1.html(html_viewer, height=600, scrolling=False)

# =====================================================
# 2. CARGAR RESULTADOS
# =====================================================
with open("resultados_simulacion.json", "r", encoding="utf-8") as f:
    resultados = json.load(f)

# =====================================================
# 3. MÉTRICAS PRINCIPALES
# =====================================================
st.header("📊 Resultados de la Simulación")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⏱️ Tiempo de ciclo promedio",
        resultados["tiempo_ciclo_texto"]
    )

with col2:
    st.metric(
        "💰 Costo total",
        f"${resultados['costo_total']:,.2f}"
    )

with col3:
    st.metric(
        "👥 Clientes simulados",
        resultados["instancias"],
        delta="6 meses"
    )

# =====================================================
# 4. CUELLO DE BOTELLA
# =====================================================
st.markdown("---")
st.header("🚨 Cuello de Botella Detectado")

recurso_bottleneck = max(resultados["recursos"], key=resultados["recursos"].get)
utilizacion_bottleneck = resultados["recursos"][recurso_bottleneck]

col_b1, col_b2 = st.columns([1, 2])

with col_b1:
    st.warning(f"**{recurso_bottleneck}**")
    st.metric(
        "Utilización",
        f"{utilizacion_bottleneck:.2f}%",
        delta="⚠️ Saturado"
    )

with col_b2:
    st.info("""
    **Impacto en el proceso:**
    - Los clientes que consultan por **préstamos** (38% del total)
    - Esperan en promedio **2.8 días** para ser atendidos
    - Esto genera insatisfacción y posibles pérdidas de clientes
    """)

# =====================================================
# 5. UTILIZACIÓN DE RECURSOS
# =====================================================
st.subheader("📈 Utilización de Recursos")

recursos_data = []
for nombre, utilizacion in resultados["recursos"].items():
    if utilizacion > 85:
        estado = "🔴 Saturado"
    elif utilizacion > 60:
        estado = "🟡 Medio"
    else:
        estado = "🟢 Normal"
    recursos_data.append({
        "Recurso": nombre,
        "Utilización": f"{utilizacion:.2f}%",
        "Estado": estado
    })

st.table(recursos_data)

# =====================================================
# 6. DISTRIBUCIÓN DE CLIENTES
# =====================================================
st.subheader("📊 Distribución de Clientes por Tipo de Consulta")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

tipos = list(resultados["distribucion_clientes"].keys())
valores = list(resultados["distribucion_clientes"].values())
colores_barra = ["#ff6b6b", "#4ecdc4", "#45b7d1"]

# Gráfico de barras
ax1.bar(tipos, valores, color=colores_barra, edgecolor="black", linewidth=1)
ax1.set_title("Cantidad de Clientes por Tipo")
ax1.set_ylabel("Número de clientes")
ax1.set_xlabel("Tipo de consulta")
for i, v in enumerate(valores):
    ax1.text(i, v + 10, str(v), ha="center", fontweight="bold")

# Gráfico de torta
ax2.pie(valores, labels=tipos, autopct="%1.1f%%", colors=colores_barra, startangle=90)
ax2.set_title("Proporción de Clientes por Tipo")

plt.tight_layout()
st.pyplot(fig)

# =====================================================
# 7. TIEMPOS DE ESPERA
# =====================================================
st.subheader("⏱️ Tiempos de Espera por Tipo de Consulta")

tiempos_data = []
for tipo, tiempo in resultados["tiempos_espera"].items():
    tiempos_data.append({
        "Tipo de consulta": tipo.replace("ATENDER CONSULTA ", ""),
        "Tiempo de espera": f"{tiempo} días"
    })

st.table(tiempos_data)

# =====================================================
# 8. PROPUESTA DE REDISEÑO
# =====================================================
st.markdown("---")
st.header("🔄 Propuesta de Rediseño")

st.markdown(f"""
### 🎯 Problema identificado
El recurso **{recurso_bottleneck}** está saturado al **{utilizacion_bottleneck:.2f}%**, 
generando tiempos de espera de **2.8 días** para los clientes de préstamos.

### 💡 Solución propuesta
Aplicando la heurística **"Case assignment"** del Capítulo 8 de Dumas et al. (2018):

> **Agregar un segundo Administrativo de Préstamos** (pasar de 1 a 2 recursos)

### 📊 Impacto esperado

| Dimensión | Impacto |
|-----------|---------|
| **Time** | ✅ Reducción de 2.8 días a ~1.2 días |
| **Cost** | ⚠️ Aumento del costo en $5.800/hora (nuevo recurso) |
| **Quality** | ✅ Mejora en la satisfacción del cliente |
| **Flexibility** | ✅ Mayor resiliencia ante picos de demanda |
""")

# =====================================================
# 9. CONCLUSIÓN
# =====================================================
st.markdown("---")
st.header("✅ Conclusión")

st.success(f"""
El análisis cualitativo y cuantitativo del proceso de atención al cliente del Banco ABC 
permitió identificar un **cuello de botella en el Administrativo de Préstamos** con 
una utilización del {utilizacion_bottleneck:.2f}%.

La propuesta de rediseño consiste en agregar un segundo Administrativo de Préstamos, 
lo que permitiría reducir el tiempo de espera de 2.8 días a 1.2 días y mejorar la 
satisfacción del cliente.

El costo total del proceso para 1000 clientes es de **${resultados['costo_total']:,.2f}** 
con un costo promedio de **${resultados['costo_promedio']:.2f}** por cliente.
""")