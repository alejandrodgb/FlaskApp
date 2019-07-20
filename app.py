from flask import Flask, render_template, request, json, redirect, session
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'adgb'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Chicharito1'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')

def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['GET','POST'])
def signUp():
    try:
        # Read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Validate received values
        if _name and _email and _password:

            # Values validated, connect to SQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name,_email, _hashed_password))
            data=cursor.fetchall()
            
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
    finally:
        cursor.close()
        conn.close()

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Connect to MySQL
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data)>0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0] # set the user key of the session to the user MySQL id
                return redirect('userHome')
            else:
                return render_template('error.html', error='Wrong email or password.')
        else:
            return render_template('error.html', error = 'Wrong email or password.')
    except Exception as e:
        return render_template('error.html', error = f'{_username}\n{str(e)}')
    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error = 'Unathorized access.')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug = True)