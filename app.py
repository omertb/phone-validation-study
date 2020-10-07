from flask import Flask, render_template, request, flash
from forms import UserForm
import os

app = Flask(__name__)
app.secret_key = os.environ['FSECRETKEY']


@app.route('/', methods=['GET', 'POST'])
def home():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Inputs are valid')

    return render_template('user_form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
