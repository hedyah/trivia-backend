from app import app
import bcrypt
import sys




if len(sys.argv) > 1:
    mode = sys.argv[1]
    
else:
    print("missing requriement argument: testing")
    exit()

if mode == "testing":
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif mode == "production":
    import bjoern
    print("running production mode")
    bjoern.run(app, "0.0.0.0", 5005)
else:
    print("invalid mode, please chose either 'testing' or 'production'")
    exit()