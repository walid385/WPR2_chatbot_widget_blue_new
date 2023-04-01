from flask import Flask, render_template, request
import openai



app = Flask(__name__)

# Set up OpenAI API credentials

openai.api_key = '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'


# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful cooking assistant for the Thermomix TM6."},
        {"role": "user", "content": message}
    ]
    )
    if completion.choices[0].message!=None:
        return completion.choices[0].message

    else :
        return 'Failed to Generate response!'
    
{"role": "assistant", "content": "All about cooking with the Thermomix TM6."},

if __name__=='__main__':
    app.run()
