import streamlit as st
import folium
from streamlit_folium import folium_static
from a_star import pathfinder, CUENCA_NODES

# ================================
# CONFIGURACIÓN DE LA PÁGINA
# ================================
st.set_page_config(
    page_title="Ruta Óptima - Cuenca",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🗺️"
)

# ================================
# ESTILOS CSS PERSONALIZADOS
# ================================
st.markdown("""
    <style>
    /* Estilo del título principal */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Subtítulo */
    .subtitle {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Tarjetas de información */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Tarjeta de ruta mejorada */
    .route-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin: 1.5rem 0;
    }
    
    .route-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .route-path {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.75rem;
        padding: 1rem;
        background: #f9fafb;
        border-radius: 8px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .route-node {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.95rem;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
    }
    
    .route-arrow {
        color: #9ca3af;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Botón personalizado */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    /* Selectbox mejorado */
    .stSelectbox label {
        font-weight: 600;
        color: #1f2937;
        font-size: 1rem;
    }
    
    /* Espaciado */
    .spacer {
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ================================
# ENCABEZADO
# ================================
st.markdown('<h1 class="main-title">🗺️ Sistema de Rutas Óptimas - Cuenca</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Encuentra la ruta más eficiente entre dos puntos utilizando el algoritmo A*</p>', unsafe_allow_html=True)

# ================================
# BARRA LATERAL CON INFORMACIÓN
# ================================
with st.sidebar:
    st.markdown("### 📍 Acerca del Sistema")
    st.markdown("""
    Este sistema utiliza el **algoritmo A*** para calcular 
    la ruta más corta entre dos puntos en la ciudad de Cuenca.
    
    **Características:**
    - 🎯 Búsqueda optimizada
    - 📊 Visualización interactiva
    - 🗺️ Mapa en tiempo real
    - 📈 Métricas detalladas
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎨 Leyenda del Mapa")
    st.markdown("""
    - 🔵 **Azul:** Punto de inicio
    - 🔴 **Rojo:** Punto de destino
    - 🟢 **Verde:** Nodos disponibles
    - 🟣 **Línea púrpura:** Ruta calculada
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ Información")
    st.markdown("**Versión:** 1.0.0")
    st.markdown("**Algoritmo:** A* (A-Star)")

# ================================
# CONTENIDO PRINCIPAL
# ================================
nodos = sorted(list(CUENCA_NODES.keys()))

# Panel de control en tarjeta
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
st.markdown("## 🎯 Configuración de Ruta")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    start = st.selectbox(
        "🚩 Punto de Inicio",
        nodos,
        index=0,
        help="Selecciona el nodo desde donde comenzará la ruta"
    )

with col2:
    goal = st.selectbox(
        "🏁 Punto de Destino",
        nodos,
        index=min(1, len(nodos)-1),
        help="Selecciona el nodo donde terminará la ruta"
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    calcular = st.button("🚗 Calcular Ruta", type="primary", use_container_width=True)

# ================================
# PROCESAMIENTO Y VISUALIZACIÓN
# ================================
if calcular:
    if start == goal:
        st.error("⚠️ **Error:** El punto de inicio y destino deben ser diferentes.")
    else:
        with st.spinner("🔄 Calculando la mejor ruta..."):
            path, total_dist, explorados = pathfinder.find_path(start, goal)
        
        if path:
            # Métricas en tarjetas
            st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
            st.markdown("## 📊 Resultados del Análisis")
            
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Distancia Total</div>
                    <div class="metric-value">{total_dist:.2f} km</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Nodos en Ruta</div>
                    <div class="metric-value">{len(path)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Nodos Explorados</div>
                    <div class="metric-value">{explorados}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Ruta detallada MEJORADA
            st.markdown("### 🛣️ Itinerario de la Ruta")
            
            # Crear el HTML de la ruta con nodos individuales
            route_nodes_html = ""
            for i, nodo in enumerate(path):
                route_nodes_html += f'<span class="route-node">{nodo}</span>'
                if i < len(path) - 1:
                    route_nodes_html += '<span class="route-arrow">→</span>'
            
            st.markdown(f"""
            <div class="route-card">
                <div class="route-title">
                    <span>📍</span>
                    <span>Secuencia de Puntos de Paso</span>
                </div>
                <div class="route-path">
                    {route_nodes_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Mapa
            st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
            st.markdown("## 🗺️ Visualización del Mapa")
            
            # Crear mapa
            mapa = folium.Map(
                location=[-2.8975, -79.005],
                zoom_start=14,
                tiles='OpenStreetMap'
            )
            
            # Agregar nodos
            for nodo, data in CUENCA_NODES.items():
                if nodo == start:
                    color, icon = "blue", "play"
                elif nodo == goal:
                    color, icon = "red", "stop"
                else:
                    color, icon = "green", "info-sign"
                
                folium.Marker(
                    [data["lat"], data["lon"]],
                    popup=folium.Popup(
                        f"<b style='font-size:14px'>{nodo}</b><br>{data['descripcion']}",
                        max_width=200
                    ),
                    tooltip=nodo,
                    icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
                ).add_to(mapa)
            
            # Dibujar ruta
            route_coords = [(CUENCA_NODES[n]["lat"], CUENCA_NODES[n]["lon"]) for n in path]
            folium.PolyLine(
                route_coords,
                color="#764ba2",
                weight=6,
                opacity=0.8,
                tooltip="Ruta calculada"
            ).add_to(mapa)
            
            # Mostrar mapa
            folium_static(mapa, width=1200, height=600)
            
            # Información adicional expandible
            with st.expander("📋 Ver información detallada de los nodos"):
                for i, nodo in enumerate(path, 1):
                    data = CUENCA_NODES[nodo]
                    st.markdown(f"""
                    **{i}. {nodo}**
                    - 📍 Coordenadas: ({data['lat']:.6f}, {data['lon']:.6f})
                    - 📝 {data['descripcion']}
                    """)
        else:
            st.error("❌ **No se encontró una ruta** entre los puntos seleccionados.")
            st.info("💡 **Sugerencia:** Intenta seleccionar otros puntos o verifica la conectividad de los nodos.")

# Footer
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6b7280;'>Desarrollado por Maura Calle usando Streamlit y Folium | © 2025</p>",
    unsafe_allow_html=True
)
