import os
from flask import Flask, request, redirect, url_for, flash, render_template
from .db_manager import URL
from .validator import validate_url
from .checker import checking_url

try:
    from dotenv import load_dotenv
    load_dotenv(".env")
except ModuleNotFoundError:
    pass


app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/urls', methods=['GET', 'POST'])
def manage_urls():
    """
    Обрабатывает добавление новых URL и отображает список существующих.

    При POST-запросе: 
    - Получает URL из формы.
    - Проверяет его на валидность с помощью функции validate_url.
    - Если URL уже существует, перенаправляет на страницу с ним.
    - Если URL новый, добавляет его в БД и перенаправляет на его страницу.
    """
    if request.method == 'POST':
        url = request.form['url']
        if not validate_url(url):
            flash('Недопустимый URL! Пожалуйста, введите действительный URL длиной не более 255 символов')
            return redirect(url_for('index'))
        
        existing_url_id = URL.url_exists(url)
        if existing_url_id:
            flash('Эта страница уже существует в базе данных')
            return redirect(url_for('show_url', id=existing_url_id))
        else:
            url_id = URL.add_url_and_get_id(url)
            if url_id is None:
                flash('Ошибка: невозможно получить ID добавленной страницы')
                return redirect(url_for('index'))
            flash('Страница успешно добавлена')
            return redirect(url_for('show_url', id=url_id))

    urls = URL.get_all_urls()
    checks_data = {}

    for url_entry in urls:
        checks = URL.get_checks(url_entry.id)
        last_check = checks[0]
        last_check_code = last_check['status_code'] if checks else ''
        last_check_date = last_check['created_at'] if checks else ''
        checks_data[url_entry.id] = {
            'status_code': last_check_code,
            'check_date': last_check_date
        }

    return render_template('list_urls.html', urls=urls, checks_data=checks_data)


@app.route('/urls/<int:id>')
def show_url(id):
    url = URL.get_url(id)
    if url is None:
        flash('Страница не найдена')
        return redirect(url_for('manage_urls'))
    
    checks = URL.get_checks(id)
    return render_template('show_url.html', url=url, checks=checks)


@app.route('/urls/<id>/checks', methods=['POST'])
def check_url(id):
    url_entry = URL.get_url(id)
    if url_entry is None:
        flash('Страница не найдена')
        return redirect(url_for('manage_urls'))
    
    check_data = checking_url(url_entry)
    if check_data is None:
        flash('Произошла ошибка при проверке')
    else:
        URL.add_check(
            id,
            check_data['code'],
            check_data['h1'],
            check_data['title'],
            check_data['meta_description']
            )
        flash('Страница успешно проверена')

    return redirect(url_for('show_url', id=id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)