from flask import Flask, render_template, jsonify, request
from gevent.pywsgi import WSGIServer
import serial
import time

app=Flask(__name__)
ser= serial.Serial("/dev/ttyAMA0",115200,timeout = 1.0)
#ser=serial.Serial("COM3",115200,timeout=1.0)

time.sleep(0.5)
ser.reset_input_buffer()

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/get_values")
def get_values():
    #this is PWM, current value for
    ser.write(b"0000 0000 0000 0000")

    line = ser.readline().decode('utf-8').rstrip()
    telemetry = [x.strip() for x in line.split(",")]
    values={
        'pitch_angle':telemetry[0],
        'yaw_angle':telemetry[1],
        'distance_1':telemetry[2],
        'distance_2':telemetry[3],
        'distance_3':telemetry[4],
        'distance_4':telemetry[5],
        'pwm_1':telemetry[6],
        'pwm_2':telemetry[7],
        'pwm_3':telemetry[8],
        'pwm_4':telemetry[9],
        'current':telemetry[10],
        'velocity':telemetry[11],
	      'mode':telemetry[12],
    }
    return jsonify(values)

@app.route("/check", methods=['GET', 'POST'])
def check():
    message = ""
    if request.method == 'POST':
        selected_mode = request.form.get('modes')
        if selected_mode == 'mode1':
            ser.write(b"0")
            message = "The Mode is in Idle"            
        if selected_mode == 'mode2':
            ser.write(b"2")
            message = "The Mode is in Auto Control" 
        elif selected_mode == 'mode4':
            # do nothing ....
            pass
        if selected_mode == 'mode3':
            ser.write(b"3")
            message = "The Mode is in Undocked"     
        if selected_mode == 'mode4':
            ser.write(b"4")
            message = "Full(Max) Power"            
    return render_template("index.html", message=message)


@app.route('/send', methods=['POST'])
def send():
    get_values = request.form['string']
    get_values1 = bytes(get_values, 'utf-8')
    ser.write(get_values1)
    return 'Sent Value: ' + get_values

if __name__=="__main__":
    http_server=WSGIServer(("127.0.0.1",8080), app)
    http_server.serve_forever()
