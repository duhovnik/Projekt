from flask import Flask, request, render_template_string, render_template
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Load database configuration
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

def get_card_type(number):
    if len(number) in [13, 16] and number.startswith(('4',)):
        return 'Visa'
    elif len(number) == 16 and number.startswith(('51', '52', '53', '54', '55')):
        return 'Mastercard'
    elif len(number) == 16 and number.startswith('6011'):
        return 'Discover'
    elif len(number) == 15 and number.startswith(('34', '37')):
        return 'American Express'
    elif len(number) == 14 and number.startswith(('36', '38')):
        return 'Diner\'s Club'
    elif 12 <= len(number) <= 19 and number.startswith('5'):
        return 'Maestro'
    elif 16 <= len(number) <= 19 and number.startswith('6304'):
        return 'Laser'
    elif len(number) in [16, 18, 19] and number.startswith(('4903', '4905', '4911', '4936', '6333', '6759')):
        return 'Switch'
    elif len(number) in [16, 18, 19] and number.startswith(('6334', '6767')):
        return 'Solo'
    elif len(number) in [15, 16] and number.startswith('35'):
        return 'JCB'
    elif len(number) == 16 and number.startswith('62'):
        return 'China UnionPay'
    else:
        return 'Unknown'

def check_credit_card(number):
    number_str = str(number)
    reversed_number_str = number_str[::-1]
    
    total = 0
    for i, digit in enumerate(reversed_number_str):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        number = request.form.get('card_number')
        card_type = get_card_type(number)
        if card_type != 'Unknown' and check_credit_card(number):
            message = f"The number is a valid {card_type} credit card number."
        else:
            message = "The number is not a valid credit card number."

        # Write results to database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO results(card_number, result) VALUES (%s, %s)", (number, message))
        mysql.connection.commit()
        cursor.close()
    return render_template('index.html', message=message)



@app.route('/results')
def results():
    cursor = mysql.connection.cursor()
    result_value = cursor.execute("SELECT * FROM results")
    if result_value > 0:
        results = cursor.fetchall()
        return render_template('results.html', results=results)
    return 'No results found'
                    
@app.route('/luhn-algorithm')
def show_luhn():
    return render_template('luhn-algorithm.html')

@app.route('/check-digits')
def show_check():
    return render_template('check-digits.html')
    
@app.route('/card-number-formats')
def show_formats():
    return render_template('card-number-formats.html')    

@app.route('/cvv')
def show_cvv():
    return render_template('cvv.html')

@app.route('/security-tips')
def show_securitytips():
    return render_template('security-tips.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
