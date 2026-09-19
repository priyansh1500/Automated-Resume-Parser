# run.py
#
# This is the entry point for the application.
# Run this file to start the Flask development server:
#
#   python run.py
#
# The server will start at: http://127.0.0.1:5000
# Press Ctrl+C in the terminal to stop it.

from app import create_app

# Create the Flask app using our factory function
app = create_app()

if __name__ == '__main__':
    # debug=True means:
    #   - The server automatically restarts when you change a .py file
    #   - You see detailed error messages in the browser (useful while learning)
    # IMPORTANT: Never use debug=True in a real production deployment.
    app.run(debug=True)
