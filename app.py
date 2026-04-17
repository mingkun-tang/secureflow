from flask import Flask, request, session, render_template, redirect, url_for
import secrets 
from markupsafe import escape

MODE = "secure"

token = secrets.token_urlsafe(32)

users = {
    "admin": {"password": "admin123", "role": "admin", "email": "admin123@gmail.com"},
    "alice": {"password": "alice123", "role": "user", "email": "alice123@gmail.com"},
    "bob": {"password": "bob123", "role": "user", "email": "bob123@gmail.com"},
    "boss": {"password": "boss123", "role": "boss", "email": "boss123@gmail.com"}
    }
                   


app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def home():
    return render_template("index.html",mode=MODE)

@app.route("/attack_demo", methods=("GET", "POST"))
def attack_demo():
    return render_template('attack_demo.html', mode=MODE)


@app.route("/profile")
def profile():
    return "This is your Profile!"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html",mode=MODE)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
    if username in users and users[username]["password"] == password:
        session["user"] = username
        session["role"] = users[username]["role"]
        return redirect(url_for("home"))
    else:
        return render_template("login.html", message="Invalid username or password",mode=MODE)


@app.route("/admin/kpi")
def admin_kpi():
    if "user" not in session:
        return redirect(url_for("login"))

    if MODE == "secure":
        if session.get("role") != "admin":
            return render_template(
                "index.html",
                message="You do not have permission to access this page",
                mode=MODE
            )
    return render_template("admin_kpi.html", mode=MODE)


@app.route("/boss/financials")
def boss_financials():
    if "user" not in session:
        return redirect(url_for("login"))

    if MODE == "secure":
        if session.get("role") != "boss":
            return render_template(
                "index.html",
                message="You do not have permission to access this page",
                mode=MODE
            )
    return render_template("boss_financials.html", mode=MODE)


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"Welcome {session["user"]}"
    else:
        return redirect(url_for("login"))


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        token = secrets.token_hex(16)
        session["csrf_token"] = token
        return render_template("transfer.html", csrf_token=token, mode=MODE)

    if request.method == "POST":
        to = request.form.get("to")
        amount = request.form.get("amount")
        form_token = request.form.get("csrf_token")
        session_token = session.get("csrf_token")

        token = secrets.token_hex(16)
        session["csrf_token"] = token

        if form_token == session_token:
            return render_template(
            "transfer.html",
            csrf_token=token,
            message=f"Transferred {amount} to {to}!", 
            mode=MODE
            )
    return render_template(
        "transfer.html",
        csrf_token=token,
        message="CSRF detected, mode==MODE"
    )


@app.route("/account")
def account():
    if "user" in session:
        user = session["user"]
        data = users.get(user, "User not found")
        return f"{user}'s account: {data}"
    else:
        return redirect(url_for("login"))


@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():
    if request.method == "GET":
        return '''
        <form method="POST">
            User to delete: <input name="user">
            <button type="submit">Delete</button>
        '''
    if request.method == "POST":
        if "user" not in session:
            return redirect(url_for("login"))
        
        user = session["user"]
        role = users[user]["role"]

        if role == "admin":
            user_to_delete = request.form.get("user")
            del users[user_to_delete]
            return f"User: {user_to_delete} is deleted from the system"
        else:
            return "You Do Not Have Access"
        
@app.route("/change_role", methods=["GET", "POST"])
def change_role():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        if MODE == "secure" and session.get("role") != "admin":
            return render_template("index.html", message="You do not have permission to access this page", mode=MODE)
        return render_template("change_role.html", mode=MODE)

    if MODE == "vulnerable":
        new_role = request.form.get("role")
        current_user = session["user"]

        users[current_user]["role"] = new_role
        session["role"] = new_role

        return render_template(
            "change_role.html",
            message=f"Your role has been changed to {new_role}",
            mode=MODE
        )

    if session.get("role") != "admin":
        return render_template("index.html", message="You do not have permission to access this page", mode=MODE)

    target_user = request.form.get("user")
    new_role = request.form.get("role")

    if target_user in users:
        users[target_user]["role"] = new_role
        return render_template(
            "change_role.html",
            message=f"{target_user}'s role has been changed to {new_role}",
            mode=MODE
        )

    return render_template(
        "change_role.html",
        message="User not found",
        mode=MODE
    )


@app.route("/update_profile", methods = ["GET", "POST"])
def update_profile():
    if request.method == "GET":
        if "user" not in session:
            return redirect(url_for("login"))
        else:
            return render_template("update_profile.html", mode=MODE)
        
    if request.method == "POST":
            if "user" in session:
                update_email = request.form.get("email")
                current_user = session["user"]    
                users[current_user]["email"] = update_email
                return f"Your email have been updated to {update_email}"

            return "Access Denied"
    
        
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("change_password.html", mode=MODE)

    user = session["user"]
    user_current_password = users[user]["password"]
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if current_password == user_current_password and new_password == confirm_password:
        users[user]["password"] = new_password
        return render_template(
            "change_password.html",
            message="Password updated successfully",
            mode=MODE
        )

    return render_template(
        "change_password.html",
        message="Invalid password change request",
        mode=MODE
    )


if __name__ == "__main__":
    app.run(debug=True)
