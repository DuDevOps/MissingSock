from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/files/t.txt')
def show_file_t_txt():
    file = open("files/t.txt", "rb")
    data = file.readlines()[1:]
    file.close
    print(data)
    return str(data)

if __name__ == '__main__':
    app.run(port=50011)