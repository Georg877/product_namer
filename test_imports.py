#!/usr/bin/env python3
"""
Тестовый скрипт для проверки импортов.
"""
import sys
import os

def test_imports():
    """Тестирует все необходимые импорты."""
    print("🔍 Тестирование импортов...")
    
    try:
        # Тест 1: Базовые библиотеки
        print("1. Тестирование базовых библиотек...")
        import requests
        import logging
        from typing import List, Dict
        from tenacity import retry, stop_after_attempt, wait_exponential
        from bs4 import BeautifulSoup
        from dotenv import load_dotenv
        print("   ✅ Базовые библиотеки импортированы успешно")
        
        # Тест 2: OpenAI
        print("2. Тестирование OpenAI...")
        from openai import OpenAI
        print("   ✅ OpenAI импортирован успешно")
        
        # Тест 3: Наш модуль
        print("3. Тестирование нашего модуля...")
        from openai_module import OpenAIProxyClient
        print("   ✅ OpenAIProxyClient импортирован успешно")
        
        # Тест 4: Основной агент
        print("4. Тестирование основного агента...")
        from agent import ProductNamerAgent
        print("   ✅ ProductNamerAgent импортирован успешно")
        
        print("\n🎉 Все импорты работают корректно!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Ошибка импорта: {e}")
        print(f"   💡 Установите зависимости: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"   ❌ Неожиданная ошибка: {e}")
        return False

def test_environment():
    """Тестирует настройки окружения."""
    print("\n🔍 Тестирование окружения...")
    
    load_dotenv()
    
    api_key = os.getenv("PROXY_API_KEY")
    api_base = os.getenv("PROXY_API_BASE")
    
    if not api_key:
        print("   ❌ PROXY_API_KEY не найден")
        return False
    
    if not api_base:
        print("   ❌ PROXY_API_BASE не найден")
        return False
    
    print("   ✅ Переменные окружения настроены корректно")
    return True

def main():
    """Основная функция тестирования."""
    print("🚀 Тестирование Product Namer Agent")
    print("=" * 50)
    
    # Тест импортов
    imports_ok = test_imports()
    
    # Тест окружения
    env_ok = test_environment()
    
    print("\n" + "=" * 50)
    if imports_ok and env_ok:
        print("✅ Все тесты пройдены успешно!")
        print("🌐 Можно запускать веб-интерфейс: python run_web.py")
    else:
        print("❌ Некоторые тесты не пройдены")
        if not imports_ok:
            print("💡 Установите зависимости: pip install -r requirements.txt")
        if not env_ok:
            print("💡 Создайте файл .env с API ключами")

if __name__ == "__main__":
    main() 