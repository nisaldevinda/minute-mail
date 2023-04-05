from flask import Flask, render_template, request
app= Flask(__name__)
app.static_folder = 'static'

@app.route("/")
@app.route("/homepage")
def inputspage():
    return render_template("index.html")

@app.route("/inputspage")
def homepage():
    return render_template("Generate email.html")

@app.route("/loginpage")
def loginpage():
    return render_template("login.html")

inputs=[]

@app.route("/GenerateEmail", methods=["POST", "GET"])
def GenerateEmail():
    if request.method=="POST":
        sender_name= request.form.get("sender-name")
        recipient_name=request.form.get("recipient-name")
        recipient_title=request.form.get("recipient-title")
        purpose=request.form.get("purpose")
        content=request.form.get("content")
        inputs.clear()
        inputs.append(sender_name)
        inputs.append(recipient_name)
        inputs.append(recipient_title)
        inputs.append(purpose)
        inputs.append(content)
        
        return DisplayEmail()
    
def CreatePrompt():
    sender_name= inputs[0]
    recipient_name= inputs[1]
    recipient_title= inputs[2]
    purpose= inputs[3]
    content= inputs[4]
    emailtype="email"
    prompt="Write an "+emailtype+" to "+recipient_title+" "+recipient_name+" for "+purpose+" and mentioning "+content+" "+" for myself, "+sender_name+". Continue"
    return prompt 
    

import openai

f = open("D:\key\key.txt", "r")

key= f.read()

openai.api_key = key

def APIcall():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= CreatePrompt(),
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    return response.choices[0].text

def DisplayEmail():
    sender_name= inputs[0]
    recipient_name= inputs[1]
    recipient_title= inputs[2]
    purpose= inputs[3]
    content= inputs[4]
    email= APIcall()
    return render_template("email-result.html", sender_name= sender_name, recipient_name= recipient_name, recipient_title= recipient_title, 
                           purpose= purpose, content=content, generated_email= email)

if __name__=="__main__":
    app.run(debug=True, port=50001)
        



