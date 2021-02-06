from flask import Flask, request, render_template
from multiprocessing import Process, Lock
from pixels import cleantext, displaychar, scrolltext


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
lock = Lock()

scrolltext("❤️", delay=0.02)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrolltext', methods=['POST'])
def scroll_text():
    text = cleantext(request.form['text'])
    colour = request.form.get('colour', None)
    delay = request.form.get('delay', 0.05)
    try:
        delay = float(delay)
    except Exception:
        delay = 0.05
    process = Process(target=locked_scrolltext, args=(lock, text, colour, delay))
    process.start()
    return text + "\n"


@app.route('/displaychar', methods=['POST'])
def show_char():
    char = cleantext(request.form['char'])[0]
    colour = request.form.get('colour', None)
    process = Process(target=locked_displaychar, args=(lock, char, colour))
    process.start()
    return char + "\n"


def locked_scrolltext(lock, text, colour, delay):
    lock.acquire()
    try:
        scrolltext(text, colour, delay)
    finally:
        lock.release()


def locked_displaychar(lock, char, colour):
    lock.acquire()
    try:
        displaychar(char, colour)
    finally:
        lock.release()
