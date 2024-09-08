from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import threading

SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  
servo.start(0)

def liberar_racao():
    servo.ChangeDutyCycle(7)
    time.sleep(1)
    servo.ChangeDutyCycle(2)
    time.sleep(1)

def alimentar_automaticamente():
    while True:
        hora_atual = time.localtime().tm_hour
        minuto_atual = time.localtime().tm_min

        for horario in horarios_de_alimentacao:
            if hora_atual == horario[0] and minuto_atual == horario[1]:
                liberar_racao()
                time.sleep(60)

        time.sleep(30)

horarios_de_alimentacao = [(8, 0), (12, 0), (18, 0)]  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', horarios=horarios_de_alimentacao)

@app.route('/alimentar', methods=['POST'])
def alimentar():
    liberar_racao()
    return "Ração liberada!"

@app.route('/atualizar_horarios', methods=['POST'])
def atualizar_horarios():
    global horarios_de_alimentacao
    novos_horarios = request.form.getlist('horarios')
    horarios_de_alimentacao = [tuple(map(int, h.split(':'))) for h in novos_horarios]
    return "Horários atualizados!"

if __name__ == "__main__":
    threading.Thread(target=alimentar_automaticamente, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
