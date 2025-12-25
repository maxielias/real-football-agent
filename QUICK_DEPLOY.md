# 🚀 Guía Rápida de Deploy

## ⚡ Deploy en 3 Pasos (2 minutos)

### 1️⃣ Ve a Streamlit Cloud

```
https://streamlit.io/cloud
```

### 2️⃣ Login con GitHub

- Click en "Sign in with GitHub"
- Autoriza Streamlit

### 3️⃣ Deploy la App

- Click en "New app"
- Selecciona:
  - **Repository:** `maxielias/real-football-agent`
  - **Branch:** `main`
  - **Main file path:** `app.py`
- Click "Deploy!"

## ✅ ¡Listo!

Tu app estará disponible en una URL pública como:

```
https://real-football-agent-xxx.streamlit.app
```

Comparte esa URL con quien quieras. ¡No necesitan instalar nada!

## 📱 Alternativa: Ejecutar Local

```bash
# Instalar
pip install streamlit

# Ejecutar
streamlit run app.py
```

Abre tu navegador en `http://localhost:8501`

## 💡 Tips

- **La app duerme después de inactividad:** Se reactiva automáticamente al acceder
- **Gratis e ilimitado:** Sin límite de usuarios ni tiempo
- **Actualización automática:** Cada push a `main` actualiza la app
- **Custom domain:** Puedes configurar tu propio dominio

## 🎮 ¡Disfruta!

Una vez deployada, cualquiera puede:

- ✅ Jugar desde el navegador
- ✅ Sin instalar Python
- ✅ Sin dependencias
- ✅ En cualquier dispositivo

---

**¿Problemas?** Lee [STREAMLIT_DEPLOY.md](./STREAMLIT_DEPLOY.md) para más detalles
