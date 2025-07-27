"""
Основной модуль агента для генерации названий продуктов.
"""
import logging
import requests
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from bs4 import BeautifulSoup
from openai_module import OpenAIProxyClient

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductNamerAgent:
    """Агент для генерации названий продуктов на основе описания из веб-страниц."""
    
    def __init__(self):
        """Инициализация агента."""
        self.openai_client = OpenAIProxyClient()
        self.session = requests.Session()
        # Устанавливаем User-Agent для более надежного парсинга
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def fetch_webpage_content(self, url: str) -> str:
        """
        Загружает HTML-контент веб-страницы.
        
        Args:
            url: URL страницы для загрузки
            
        Returns:
            HTML-контент страницы
        """
        try:
            logger.info(f"Загрузка страницы: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            logger.info(f"Страница успешно загружена, размер: {len(response.content)} байт")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Ошибка при загрузке страницы {url}: {e}")
            raise
    
    def extract_product_description(self, html_content: str) -> str:
        """
        Извлекает описание продукта из HTML-контента.
        
        Args:
            html_content: HTML-контент страницы
            
        Returns:
            Извлеченное описание продукта
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Удаляем скрипты и стили
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Ищем описание в различных тегах
            description_candidates = []
            
            # 1. Ищем в meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                description_candidates.append(meta_desc['content'])
            
            # 2. Ищем в тегах article, main, section
            for tag in ['article', 'main', 'section']:
                elements = soup.find_all(tag)
                for element in elements:
                    text = element.get_text(strip=True)
                    if len(text) > 100:  # Минимальная длина для описания
                        description_candidates.append(text)
            
            # 3. Ищем в параграфах
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if len(text) > 50:  # Минимальная длина для параграфа
                    description_candidates.append(text)
            
            # 4. Если ничего не найдено, берем весь текст body
            if not description_candidates:
                body = soup.find('body')
                if body:
                    description_candidates.append(body.get_text(strip=True))
            
            # Выбираем лучшее описание (самое длинное из подходящих)
            if description_candidates:
                # Фильтруем слишком короткие описания
                filtered_candidates = [desc for desc in description_candidates if len(desc) > 100]
                if filtered_candidates:
                    best_description = max(filtered_candidates, key=len)
                else:
                    best_description = max(description_candidates, key=len)
                
                # Ограничиваем длину описания
                if len(best_description) > 2000:
                    best_description = best_description[:2000] + "..."
                
                logger.info(f"Извлечено описание длиной {len(best_description)} символов")
                return best_description
            else:
                raise ValueError("Не удалось извлечь описание продукта из страницы")
                
        except Exception as e:
            logger.error(f"Ошибка при извлечении описания: {e}")
            raise
    
    def generate_names_from_url(self, url: str) -> List[Dict[str, str]]:
        """
        Основной метод: загружает страницу, извлекает описание и генерирует названия.
        
        Args:
            url: URL страницы с описанием продукта
            
        Returns:
            Список из 5 словарей с ключами 'name' и 'reason'
        """
        try:
            logger.info(f"Начинаем обработку URL: {url}")
            
            # 1. Загружаем HTML
            html_content = self.fetch_webpage_content(url)
            
            # 2. Извлекаем описание
            product_description = self.extract_product_description(html_content)
            logger.info(f"Извлечено описание продукта: {product_description[:200]}...")
            
            # 3. Генерируем названия
            names = self.openai_client.generate_product_names(product_description)
            
            logger.info(f"Успешно сгенерировано {len(names)} названий")
            return names
            
        except Exception as e:
            logger.error(f"Ошибка в процессе генерации названий: {e}")
            raise
    
    def generate_names_from_description(self, description: str) -> List[Dict[str, str]]:
        """
        Генерирует названия напрямую из предоставленного описания.
        
        Args:
            description: Описание продукта
            
        Returns:
            Список из 5 словарей с ключами 'name' и 'reason'
        """
        try:
            logger.info("Генерация названий из предоставленного описания")
            names = self.openai_client.generate_product_names(description)
            logger.info(f"Успешно сгенерировано {len(names)} названий")
            return names
        except Exception as e:
            logger.error(f"Ошибка при генерации названий: {e}")
            raise


def main():
    """Пример использования агента."""
    agent = ProductNamerAgent()
    
    # Пример URL для тестирования
    test_url = "https://example.com/product-page"
    
    try:
        names = agent.generate_names_from_url(test_url)
        print("Сгенерированные названия:")
        for i, name_data in enumerate(names, 1):
            print(f"{i}. {name_data['name']}")
            print(f"   Причина: {name_data['reason']}")
            print()
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main() 