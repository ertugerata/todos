import os
import time
from dotenv import load_dotenv
from flask import Flask, request, session, redirect, url_for
import requests
import init_db  # Import the new DB initialization script

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
PB_URL = os.getenv("POCKETBASE_URL")
# Admin credentials might still be loaded but are not used for schema creation anymore
PB_ADMIN_EMAIL = os.getenv("PB_ADMIN_EMAIL")
PB_ADMIN_PASSWORD = os.getenv("PB_ADMIN_PASSWORD")

# ensure_schema function removed as we use init_db.py via SQL

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            resp = requests.post(f"{PB_URL}/api/collections/users/auth-with-password", json={"identity": email, "password": password})
            if resp.status_code == 200:
                data = resp.json()
                session['user_token'] = data['token']
                session['user_id'] = data['record']['id']
                return redirect(url_for('dashboard'))
            else:
                return "Hata: Giriş bilgileri yanlış."
        except:
             return "Bağlantı hatası"
    return '''
        <div style="text-align:center; margin-top:50px;">
            <h3>Giriş Yap</h3>
            <form method="post">
                <input type="text" name="email" placeholder="Email" required><br><br>
                <input type="password" name="password" placeholder="Şifre" required><br><br>
                <input type="submit" value="Giriş Yap">
            </form>
        </div>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_token' not in session:
        return redirect(url_for('login'))

    token = session['user_token']
    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Verileri çek
        todos_resp = requests.get(f"{PB_URL}/api/collections/todos/records?sort=-created", headers=headers)
        todos = todos_resp.json().get('items', [])
    except:
        todos = []

    todos_html = ""
    for todo in todos:
        # İkonlar ve Stiller
        icon = "✅" if todo['is_completed'] else "⬜"
        text_style = "text-decoration: line-through; color: gray;" if todo['is_completed'] else ""
        
        # HTML Satırı (Checkbox - Metin - Sil Butonu)
        # Flexbox kullanarak silme butonunu en sağa itiyoruz
        todos_html += f"""
            <li style="display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #eee;">
                
                <a href="/toggle-status/{todo['id']}" style="text-decoration:none; margin-right:10px; font-size:1.2em;">
                    {icon}
                </a>
                
                <span style="{text_style}; flex-grow: 1;">{todo['title']}</span>
                
                <a href="/delete-todo/{todo['id']}" 
                   onclick="return confirm('Bu görevi silmek istediğine emin misin?');"
                   style="text-decoration:none; cursor:pointer;" title="Sil">
                    🗑️
                </a>
            </li>
        """

    return f"""
        <div style="font-family: sans-serif; max-width: 600px; margin: 50px auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h1>Yapılacaklar</h1>
                <a href="/logout" style="color:red; text-decoration:none; font-size:0.9em;">Çıkış Yap</a>
            </div>
            
            <div style="background:#f9f9f9; padding:15px; border-radius:8px; margin-bottom:20px;">
                <form action="/add-todo" method="post" style="display:flex; gap:10px;">
                    <input type="text" name="title" placeholder="Yeni görev ekle..." required style="flex:1; padding:10px; border:1px solid #ccc; border-radius:4px;">
                    <input type="submit" value="Ekle" style="padding:10px 20px; cursor:pointer; background-color:#28a745; color:white; border:none; border-radius:4px;">
                </form>
            </div>

            <ul style="list-style:none; padding:0;">
                {todos_html}
            </ul>
            
            <p style="text-align:center; color:#ccc; margin-top:30px;"><small>User ID: {session['user_id']}</small></p>
        </div>
    """

@app.route('/add-todo', methods=['POST'])
def add_todo():
    if 'user_token' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    new_todo = {
        "title": title,
        "is_completed": False,
        "user": session['user_id']
    }
    headers = {"Authorization": f"Bearer {session['user_token']}", "Content-Type": "application/json"}
    requests.post(f"{PB_URL}/api/collections/todos/records", json=new_todo, headers=headers)
    return redirect(url_for('dashboard'))

@app.route('/toggle-status/<todo_id>')
def toggle_status(todo_id):
    if 'user_token' not in session:
        return redirect(url_for('login'))

    headers = {"Authorization": f"Bearer {session['user_token']}"}
    url = f"{PB_URL}/api/collections/todos/records/{todo_id}"
    resp = requests.get(url, headers=headers)
    
    if resp.status_code == 200:
        current_status = resp.json().get('is_completed')
        requests.patch(url, json={"is_completed": not current_status}, headers=headers)
    
    return redirect(url_for('dashboard'))

@app.route('/delete-todo/<todo_id>')
def delete_todo(todo_id):
    if 'user_token' not in session:
        return redirect(url_for('login'))

    headers = {"Authorization": f"Bearer {session['user_token']}"}
    requests.delete(f"{PB_URL}/api/collections/todos/records/{todo_id}", headers=headers)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Initialize DB via SQL
    print("Initializing PocketBase schema via SQL...")
    for i in range(30):
        if init_db.init_db():
            break
        print(f"Retrying DB init in 2 seconds... ({i+1}/30)")
        time.sleep(2)

    app.run(debug=True, port=5000, host='127.0.0.1')
