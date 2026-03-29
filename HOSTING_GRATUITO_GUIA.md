# 🌐 GUÍA COMPLETA - HOSTING GRATUITO PARA EL BOT

## 🎯 **MEJORES OPCIONES GRATUITAS (2026)**

---

## 🥇 **OPCIÓN 1: RAILWAY.APP** ⭐ (MÁS RECOMENDADA)

### **✅ VENTAJAS:**
- Setup super fácil (5-10 minutos)
- $5 USD gratis al mes (suficiente para el bot)
- Despliegue automático desde GitHub
- Logs en tiempo real
- Muy fácil de usar

### **❌ LIMITACIONES:**
- Requiere tarjeta de crédito (no se cobra si no excedes $5)
- $5/mes de crédito gratis (se renueva cada mes)

### **📋 PASOS:**

#### **1. Preparar archivos**

Necesitas 3 archivos en tu carpeta:

**Archivo 1: `requirements.txt`**
```
ccxt>=4.0.0
pandas>=2.0.0
numpy>=1.24.0
python-telegram-bot>=20.0
schedule>=1.2.0
requests>=2.31.0
colorama>=0.4.6
```

**Archivo 2: `Procfile`** (sin extensión .txt)
```
worker: python bot_alerts_ROBUSTO.py
```

**Archivo 3: `railway.json`**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python bot_alerts_ROBUSTO.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### **2. Crear cuenta GitHub**

```
1. Ve a github.com
2. Crea cuenta gratis
3. Crea nuevo repositorio: "trading-bot"
4. Haz público o privado
```

#### **3. Subir archivos a GitHub**

**Opción A: Desde web (más fácil)**
```
1. En tu repositorio → Add file → Upload files
2. Arrastra:
   - bot_alerts_ROBUSTO.py
   - requirements.txt
   - Procfile
   - railway.json
3. Commit changes
```

**Opción B: Desde Git (avanzado)**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU_USUARIO/trading-bot.git
git push -u origin main
```

#### **4. Desplegar en Railway**

```
1. Ve a railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub repo
4. Selecciona tu repositorio "trading-bot"
5. Railway detecta Python automáticamente
6. Click "Deploy"
7. ¡Espera 2-3 minutos!
```

#### **5. Verificar funcionamiento**

```
1. En Railway → tu proyecto → Deployments
2. Click en el deployment activo
3. Ver "Logs" → Deberías ver el bot ejecutándose
4. Verifica en Telegram que recibes alertas
```

**✅ ¡LISTO! Bot corriendo 24/7 gratis**

---

## 🥈 **OPCIÓN 2: RENDER.COM** (ALTERNATIVA EXCELENTE)

### **✅ VENTAJAS:**
- 750 horas gratis al mes (suficiente para 24/7)
- No requiere tarjeta de crédito
- Deploy desde GitHub
- Muy estable

### **❌ LIMITACIONES:**
- Se suspende después de 15 min inactivo (pero se reactiva)
- Para 24/7 SIN suspensión: $7/mes

### **📋 PASOS:**

#### **1. Archivos necesarios**

Mismos que Railway + adicional:

**render.yaml**
```yaml
services:
  - type: worker
    name: trading-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot_alerts_ROBUSTO.py
    plan: free
```

#### **2. Subir a GitHub**

(Mismo proceso que Railway)

#### **3. Desplegar en Render**

```
1. Ve a render.com
2. Sign up with GitHub
3. New → Background Worker
4. Connect tu repositorio
5. Name: trading-bot
6. Build Command: pip install -r requirements.txt
7. Start Command: python bot_alerts_ROBUSTO.py
8. Plan: Free
9. Create Web Service
```

**✅ ¡Bot corriendo!**

**⚠️ NOTA:** El plan free se suspende tras 15 min de inactividad. Para evitarlo:
- Upgrade a plan paid ($7/mes)
- O usar Railway que no suspende

---

## 🥉 **OPCIÓN 3: PYTHONANYWHERE** (ESPECÍFICO PARA PYTHON)

### **✅ VENTAJAS:**
- Diseñado específicamente para Python
- Plan gratuito decente
- Muy fácil de usar
- No requiere tarjeta

### **❌ LIMITACIONES:**
- Plan gratuito: Solo 1 proceso en background
- CPU limitada
- Debe "tocar" el archivo cada 3 meses

### **📋 PASOS:**

#### **1. Crear cuenta**

```
1. Ve a pythonanywhere.com
2. Sign up → Beginner (Free)
3. Confirma email
```

#### **2. Subir archivos**

```
1. Dashboard → Files
2. Upload: bot_alerts_ROBUSTO.py
3. Upload: requirements.txt
```

#### **3. Instalar dependencias**

```
1. Dashboard → Consoles → Bash
2. Ejecutar:
   pip3 install --user -r requirements.txt
```

#### **4. Crear tarea programada**

```
1. Dashboard → Tasks
2. Schedule: @hourly
3. Command: python3 /home/TU_USUARIO/bot_alerts_ROBUSTO.py
4. Save
```

**⚠️ LIMITACIÓN:** Solo ejecuta cada hora, no mantiene proceso corriendo

**Solución:** Modificar bot para ejecutar una vez y terminar:

```python
# Al final de bot_alerts_ROBUSTO.py
if __name__ == "__main__":
    # En vez de loop infinito
    bot = RobustICTBot(...)
    bot.scan_market()  # Ejecuta una vez y termina
    # PythonAnywhere lo ejecutará cada hora
