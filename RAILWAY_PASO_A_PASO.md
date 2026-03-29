# 🚂 GUÍA PASO A PASO - RAILWAY.APP

## ⏱️ **TIEMPO ESTIMADO: 10 MINUTOS**

---

## 📦 **PASO 1: PREPARAR ARCHIVOS (2 min)**

Necesitas estos 4 archivos en una carpeta:

### **1. bot_alerts_HOSTING.py** ⭐
```
El bot modificado para usar variables de entorno
✅ Ya lo tienes - descárgalo arriba
```

### **2. requirements.txt**
```
ccxt>=4.0.0
pandas>=2.0.0
numpy>=1.24.0
schedule>=1.2.0
requests>=2.31.0
```

### **3. Procfile** (sin extensión)
```
worker: python bot_alerts_HOSTING.py
```

### **4. railway.json**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python bot_alerts_HOSTING.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**✅ Todos estos archivos están arriba ⬆️ para descargar**

---

## 🐙 **PASO 2: SUBIR A GITHUB (3 min)**

### **Opción A: Desde la web (MÁS FÁCIL)** ⭐

#### **1. Crear cuenta GitHub**
```
1. Ve a github.com
2. Sign up (gratis)
3. Confirma email
```

#### **2. Crear repositorio**
```
1. Click "+" arriba derecha → New repository
2. Nombre: trading-bot
3. Descripción: ICT 2022 Trading Bot
4. ✅ Public (o Private, ambos funcionan)
5. ✅ Add a README file
6. Create repository
```

#### **3. Subir archivos**
```
1. En tu repositorio → Add file → Upload files
2. Arrastra los 4 archivos:
   - bot_alerts_HOSTING.py
   - requirements.txt
   - Procfile
   - railway.json
3. Commit changes (abajo)
```

### **Opción B: Desde Git (Avanzado)**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/trading-bot.git
git push -u origin main
```

**✅ Archivos en GitHub - Listo para deploy**

---

## 🚂 **PASO 3: CONFIGURAR RAILWAY (3 min)**

### **1. Crear cuenta Railway**
```
1. Ve a railway.app
2. Login with GitHub
3. Autoriza Railway a acceder a GitHub
4. ✅ Cuenta creada
```

### **2. Nuevo proyecto**
```
1. Dashboard → New Project
2. Deploy from GitHub repo
3. Selecciona: trading-bot
4. Deploy Now
```

### **3. Railway detecta Python automáticamente**
```
Railway verá:
- requirements.txt → Instala dependencias
- Procfile → Sabe cómo ejecutar
- railway.json → Configuración custom

✅ Todo automático
```

---

## ⚙️ **PASO 4: CONFIGURAR VARIABLES (2 min)**

**MUY IMPORTANTE:** No pongas credenciales en el código público.

### **En Railway:**

```
1. Tu proyecto → Settings
2. Variables
3. New Variable
```

### **Agregar estas variables:**

```
Variable 1:
Name: TELEGRAM_BOT_TOKEN
Value: 7614545129:AAEo6aOQbU0ia_5etD9N0YSvZG7H0dYuLG4

Variable 2:
Name: TELEGRAM_CHAT_ID
Value: 890173331

Variable 3 (opcional):
Name: BALANCE
Value: 900

Variable 4 (opcional):
Name: RISK
Value: moderate
```

### **Guardar:**
```
Save Variables → Redeploy automático
```

**✅ Credenciales seguras**

---

## ✅ **PASO 5: VERIFICAR FUNCIONAMIENTO (2 min)**

### **1. Ver logs en tiempo real**
```
1. Tu proyecto → Deployments
2. Click en el deployment activo
3. View Logs
```

### **2. Deberías ver:**
```
================================================================================
ICT 2022 BOT - VERSIÓN HOSTING
================================================================================
Configuración cargada - Balance: $900, Risk: moderate
Bot Robusto iniciado
Balance: $900
Activos: 5
Timeframes: 4H

INICIANDO BOT EN HOSTING
Escaneos automáticos cada hora

Ejecutando primer escaneo...

ESCANEO - 2026-03-29 15:00:00
Analizando 5 activos...

Exitosos: 5, Fallidos: 0, Alertas: 0
No hay señales en este escaneo
Escaneo completado

