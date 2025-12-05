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

app.secret_key = os.getenv('SECRET_KEY') or 'default_secret'
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/urls', methods=['GET', 'POST'])
def manage_urls():
    if request.method == 'POST':
        url = request.form['url']
        if not validate_url(url):
            flash('Invalid URL! Please enter a valid URL not exceeding 255 characters.')
            return redirect(url_for('index'))
        
        existing_url_id = URL.get_id(url)
        if existing_url_id is not None:
            flash('This URL already exists in the database.')
            return redirect(url_for('show_url', id=existing_url_id))
        
        URL.add_to_urls(url)

        url_id = URL.get_id(url)
        if url_id is None:
            flash('Error: Unable to retrieve the ID for the added URL.')
            return redirect(url_for('index'))
        else:
            flash('URL added successfully!')
            return redirect(url_for('show_url', id=url_id))

    urls = URL.get_all_urls()
    return render_template('list_urls.html', urls=urls)


@app.route('/urls/<int:id>')
def show_url(id):
    url = URL.get_url(id)
    if url is None:
        flash('URL not found.')
        return redirect(url_for('manage_urls'))
    
    return render_template('show_url.html', url=url)


if __name__ == "__main__":
    app.run(debug=True)