from flask import Flask, request, jsonify
import jwt
import datetime
import os

app = Flask(__name__)
SECRET_KEY = "mysecretkey123"  # Change to a stronger secret for production

# --------------------------
# Login Endpoint (POST)
# --------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Dummy authentication
    if username == "aravind" and password == "12345":
        token = jwt.encode({
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            "iat": datetime.datetime.utcnow()
        }, SECRET_KEY, algorithm="HS256")
        
        # Ensure token is string for compatibility
        token = token if isinstance(token, str) else token.decode('utf-8')

        return jsonify({"access_token": token})

    return jsonify({"error": "Invalid credentials"}), 401

# --------------------------
# Protected Endpoint (GET)
# --------------------------
@app.route("/profile", methods=["GET"])
def profile():
    auth = request.headers.get("Authorization")
    if not auth:
        return jsonify({"error": "Missing token"}), 401

    try:
        token = auth.split(" ")[1]   # Bearer <token>
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "Token valid", "data": decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

# --------------------------
# Main
# --------------------------
if __name__ == "__main__":
    # Host 0.0.0.0 makes it accessible on deployed servers
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port, debug=False)