Próximo escaneo: 16:00
```

### **3. Verificar Telegram**
```
- Espera al siguiente escaneo (cada hora)
- O espera a que encuentre una señal
- Deberías recibir alerta en Telegram
```

**✅ SI VES ESTO - ¡TODO FUNCIONA!**

---

## 📊 **MONITOREAR EL BOT**

### **Ver logs:**
```
Railway → Tu proyecto → Deployments → View Logs
```

### **Ver uso de recursos:**
```
Railway → Tu proyecto → Metrics
```

### **Ver cuánto has gastado:**
```
Railway → Account → Usage
Deberías ver: $0.50-1.00/mes
Crédito restante: ~$4/mes
```

---

## 🔄 **ACTUALIZAR EL BOT**

Si haces cambios:

### **Método 1: Desde GitHub (automático)**
```
1. Edita archivo en GitHub
2. Commit changes
3. Railway detecta cambio
4. Redeploy automático
5. ✅ Bot actualizado
```

### **Método 2: Manual redeploy**
```
1. Railway → Proyecto → Deployments
2. Click ⋮ (tres puntos)
3. Redeploy
```

---

## ⚠️ **PROBLEMAS COMUNES**

### **"Build failed"**
```
Causa: requirements.txt mal formateado
Solución:
1. Verifica que no tenga espacios extra
2. Cada librería en una línea
3. Sin líneas vacías al final
```

### **"Application error - Environment variable missing"**
```
Causa: Falta TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID
Solución:
1. Railway → Settings → Variables
2. Agregar las variables
3. Redeploy
```

### **"Bot no envía alertas"**
```
Posibles causas:
1. Variables de entorno incorrectas
2. Bot Token inválido
3. Chat ID incorrecto
4. No hay señales (normal)

Verificar:
1. Logs muestran "Bot iniciado"?
2. Logs muestran "Escaneo completado"?
3. Prueba enviando /start a tu bot
```

### **"Exceeded credit limit"**
```
Causa: Usaste más de $5
Solución:
- Poco probable con este bot
- Verifica Metrics
- Agrega tarjeta para continuar
```

---

## 💰 **COSTOS Y LÍMITES**

### **Crédito mensual:**
```
Railway te da: $5/mes gratis
Tu bot usa: ~$0.50-1/mes
Sobra: ~$4/mes
```

### **¿Qué pasa cuando se acaba?**
```
1. Railway te avisa por email
2. Bot se detiene
3. Opciones:
   - Agregar tarjeta (se cobra desde $5.01)
   - Esperar al siguiente mes (se renueva)
```

### **Para evitar sorpresas:**
```
Railway → Settings → Usage Limits
Set limit: $5
```

---

## 🎯 **CHECKLIST FINAL**

```
□ Archivos subidos a GitHub
□ Proyecto creado en Railway
□ Variables de entorno configuradas
□ Deploy exitoso
□ Logs muestran bot corriendo
□ Primer escaneo completado
□ Recibo alertas en Telegram (cuando hay señales)
□ ✅ ¡Bot funcionando 24/7!
```

---

## 🎉 **¡FELICIDADES!**

Tu bot ahora:
- ✅ Corre 24/7 en la nube
- ✅ No depende de tu PC
- ✅ Escanea mercado cada hora
- ✅ Envía alertas a Telegram
- ✅ Gratis ($5 crédito mensual)
- ✅ Logs monitoreables
- ✅ Actualizable desde GitHub

---

## 📱 **PRÓXIMOS PASOS**

### **Opcional - Mejoras:**

1. **Agregar más activos:**
   ```python
   self.watchlist = [
       'BTC/USDT', 'ETH/USDT', 'BNB/USDT',
       'SOL/USDT', 'XRP/USDT', 'ADA/USDT'  # Nuevo
   ]
   ```

2. **Cambiar timeframes:**
   ```python
   self.timeframes = ['1h', '4h']  # Añadir 1H
   ```

3. **Ajustar probabilidad mínima:**
   ```python
   self.min_probability = 75  # Más conservador
   ```

Edita en GitHub → Railway redeploy automático

---

## 🆘 **SOPORTE**

**Si algo falla:**

1. **Ver logs en Railway**
   - Busca líneas con "ERROR"
   - Copia el error completo

2. **Verificar variables**
   - Settings → Variables
   - Están todas?
   - Valores correctos?

3. **Redeploy manual**
   - A veces soluciona problemas temporales

---

**¿Todo listo? ¡Tu bot está en la nube funcionando 24/7!** 🚀
