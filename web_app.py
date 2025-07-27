"""
Веб-приложение для Product Namer Agent.
"""
from flask import Flask, render_template, request, jsonify
import logging
from agent import ProductNamerAgent
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Инициализируем агента
try:
    agent = ProductNamerAgent()
    logger.info("Product Namer Agent успешно инициализирован")
except Exception as e:
    logger.error(f"Ошибка инициализации агента: {e}")
    agent = None


@app.route('/')
def index():
    """Главная страница."""
    return render_template('index.html')


@app.route('/api/generate-names', methods=['POST'])
def generate_names():
    """API endpoint для генерации названий."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Данные не получены'}), 400
        
        url = data.get('url', '').strip()
        description = data.get('description', '').strip()
        
        if not url and not description:
            return jsonify({'error': 'Необходимо указать URL или описание продукта'}), 400
        
        if not agent:
            return jsonify({'error': 'Агент не инициализирован. Проверьте настройки API.'}), 500
        
        # Генерируем названия
        if url:
            logger.info(f"Генерация названий из URL: {url}")
            names = agent.generate_names_from_url(url)
        else:
            logger.info("Генерация названий из описания")
            names = agent.generate_names_from_description(description)
        
        return jsonify({
            'success': True,
            'names': names,
            'source': 'url' if url else 'description'
        })
        
    except Exception as e:
        logger.error(f"Ошибка при генерации названий: {e}")
        return jsonify({
            'error': f'Ошибка при генерации названий: {str(e)}'
        }), 500


@app.route('/api/health')
def health_check():
    """Проверка состояния API."""
    return jsonify({
        'status': 'healthy',
        'agent_initialized': agent is not None
    })


@app.errorhandler(404)
def not_found(error):
    """Обработка 404 ошибки."""
    return jsonify({'error': 'Страница не найдена'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработка 500 ошибки."""
    return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


if __name__ == '__main__':
    # Проверяем инициализацию агента
    if agent:
        print("✅ Product Namer Agent готов к работе!")
        print("🌐 Веб-интерфейс доступен по адресу: http://localhost:5000")
    else:
        print("❌ Ошибка инициализации агента. Проверьте настройки в .env файле")
        print("💡 Убедитесь, что установлены PROXY_API_KEY и PROXY_API_BASE")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 