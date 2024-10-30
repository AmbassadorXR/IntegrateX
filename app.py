from flask import Flask, render_template, request, redirect, url_for
from app.api_service import fetch_repos
import asyncio
import logging_config

app = Flask(__name__)

logger = logging_config.get_logger(__name__)


@app.route('/')
def home():
    return render_template('index.html')


# Страница дашборда
@app.route('/dashboard')
async def dashboard():
    logger.info('Получаем имя пользователя из аргументов или сессии')
    username = request.args.get('username')
    if not username:
        return redirect(url_for('home'))

    logger.info('Получаем репозитории через API')
    repos = await fetch_repos(username)
    if repos is None:
        error = 'Ошибка получения данных'
        logger.error(error)
        return render_template('error.html', error=error)

    logger.info('Передаем данные на дашборд')
    return render_template('dashboard.html', repos=repos)


# Страница настроек (ввод GitHub username)
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        logger.info('Получаем введенное имя пользователя')
        username = request.form.get('username')
        if username:
            logger.info('Перенаправляем на дашборд с введенным именем пользователя')
            return redirect(url_for('dashboard', username=username))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
