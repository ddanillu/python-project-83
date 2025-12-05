import os
from flask import Flask, request, redirect, url_for, flash, render_template
from .db_manager import URL
from .validator import validate_url

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
    return render_template('list_urls.html', urls=urls)


@app.route('/urls/<int:id>')
def show_url(id):
    url = URL.get_url(id)
    if url is None:
        flash('Страница не найдена')
        return redirect(url_for('manage_urls'))
    
    return render_template('show_url.html', url=url)


@app.route('/urls/<id>/checks')
def check_url(id):
    url_entry = URL.get_url(id)
    if url_entry is None:
        flash('Страница не найдена')
        return redirect(url_for('manage_urls'))

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