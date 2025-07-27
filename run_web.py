#!/usr/bin/env python3
"""
Скрипт для запуска веб-интерфейса Product Namer Agent.
"""
import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def check_environment():
    """Проверяет настройки окружения."""
    print("🔍 Проверка настроек окружения...")
    
    api_key = os.getenv("PROXY_API_KEY")
    api_base = os.getenv("PROXY_API_BASE")
    
    if not api_key:
        print("❌ Ошибка: PROXY_API_KEY не найден в .env файле")
        print("💡 Создайте файл .env с содержимым:")
        print("   PROXY_API_KEY=your_proxy_api_key_here")
        print("   PROXY_API_BASE=https://api.proxyapi.ru/openai/v1")
        return False
    
    if not api_base:
        print("❌ Ошибка: PROXY_API_BASE не найден в .env файле")
        return False
    
    print("✅ Настройки окружения корректны")
    return True


def main():
    """Основная функция запуска."""
    print("🚀 Product Namer Agent - Веб-интерфейс")
    print("=" * 50)
    
    # Проверяем настройки
    if not check_environment():
        sys.exit(1)
    
    try:
        # Импортируем и запускаем веб-приложение
        from web_app import app
        
        print("✅ Веб-приложение готово к запуску!")
        print("🌐 Откройте браузер и перейдите по адресу: http://localhost:5000")
        print("📱 Приложение также доступно по адресу: http://127.0.0.1:5000")
        print()
        print("💡 Для остановки сервера нажмите Ctrl+C")
        print("=" * 50)
        
        # Запускаем приложение
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Убедитесь, что установлены все зависимости:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 