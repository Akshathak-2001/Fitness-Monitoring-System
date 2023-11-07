from flask import Flask, render_template, request, Response

app = Flask(__name__)#creates flask application

@app.route('/')#root directory
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        name=request.form['name']
        weight=int(request.form['weight'])
        height=int(request.form['height'])
                
        #calculating BMI
        bmi =weight/((height/100)**2)
        #conditions
        print("Your body mass index is: ", bmi)
        if ( bmi < 16):
            sug = 'pushup'
            sug1 = 'squat'
        elif ( bmi >= 16 and bmi < 18.5):
            sug = 'downward_dog'
            sug1 = 'plank'
        elif ( bmi >= 18.5 and bmi < 25):
            sug = 'bicep'
            sug1 = 'squat'
        elif ( bmi >= 25 and bmi < 30):
            sug = 'plank'
            sug1 = 'pushup'
        elif ( bmi >=30):
            sug = 'downward_dog'
            sug1 = 'squat'
        print(sug)
        return render_template('index.html', sug1=sug1, sug=sug, bmi='{:.2f}'.format(bmi), name=name)
        
    return render_template('index.html')

@app.route('/video/<vid>') #<vid> is a variable for different exercises
def video(vid):
    print(vid)
    f = open('exercise.txt', 'w')# previious entry will be erased everytime something is written
    f.write(vid+',1')
    f.close()
    return render_template('index.html', res=vid)

@app.route('/live/<vid>')
def live(vid):
    print(vid)
    f = open('exercise.txt', 'w')
    f.write(vid+',0')
    f.close()
    return render_template('index.html', res=vid)

@app.route('/video_feed')
def video_feed():
    f = open('exercise.txt', 'r')
    data = f.readline()
    f.close()
    data = data.split(',') # exercise.txt
    if data[0] == 'bicep':
        from bicep import gen_frames
    if data[0] == 'downward_dog':
        from downward_dog import gen_frames
    if data[0] == 'plank':
        from plank import gen_frames
    if data[0] == 'pushup':
        from pushup import gen_frames
    if data[0] == 'squat':
        from squat import gen_frames
    
    if data[1] == '0':
        d = 0
    else:
        d = data[0]+'.mp4'
    try:
        return Response(gen_frames(d), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(e)
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
