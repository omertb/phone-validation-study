from flask import Flask, render_template, request, flash, redirect, url_for, session
from forms import UserForm, EnterOtpForm
import os
from random import randint
import time

app = Flask(__name__)
app.secret_key = os.environ['FSECRETKEY']


def generate_otp():
    return randint(100000, 999999)


def verify_user(username, phone_number):
    # Pull LDAP attributes and verify
    return True


def send_otp(phone_number):
    # GSM Network SMS API
    otp = generate_otp()
    session['otp_generation_time'] = int(time.time())
    session['otp_in_session'] = str(otp)
    print('Your OTP Key is: {}'.format(session['otp_in_session']))
    return True


@app.route('/', methods=['GET', 'POST'])
def home():
    form = UserForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Inputs are valid')
            username = request.form['username']
            phone_number = request.form['phone_number']
            user_verified = verify_user(username, phone_number)
            if user_verified:
                sms_sent = send_otp(phone_number)
                if sms_sent:
                    return redirect(url_for('enter_otp'))
            else:
                flash('User Not Found!')
        else:
            flash('Invalid Input')

    return render_template('user_form.html', form=form)


@app.route('/enter_otp', methods=['GET', 'POST'])
def enter_otp():
    form = EnterOtpForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            form_input_otp = request.form['otp_field']
            if 'otp_in_session' in session:
                current_time = int(time.time())

                if current_time - session['otp_generation_time'] < 60:
                    if form_input_otp == session['otp_in_session']:
                        flash('Verified')
                        print("Entered OTP: {}".format(form_input_otp))
                        print("Generated OTP: {}".format((session['otp_in_session'])))
                        session.pop('otp_in_session', None)
                    else:
                        print("Entered OTP: {}".format(form_input_otp))
                        print("Generated OTP: {}".format((session['otp_in_session'])))
                        flash('Failed')
                else:
                    session.pop('otp_in_session', None)
                    session.pop('otp_generation_time', None)
                    flash('OTP Key is no longer valid, go to previous page')
            else:
                return redirect(url_for('home'))

    return render_template('otp_form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
