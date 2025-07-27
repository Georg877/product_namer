"""
Тестовый скрипт для демонстрации работы Product Namer Agent.
"""
from agent import ProductNamerAgent
import json


def test_with_description():
    """Тест с прямым описанием продукта."""
    print("🧪 Тест 1: Генерация названий из описания")
    print("=" * 50)
    
    agent = ProductNamerAgent()
    
    # Пример описания продукта
    description = """
    Инновационный смартфон с искусственным интеллектом, оснащенный 
    передовой камерой с возможностью распознавания объектов в реальном времени. 
    Устройство имеет ультратонкий дизайн, защищенный от воды и пыли, 
    с батареей, работающей до 48 часов без подзарядки. 
    Включает в себя голосового помощника с поддержкой 15 языков 
    и систему безопасности с биометрической аутентификацией.
    """
    
    try:
        names = agent.generate_names_from_description(description)
        
        print("✅ Успешно сгенерированы названия:")
        print()
        
        for i, name_data in enumerate(names, 1):
            print(f"📱 {i}. {name_data['name']}")
            print(f"   💡 {name_data['reason']}")
            print()
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def test_with_url():
    """Тест с URL (требует реальный URL)."""
    print("🧪 Тест 2: Генерация названий из URL")
    print("=" * 50)
    
    agent = ProductNamerAgent()
    
    # Замените на реальный URL с описанием продукта
    test_url = "https://example.com/product-page"
    
    print(f"⚠️  Внимание: Для реального теста замените URL на действующий")
    print(f"📄 Текущий URL: {test_url}")
    print()
    
    try:
        names = agent.generate_names_from_url(test_url)
        
        print("✅ Успешно сгенерированы названия:")
        print()
        
        for i, name_data in enumerate(names, 1):
            print(f"📱 {i}. {name_data['name']}")
            print(f"   💡 {name_data['reason']}")
            print()
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("💡 Это ожидаемо для тестового URL")


def save_results_to_file(names, filename="generated_names.json"):
    """Сохраняет результаты в JSON файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(names, f, ensure_ascii=False, indent=2)
        print(f"💾 Результаты сохранены в файл: {filename}")
    except Exception as e:
        print(f"❌ Ошибка при сохранении файла: {e}")


def main():
    """Основная функция тестирования."""
    print("🚀 Product Namer Agent - Тестирование")
    print("=" * 60)
    print()
    
    # Тест 1: С описанием
    test_with_description()
    
    print()
    print("-" * 60)
    print()
    
    # Тест 2: С URL
    test_with_url()
    
    print()
    print("=" * 60)
    print("✅ Тестирование завершено!")
    print()
    print("💡 Для использования с реальными URL:")
    print("   1. Убедитесь, что файл .env настроен правильно")
    print("   2. Замените test_url на реальный URL продукта")
    print("   3. Запустите скрипт снова")


if __name__ == "__main__":
    main() 