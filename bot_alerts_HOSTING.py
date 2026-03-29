#!/usr/bin/env python3
"""
ICT 2022 BOT - VERSIÓN PARA HOSTING
Optimizado para Railway/Render con variables de entorno
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import schedule
import logging
import os
import traceback

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ==========================================
# CONFIGURACIÓN DESDE VARIABLES DE ENTORNO
# ==========================================
BALANCE = int(os.environ.get('BALANCE', '900'))
RISK = os.environ.get('RISK', 'moderate')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Validar que las credenciales existen
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    logger.error("ERROR: Faltan variables de entorno TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID")
    logger.error("Configúralas en Railway/Render Settings → Variables")
    exit(1)

logger.info(f"Configuración cargada - Balance: ${BALANCE}, Risk: {RISK}")
# ==========================================


class RobustICTBot:
    """Bot ICT con manejo robusto de errores"""
    
    def __init__(self, balance=900, risk='moderate', telegram_token=None, chat_id=None):
        # Exchange
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'timeout': 30000,
            'options': {'defaultType': 'spot'}
        })
        
        self.balance = balance
        self.risk_tolerance = risk
        self.bot_token = telegram_token
        self.main_chat_id = chat_id
        
        # Configuración
        self.min_probability = 70
        self.timeframes = ['4h']
        self.watchlist = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT']
        
        # Tracking
        self.sent_alerts = set()
        self.failed_symbols = {}
        
        logger.info("Bot Robusto iniciado")
        logger.info(f"Balance: ${balance}")
        logger.info(f"Activos: {len(self.watchlist)}")
        logger.info(f"Timeframes: {', '.join([tf.upper() for tf in self.timeframes])}")
    
    def fetch_safe_ohlcv(self, symbol, timeframe, limit=100):
        """Obtener datos OHLCV con manejo de errores"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            if not ohlcv or len(ohlcv) < 50:
                return None
            
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            return df
            
        except Exception as e:
            logger.error(f"Error obteniendo datos para {symbol}: {e}")
            return None
    
    def simple_analysis(self, df, symbol, timeframe, current_price):
        """Análisis simplificado"""
        try:
            high_20 = df['high'].tail(20).max()
            low_20 = df['low'].tail(20).min()
            
            df['sma_20'] = df['close'].rolling(20).mean()
            df['sma_50'] = df['close'].rolling(50).mean()
            
            sma_20 = df.iloc[-1]['sma_20']
            sma_50 = df.iloc[-1]['sma_50']
            
            if current_price > sma_20 > sma_50:
                bias = 'bullish'
                bias_strength = 70
            elif current_price < sma_20 < sma_50:
                bias = 'bearish'
                bias_strength = 70
            else:
                bias = 'neutral'
                bias_strength = 50
            
            signals = []
            
            distance_to_low = abs(current_price - low_20) / current_price * 100
            if distance_to_low < 1 and bias == 'bullish':
                atr = (df['high'] - df['low']).tail(14).mean()
                signals.append({
                    'type': 'SUPPORT_BOUNCE',
                    'direction': 'long',
                    'entry': current_price,
                    'sl': low_20 * 0.995,
                    'tp': current_price + (atr * 2),
                    'probability': 72,
                    'priority': 'MEDIUM',
                    'reason': f'Price near support with {bias} bias'
                })
            
            distance_to_high = abs(current_price - high_20) / current_price * 100
            if distance_to_high < 1 and bias == 'bearish':
                atr = (df['high'] - df['low']).tail(14).mean()
                signals.append({
                    'type': 'RESISTANCE_REJECTION',
                    'direction': 'short',
                    'entry': current_price,
                    'sl': high_20 * 1.005,
                    'tp': current_price - (atr * 2),
                    'probability': 72,
                    'priority': 'MEDIUM',
                    'reason': f'Price near resistance with {bias} bias'
                })
            
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'current_price': current_price,
                'bias': bias,
                'bias_strength': bias_strength,
                'signals': signals
            }
            
        except Exception as e:
            logger.error(f"Error en análisis: {e}")
            return None
    
    def analyze_symbol_safe(self, symbol, timeframe):
        """Analizar símbolo con manejo de errores"""
        try:
            df = self.fetch_safe_ohlcv(symbol, timeframe, limit=100)
            
            if df is None or len(df) < 50:
                return None
            
            current_price = df.iloc[-1]['close']
            result = self.simple_analysis(df, symbol, timeframe, current_price)
            
            return result
            
        except Exception as e:
            logger.error(f"Error analizando {symbol}: {str(e)}")
            self.failed_symbols[symbol] = self.failed_symbols.get(symbol, 0) + 1
            return None
    
    def send_telegram_alert(self, setup):
        """Enviar alerta por Telegram"""
        signal = setup['signal']
        emoji = "🟢" if signal['direction'] == 'long' else "🔴"
        
        message = f"""
{emoji} <b>SEÑAL DETECTADA</b> {emoji}

<b>Asset:</b> {setup['symbol']}
<b>Timeframe:</b> {setup['timeframe'].upper()}
<b>Dirección:</b> {signal['direction'].upper()}
<b>Precio Actual:</b> ${setup['current_price']:,.4f}

<b>📊 SETUP:</b>
• Type: {signal['type']}
• Priority: {signal['priority']}
• Probability: <b>{signal['probability']:.0f}%</b>

<b>💰 TRADE:</b>
• Entry: ${signal['entry']:,.4f}
• SL: ${signal['sl']:,.4f}
• TP: ${signal['tp']:,.4f}
• R:R: {abs(signal['tp'] - signal['entry']) / abs(signal['entry'] - signal['sl']):.2f}:1

<b>📈 BIAS:</b> {setup['bias'].upper()} ({setup['bias_strength']:.0f}%)
<b>⏰:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        try:
            import requests
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.main_chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logger.info("Alerta enviada por Telegram")
                return True
            else:
                logger.error(f"Error Telegram: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error enviando Telegram: {e}")
            return False
    
    def scan_market(self):
        """Escanear mercado"""
        logger.info(f"\nESCANEO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        all_alerts = []
        successful_scans = 0
        failed_scans = 0
        
        active_watchlist = [
            s for s in self.watchlist 
            if self.failed_symbols.get(s, 0) < 3
        ]
        
        logger.info(f"Analizando {len(active_watchlist)} activos...")
        
        for symbol in active_watchlist:
            for tf in self.timeframes:
                try:
                    result = self.analyze_symbol_safe(symbol, tf)
                    
                    if result:
                        successful_scans += 1
                        
                        if result.get('signals'):
                            for signal in result['signals']:
                                if signal['probability'] >= self.min_probability:
                                    alert_data = {
                                        'symbol': symbol,
                                        'timeframe': tf,
                                        'current_price': result['current_price'],
                                        'bias': result['bias'],
                                        'bias_strength': result['bias_strength'],
                                        'signal': signal
                                    }
                                    all_alerts.append(alert_data)
                    else:
                        successful_scans += 1
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    failed_scans += 1
                    logger.error(f"Error escaneando {symbol}: {e}")
                    continue
        
        logger.info(f"Exitosos: {successful_scans}, Fallidos: {failed_scans}, Alertas: {len(all_alerts)}")
        
        if all_alerts:
            logger.info(f"Enviando {len(all_alerts)} alertas...")
            for alert in all_alerts:
                self.send_telegram_alert(alert)
                time.sleep(1)
        else:
            logger.info("No hay señales en este escaneo")
        
        logger.info("Escaneo completado")
    
    def start_scheduler(self):
        """Iniciar scheduler"""
        logger.info("INICIANDO BOT EN HOSTING")
        logger.info("Escaneos automáticos cada hora")
        
        # Primer escaneo
        logger.info("Ejecutando primer escaneo...")
        self.scan_market()
        
        # Programar cada hora
        schedule.every().hour.at(":00").do(self.scan_market)
        
        logger.info(f"Próximo escaneo: {(datetime.now() + timedelta(hours=1)).strftime('%H:%M')}")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Bot detenido")


def main():
    """Función principal"""
    logger.info("="*80)
    logger.info("ICT 2022 BOT - VERSIÓN HOSTING")
    logger.info("="*80)
    
    # Crear y ejecutar bot
    bot = RobustICTBot(
        balance=BALANCE,
        risk=RISK,
        telegram_token=TELEGRAM_BOT_TOKEN,
        chat_id=TELEGRAM_CHAT_ID
    )
    
    bot.start_scheduler()


if __name__ == "__main__":
    main()
