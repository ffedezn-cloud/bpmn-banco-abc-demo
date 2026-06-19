import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np
import base64

# =====================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================
st.set_page_config(
    page_title="Simulación BPMN - Banco ABC",
    page_icon="🏦",
    layout="wide"
)

# Estilos CSS personalizados para un look más limpio
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        font-size: 1.1rem;
        color: #4a4a6a;
        margin-bottom: 2rem;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 500;
        color: #2d2d44;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1a1a2e;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6c6c8a;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .bottleneck-card {
        background: #fff5f5;
        border-left: 4px solid #dc3545;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }
    .bottleneck-title {
        font-weight: 600;
        color: #dc3545;
        font-size: 1.1rem;
    }
    .info-card {
        background: #f0f7ff;
        border-left: 4px solid #2b6cb0;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }
    .success-card {
        background: #f0fff4;
        border-left: 4px solid #38a169;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }
    .footer {
        text-align: center;
        color: #8888aa;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# ENCABEZADO
# =====================================================
st.markdown('<div class="main-title">Banco ABC</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Análisis y Simulación del Proceso de Atención al Cliente</div>', unsafe_allow_html=True)
st.divider()

# =====================================================
# 1. DIAGRAMA BPMN - VERSIÓN CORREGIDA
# =====================================================
st.markdown('<div class="section-title">Diagrama BPMN del Proceso</div>', unsafe_allow_html=True)

# Leer el archivo BPMN fijo
with open("banco_abc.bpmn", "r", encoding="utf-8") as f:
    bpmn_xml = f.read()

# Escapar el XML para JavaScript
bpmn_xml_escaped = bpmn_xml.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")

# HTML con bpmn-js y zoom nativo
html_viewer = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://unpkg.com/bpmn-js@11.5.0/dist/bpmn-viewer.development.js"></script>
    <style>
        body {{ margin: 0; padding: 0; background: #f5f6fa; font-family: sans-serif; }}
        #canvas-container {{
            height: 600px;
            width: 100%;
            background: white;
            border: 1px solid #d0d0d0;
            border-radius: 10px;
            overflow: auto;
            position: relative;
        }}
        #canvas {{
            height: 100%;
            width: 100%;
            min-height: 500px;
        }}
        .controls {{
            display: flex;
            gap: 10px;
            padding: 10px 0;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
        }}
        .controls button {{
            padding: 6px 16px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: 0.2s;
        }}
        .controls button:hover {{
            background: #e8e8e8;
            border-color: #999;
        }}
        .controls .zoom-label {{
            font-size: 13px;
            color: #555;
            font-weight: 500;
            margin: 0 5px;
        }}
        .controls input[type="range"] {{
            width: 120px;
            accent-color: #2b6cb0;
            cursor: pointer;
        }}
        .error-message {{
            color: #c0392b;
            padding: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div id="canvas-container">
        <div id="canvas"></div>
    </div>
    <div class="controls">
        <button onclick="zoomIn()">Zoom In</button>
        <button onclick="zoomOut()">Zoom Out</button>
        <button onclick="resetZoom()">Reset</button>
        <span class="zoom-label">Zoom: <span id="zoomLevel">100</span>%</span>
        <input type="range" id="zoomSlider" min="20" max="200" value="100" step="5"
               oninput="setZoom(this.value)">
    </div>
    <script>
        // Inicializar el viewer sin extensiones externas
        const viewer = new BpmnJS({{
            container: '#canvas',
            width: '100%',
            height: '100%'
        }});

        const bpmnXml = `{bpmn_xml_escaped}`;

        // Función para actualizar el display del zoom
        function updateZoomDisplay() {{
            try {{
                const canvas = viewer.get('canvas');
                const zoom = canvas.zoom();
                const percent = Math.round(zoom * 100);
                document.getElementById('zoomLevel').textContent = percent;
                document.getElementById('zoomSlider').value = percent;
            }} catch(e) {{
                // Ignorar errores si aún no está cargado
            }}
        }}

        // Cargar el diagrama
        viewer.importXML(bpmnXml)
            .then(function() {{
                const canvas = viewer.get('canvas');
                canvas.zoom('fit-viewport');
                setTimeout(updateZoomDisplay, 100);
            }})
            .catch(function(err) {{
                console.error('Error loading BPMN:', err);
                document.getElementById('canvas').innerHTML = 
                    '<p class="error-message">Error al cargar el diagrama.</p>';
            }});

        // Funciones de zoom
        function getZoom() {{
            try {{
                const canvas = viewer.get('canvas');
                return canvas.zoom();
            }} catch(e) {{
                return 1.0;
            }}
        }}

        function setZoom(value) {{
            try {{
                const canvas = viewer.get('canvas');
                const zoomVal = parseFloat(value) / 100;
                canvas.zoom(zoomVal);
                document.getElementById('zoomLevel').textContent = Math.round(value);
            }} catch(e) {{
                // Ignorar
            }}
        }}

        function zoomIn() {{
            try {{
                const canvas = viewer.get('canvas');
                const currentZoom = canvas.zoom();
                const newZoom = Math.min(currentZoom * 1.2, 2.0);
                canvas.zoom(newZoom);
                setTimeout(updateZoomDisplay, 50);
            }} catch(e) {{
                // Ignorar
            }}
        }}

        function zoomOut() {{
            try {{
                const canvas = viewer.get('canvas');
                const currentZoom = canvas.zoom();
                const newZoom = Math.max(currentZoom / 1.2, 0.2);
                canvas.zoom(newZoom);
                setTimeout(updateZoomDisplay, 50);
            }} catch(e) {{
                // Ignorar
            }}
        }}

        function resetZoom() {{
            try {{
                const canvas = viewer.get('canvas');
                canvas.zoom('fit-viewport');
                setTimeout(updateZoomDisplay, 50);
            }} catch(e) {{
                // Ignorar
            }}
        }}

        // Escuchar eventos de zoom del canvas
        viewer.on('canvas.zoom', function() {{
            setTimeout(updateZoomDisplay, 50);
        }});

        // Intentar actualizar el display después de la carga
        setTimeout(function() {{
            try {{
                updateZoomDisplay();
            }} catch(e) {{
                // Ignorar
            }}
        }}, 500);
    </script>
</body>
</html>
"""

st.components.v1.html(html_viewer, height=650, scrolling=False)

# =====================================================
# 2. CARGAR RESULTADOS
# =====================================================
try:
    with open("resultados_simulacion.json", "r", encoding="utf-8") as f:
        resultados = json.load(f)
except Exception as e:
    st.error(f"Error al cargar resultados: {e}")
    st.stop()

# =====================================================
# 3. MÉTRICAS PRINCIPALES
# =====================================================
st.markdown('<div class="section-title">Resultados de la Simulación</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Tiempo de ciclo promedio</div>
        <div class="metric-value">{resultados.get('tiempo_ciclo_texto', '1.2 días')}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Costo total</div>
        <div class="metric-value">${resultados.get('costo_total', 0):,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Clientes simulados</div>
        <div class="metric-value">{resultados.get('instancias', 1000)}</div>
        <div style="font-size:0.8rem; color:#6c6c8a;">(6 meses)</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================================
# 4. CUELLO DE BOTELLA
# =====================================================
st.markdown('<div class="section-title">Cuello de Botella Detectado</div>', unsafe_allow_html=True)

recursos = resultados.get("recursos", {})
if recursos:
    recurso_bottleneck = max(recursos, key=recursos.get)
    utilizacion_bottleneck = recursos[recurso_bottleneck]
else:
    recurso_bottleneck = "No disponible"
    utilizacion_bottleneck = 0

col_b1, col_b2 = st.columns([1, 2])

with col_b1:
    st.markdown(f"""
    <div class="bottleneck-card">
        <div class="bottleneck-title">{recurso_bottleneck}</div>
        <div style="font-size:2rem; font-weight:600; color:#dc3545;">{utilizacion_bottleneck:.2f}%</div>
        <div style="color:#6c6c8a; font-size:0.9rem;">Utilización</div>
        <div style="color:#dc3545; font-weight:500; margin-top:0.3rem;">Saturado</div>
    </div>
    """, unsafe_allow_html=True)

with col_b2:
    st.markdown("""
    <div class="info-card">
        <strong style="color:#2b6cb0;">Impacto en el proceso</strong>
        <ul style="margin:0.5rem 0; padding-left:1.2rem;">
            <li>Los clientes que consultan por <strong>préstamos</strong> (38% del total)</li>
            <li>Esperan en promedio <strong>2.8 días</strong> para ser atendidos</li>
            <li>Esto genera insatisfacción y posibles pérdidas de clientes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================================
# 5. UTILIZACIÓN DE RECURSOS
# =====================================================
st.markdown('<div class="section-title">Utilización de Recursos</div>', unsafe_allow_html=True)

for nombre, utilizacion in recursos.items():
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"**{nombre}**")
        st.progress(utilizacion / 100, text=f"{utilizacion:.2f}%")
    with col2:
        if utilizacion > 85:
            st.write("Saturado")
        elif utilizacion > 60:
            st.write("Medio")
        else:
            st.write("Normal")
    with col3:
        st.write(f"{utilizacion:.2f}%")
    st.divider()

# =====================================================
# 6. DISTRIBUCIÓN DE CLIENTES
# =====================================================
st.markdown('<div class="section-title">Distribución de Clientes por Tipo de Consulta</div>', unsafe_allow_html=True)

distribucion = resultados.get("distribucion_clientes", {})
if distribucion:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    tipos = list(distribucion.keys())
    valores = list(distribucion.values())
    colores_barra = ["#e74c3c", "#3498db", "#2ecc71"]

    # Gráfico de barras
    bars = ax1.bar(tipos, valores, color=colores_barra, edgecolor="white", linewidth=1.5)
    ax1.set_title("Cantidad de Clientes", fontsize=14, fontweight=600)
    ax1.set_ylabel("Número de clientes", fontsize=12)
    ax1.set_xlabel("Tipo de consulta", fontsize=12)
    for bar, v in zip(bars, valores):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8, str(v), 
                ha="center", fontweight=600, fontsize=11)

    # Gráfico de torta
    wedges, texts, autotexts = ax2.pie(valores, labels=tipos, autopct="%1.1f%%", 
                                       colors=colores_barra, startangle=90,
                                       textprops={'fontsize': 11, 'fontweight': 500})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    ax2.set_title("Proporción de Clientes", fontsize=14, fontweight=600)

    plt.tight_layout()
    st.pyplot(fig)

# =====================================================
# 7. TIEMPOS DE ESPERA
# =====================================================
st.markdown('<div class="section-title">Tiempos de Espera por Tipo de Consulta</div>', unsafe_allow_html=True)

tiempos_espera = resultados.get("tiempos_espera", {})
if tiempos_espera:
    cols = st.columns(len(tiempos_espera))
    for idx, (tipo, tiempo) in enumerate(tiempos_espera.items()):
        nombre = tipo.replace("ATENDER CONSULTA ", "").replace("INVERSION", "Inversión").replace("PRESTAMO", "Préstamo").replace("PLAZO FIJO", "Plazo Fijo")
        with cols[idx]:
            st.markdown(f"""
            <div style="background:#f8f9fa; border-radius:8px; padding:0.8rem 1rem; border:1px solid #e0e0e0; text-align:center;">
                <div style="font-size:0.85rem; color:#6c6c8a; font-weight:500; text-transform:uppercase; letter-spacing:0.3px;">{nombre}</div>
                <div style="font-size:1.6rem; font-weight:600; color:#2d2d44;">{tiempo}</div>
                <div style="font-size:0.8rem; color:#6c6c8a;">días</div>
            </div>
            """, unsafe_allow_html=True)

# =====================================================
# 8. PROPUESTA DE REDISEÑO
# =====================================================
st.divider()
st.markdown('<div class="section-title">Propuesta de Rediseño</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="background:#f8fafc; border-radius:10px; padding:1.5rem; border:1px solid #e0e0e0; margin-bottom:1rem;">
    <div style="font-weight:600; font-size:1.1rem; color:#2b6cb0;">Problema identificado</div>
    <p>El recurso <strong>{recurso_bottleneck}</strong> está saturado al <strong>{utilizacion_bottleneck:.2f}%</strong>, generando tiempos de espera de <strong>2.8 días</strong> para los clientes de préstamos.</p>
</div>
""", unsafe_allow_html=True)

col_sol1, col_sol2 = st.columns([2, 1])

with col_sol1:
    st.markdown(f"""
    <div style="background:#f0fff4; border-radius:10px; padding:1.5rem; border:1px solid #c6f6d5;">
        <div style="font-weight:600; font-size:1.1rem; color:#2f855a;">Solución propuesta</div>
        <p style="margin-top:0.5rem;">Aplicando la heurística <strong>"Case assignment"</strong> del Capítulo 8 de Dumas et al. (2018):</p>
        <blockquote style="background:white; border-radius:6px; padding:0.8rem 1.2rem; border-left:4px solid #38a169; margin:0.5rem 0;">
            Agregar un segundo Administrativo de Préstamos (pasar de 1 a 2 recursos)
        </blockquote>
    </div>
    """, unsafe_allow_html=True)

with col_sol2:
    st.markdown("""
    <div style="background:#f0f7ff; border-radius:10px; padding:1.5rem; border:1px solid #bee3f8; height:100%;">
        <div style="font-weight:600; font-size:1.1rem; color:#2b6cb0;">Impacto esperado</div>
        <table style="width:100%; margin-top:0.5rem; border-collapse:collapse; font-size:0.95rem;">
            <tr><td style="padding:4px 0;"><strong>Time</strong></td><td style="padding:4px 0; color:#38a169;">✅ Reducción a ~1.2 días</td></tr>
            <tr><td style="padding:4px 0;"><strong>Cost</strong></td><td style="padding:4px 0; color:#d69e2e;">⚠️ +$5.800/hora</td></tr>
            <tr><td style="padding:4px 0;"><strong>Quality</strong></td><td style="padding:4px 0; color:#38a169;">✅ Mejora</td></tr>
            <tr><td style="padding:4px 0;"><strong>Flexibility</strong></td><td style="padding:4px 0; color:#38a169;">✅ Mayor resiliencia</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 9. CONCLUSIÓN
# =====================================================
st.divider()
st.markdown('<div class="section-title">Conclusión</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="success-card">
    <p style="margin:0; line-height:1.6;">
        El análisis cualitativo y cuantitativo del proceso de atención al cliente del Banco ABC 
        permitió identificar un <strong>cuello de botella en el Administrativo de Préstamos</strong> con 
        una utilización del <strong>{utilizacion_bottleneck:.2f}%</strong>.
    </p>
    <p style="margin:0.8rem 0 0 0; line-height:1.6;">
        La propuesta de rediseño consiste en agregar un segundo Administrativo de Préstamos, 
        lo que permitiría reducir el tiempo de espera de <strong>2.8 días a 1.2 días</strong> y mejorar la 
        satisfacción del cliente.
    </p>
    <p style="margin:0.8rem 0 0 0; line-height:1.6;">
        El costo total del proceso para 1000 clientes es de <strong>${resultados.get('costo_total', 0):,.2f}</strong> 
        con un costo promedio de <strong>${resultados.get('costo_promedio', 0):.2f}</strong> por cliente.
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown(f"""
<div class="footer">
    Simulación BPMN · Banco ABC · {resultados.get('instancias', 1000)} clientes · 6 meses
</div>
""", unsafe_allow_html=True)
