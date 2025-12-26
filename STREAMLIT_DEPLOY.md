# ⚽ Football Agent Simulator - Web Version

Interfaz web interactiva para el simulador de agente de fútbol, desplegable gratuitamente en Streamlit Cloud.

## 🌐 Deploy en Streamlit Cloud (GRATIS)

### Opción 1: Deploy Directo desde GitHub

1. Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
2. Haz login con tu cuenta de GitHub
3. Click en "New app"
4. Selecciona:
   - **Repository:** `maxielias/real-football-agent`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click "Deploy!"

¡Tu app estará disponible en una URL pública en menos de 2 minutos! 🚀

### Opción 2: Deploy Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la app
streamlit run app.py
```

La app se abrirá automáticamente en `http://localhost:8501`

## 📱 Características de la UI

### 🏠 Panel Principal

- Métricas en tiempo real (dinero, clientes, semana, acciones)
- Actividad reciente (transferencias, ofertas)
- Accesos rápidos a funciones principales

### 👤 Mis Clientes

- Lista completa con filtros (posición, estado)
- Detalles expandibles por jugador
- Estadísticas de temporada y últimos 5 partidos
- Información de contratos

### 📊 Estadísticas

- Top scorers (máximos goleadores)
- Top assists (máximos asistidores)
- Best ratings (mejores ratings)
- Promedios y comparativas

### 📝 Reportes Semanales

- Actuaciones de la semana
- Promesas activas con countdown
- Ofertas recibidas
- Rankings de mejores/peores performers

### 💼 Contratos

- Gestión de ofertas pendientes
- Aceptar/rechazar con un click
- Sistema de rescisión de contratos
- Cálculo automático de fees

### 🔍 Buscar Jugadores

- Catálogo completo de jugadores disponibles
- Filtros por posición, potencial
- Ordenamiento múltiple
- Firma con un click

### 🤝 Interacciones

- 5 tipos de interacciones con clientes
- Mejora de moral y confianza
- Feedback inmediato

### 📈 Liga

- Tabla de posiciones actualizada
- Estadísticas por equipo
- Partidos jugados, goles, puntos

### ⚙️ Acciones Especiales

- Plantar rumores en la prensa
- Hacer promesas de campaña
- Sistema de costos y riesgos

## 🎨 UI Features

✅ **Responsive** - Funciona en desktop, tablet y móvil
✅ **Session State** - Mantiene el estado del juego entre acciones
✅ **Real-time Updates** - Actualizaciones instantáneas
✅ **Custom Styling** - Cards, métricas, colores personalizados
✅ **Navigation** - Sidebar con navegación clara

## 🚀 Compartir tu App

Una vez desplegada en Streamlit Cloud:

1. Obtendrás una URL como: `https://yourapp.streamlit.app`
2. Comparte esa URL con quien quieras
3. ¡No necesitan instalar nada! Solo abrir el navegador

### Límites del Plan Gratuito

- ✅ Apps públicas ilimitadas
- ✅ 1GB de RAM por app
- ✅ Sin límite de usuarios
- ✅ Dominio personalizado disponible
- ⚠️ La app duerme después de inactividad (se reactiva al acceder)

## 📝 Estructura del Código

```
app.py                 # Aplicación principal Streamlit
├── render_sidebar()   # Barra lateral con navegación
├── render_home()      # Página principal
├── render_clients()   # Gestión de clientes
├── render_stats()     # Estadísticas detalladas
├── render_reports()   # Reportes semanales
├── render_contracts() # Ofertas y contratos
└── render_*()         # Otras páginas...

game.py                # Lógica del juego (backend)
player.py              # Clase Player
club.py                # Clase Club
agent.py               # Clase Agent
game_data.py           # Datos del juego
```

## 🔧 Personalización

### Cambiar Tema

Edita `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"      # Color principal
backgroundColor = "#0E1117"    # Fondo (dark mode)
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
```

### Agregar Funcionalidades

1. Abre `app.py`
2. Crea una nueva función `render_nueva_feature()`
3. Agrégala al menú en `render_sidebar()`
4. Añade el routing en `main()`

## 🐛 Troubleshooting

**Error: "ModuleNotFoundError"**

- Asegúrate de que `requirements.txt` esté completo
- En Streamlit Cloud, click "Manage app" → "Reboot"

**La app no guarda el progreso**

- Streamlit usa session state volátil
- Para persistencia, implementa save/load con archivos

**La app es lenta**

- Verifica el límite de RAM (1GB en free tier)
- Optimiza bucles y cálculos pesados

## 📧 Soporte

¿Problemas con el deploy? Revisa la [documentación de Streamlit](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

## 🎮 ¡Disfruta del Juego!

Una vez desplegado, comparte la URL y que otros disfruten de tu simulador de agente de fútbol. ⚽🎉