```

---

## 🆓 **OPCIÓN 4: REPLIT** (PARA PRUEBAS)

### **✅ VENTAJAS:**
- Totalmente gratis
- Editor online
- Muy fácil

### **❌ LIMITACIONES:**
- Se suspende si no hay actividad
- Requiere "keep alive" con pings
- No recomendado para producción

### **📋 PASOS:**

```
1. Ve a replit.com
2. Create Repl → Python
3. Pega tu código
4. Install packages (botón)
5. Run
```

**Para mantenerlo vivo:**
- Necesitas hacer ping cada 5 min desde otro servicio
- Complicado y poco confiable
- ❌ No recomendado

---

## 🏆 **COMPARACIÓN**

| Hosting | Gratis | 24/7 | Fácil | Recomendación |
|---------|--------|------|-------|---------------|
| **Railway.app** | ✅ ($5/mes) | ✅ | ⭐⭐⭐⭐⭐ | 🥇 MEJOR |
| **Render.com** | ✅ | ⚠️* | ⭐⭐⭐⭐ | 🥈 Buena |
| **PythonAnywhere** | ✅ | ⚠️** | ⭐⭐⭐ | 🥉 OK |
| **Replit** | ✅ | ❌ | ⭐⭐ | ❌ No |

*Render: Se suspende tras 15 min inactividad (plan free)
**PythonAnywhere: Solo tareas programadas, no proceso continuo

---

## 🎯 **MI RECOMENDACIÓN FINAL**

### **MEJOR OPCIÓN: RAILWAY.APP** ⭐⭐⭐⭐⭐

**Por qué:**
```
✅ $5 gratis al mes (tu bot usa ~$0.50-1/mes)
✅ No se suspende nunca
✅ Super fácil de configurar
✅ Deploy automático desde GitHub
✅ Logs en tiempo real
✅ Funciona 24/7 sin problemas
```

**Único "pero":**
- Requiere tarjeta de crédito (pero NO se cobra nada si usas menos de $5)

**Alternativa si no quieres poner tarjeta:**
- **Render.com** - Gratis pero se suspende
- **PythonAnywhere** - Gratis pero solo ejecuciones por hora

---

## 🚀 **SETUP RÁPIDO EN RAILWAY (RECOMENDADO)**

### **Tiempo estimado: 10 minutos**

```
□ Paso 1: Crear cuenta GitHub (2 min)
□ Paso 2: Crear repositorio (1 min)
□ Paso 3: Subir archivos (2 min)
□ Paso 4: Cuenta Railway con GitHub (1 min)
□ Paso 5: Deploy desde repo (2 min)
□ Paso 6: Verificar logs (2 min)
□ ✅ ¡Bot corriendo 24/7!
```

---

## ⚠️ **IMPORTANTE ANTES DE SUBIR**

### **Proteger credenciales:**

**❌ NUNCA subas esto a GitHub público:**
```python
TELEGRAM_BOT_TOKEN = "7614545129:AAEo6aOQbU0ia_5etD9N0YSvZG7H0dYuLG4"
TELEGRAM_CHAT_ID = "890173331"
```

**✅ USA variables de entorno:**

1. En Railway/Render → Settings → Variables
2. Agregar:
   ```
   TELEGRAM_BOT_TOKEN = 7614545129:AAEo6aOQbU0ia_5etD9N0YSvZG7H0dYuLG4
   TELEGRAM_CHAT_ID = 890173331
   ```

3. En tu código:
   ```python
   import os
   
   TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
   TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
   ```

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### **Bot no arranca en Railway**
```
1. Ver Logs en Railway
2. Verificar requirements.txt está completo
3. Verificar Procfile tiene "worker:" no "web:"
4. Redeploy
```

### **Bot se suspende en Render**
```
Causa: Plan free se suspende
Solución: 
- Upgrade a paid ($7/mes)
- O usar Railway
```

### **Error al instalar dependencias**
```
Verificar requirements.txt:
- Sin espacios extras
- Versiones compatibles
- Formato correcto
```

---

## 💰 **COSTOS REALES**

### **Railway (Recomendado):**
```
Gratis: $5/mes de crédito
Tu bot usa: ~$0.50-1/mes
Sobra: $4/mes para otros proyectos
Costo real: $0 (mientras no excedas $5)
```

### **Render:**
```
Free plan: Gratis pero se suspende
Paid plan: $7/mes sin suspensión
```

### **PythonAnywhere:**
```
Free: Totalmente gratis
Limitación: Solo ejecuciones programadas
```

---

## ✅ **CHECKLIST FINAL**

```
□ Creé archivos: requirements.txt, Procfile
□ Subí código a GitHub
□ Creé cuenta en Railway/Render
□ Configuré variables de entorno
□ Deploy exitoso
□ Verifico logs - bot corriendo
□ Recibo alertas en Telegram
□ ✅ ¡Bot 24/7 funcionando!
```

---

**¿Quieres que te cree los archivos necesarios para Railway?** 

**Es la opción más fácil y funciona perfecto.** 🚀
