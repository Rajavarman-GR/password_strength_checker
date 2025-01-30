from flask import Flask, render_template, request, jsonify
import re
import random
import string
app = Flask(__name__)
# Home route serving the HTML page
@app.route('/')
def home():
    return render_template('index.html')
# Password Strength Checker route
@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    password = data.get('password', '')
    # Check the strength and recommendations
    strength, recommendations = password_strength_checker(password)
    return jsonify({"strength": strength, "recommendations": recommendations})
# Password Generator route
@app.route('/generate')
def generate():
    password = generate_password()
    return jsonify({"password": password})
# Function to check password strength
def password_strength_checker(password):
    score = 0
    recommendations = []
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        recommendations.append("Password should be at least 8 characters long.")
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        recommendations.append("Add at least one uppercase letter.")
    if re.search(r'[a-z]', password):
        score += 1
    else:
        recommendations.append("Add at least one lowercase letter.")
    if re.search(r'[0-9]', password):
        score += 1
    else:
        recommendations.append("Add at least one digit.")
    if re.search(r'[@$!%*?&]', password):
        score += 1
    else:
        recommendations.append("Add at least one special character.")
    if re.search(r'(.)\1\1', password):
        recommendations.append("Avoid repeated characters.")
    if re.search(r'123|abc|password', password.lower()):
        recommendations.append("Avoid common sequences or phrases like '123', 'abc', or 'password'.")
    if score >= 5:
        strength = "Very Strong"
    elif score >= 4:
        strength = "Strong"
    elif score >= 2:
        strength = "Moderate"
    else:
        strength = "Weak"
    return strength, recommendations
# Function to generate a strong password
def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + "@$!%*?&"
    return ''.join(random.choice(characters) for _ in range(length))
if __name__ == '__main__':
    app.run(debug=True)
