"""
Модуль для работы с OpenAI API через прокси.
"""
import os
import logging
import json
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import OpenAI
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIProxyClient:
    """Клиент для работы с OpenAI API через прокси."""
    
    def __init__(self):
        """Инициализация клиента с настройками из .env."""
        self.api_key = os.getenv("PROXY_API_KEY")
        self.api_base = os.getenv("PROXY_API_BASE")
        
        if not self.api_key or not self.api_base:
            raise ValueError("PROXY_API_KEY и PROXY_API_BASE должны быть установлены в .env")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def generate_product_names(self, product_description: str) -> List[Dict[str, str]]:
        """
        Генерирует 5 вариантов названий для продукта.
        
        Args:
            product_description: Описание продукта из статьи
            
        Returns:
            Список из 5 словарей с ключами 'name' и 'reason'
        """
        prompt = f"""Ты креативный маркетолог. Предложи 5 вариантов названия для продукта.

Описание продукта:
{product_description}

Верни ответ в формате JSON:
[
    {{"name": "Название 1", "reason": "Объяснение почему это название подходит"}},
    {{"name": "Название 2", "reason": "Объяснение почему это название подходит"}},
    {{"name": "Название 3", "reason": "Объяснение почему это название подходит"}},
    {{"name": "Название 4", "reason": "Объяснение почему это название подходит"}},
    {{"name": "Название 5", "reason": "Объяснение почему это название подходит"}}
]

Убедись, что названия уникальные, креативные и подходят к описанию продукта."""

        try:
            logger.info("Отправка запроса к OpenAI API...")
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Ты креативный маркетолог, специализирующийся на создании запоминающихся названий для продуктов."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            # Извлекаем ответ
            content = response.choices[0].message.content.strip()
            logger.info("Получен ответ от OpenAI API")
            
            # Парсим JSON ответ
            try:
                result = json.loads(content)
                if not isinstance(result, list) or len(result) != 5:
                    raise ValueError("Неверный формат ответа")
                
                # Проверяем структуру каждого элемента
                for item in result:
                    if not isinstance(item, dict) or 'name' not in item or 'reason' not in item:
                        raise ValueError("Неверная структура элемента ответа")
                
                logger.info(f"Успешно сгенерировано {len(result)} названий")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга JSON: {e}")
                logger.error(f"Полученный контент: {content}")
                raise ValueError(f"Не удалось распарсить JSON ответ: {e}")
                
        except Exception as e:
            logger.error(f"Ошибка при обращении к OpenAI API: {e}")
            raise 