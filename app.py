from flask import Flask, render_template, request
import metro

app = Flask(__name__)


@app.route('/')
def forma():
    return render_template('forma.html')

@app.route('/plan')
def plan():
    return render_template('plan.html', plan=metro.plan)

@app.route('/submit', methods=['POST'])
def submit():
    hour = int(request.form.get('hour'))
    min = int(request.form.get('min'))
    ss = request.form.get('ss')
    es = request.form.get('es')

    metro.add_task(ss, es, hour, min)

    return render_template('sumbit.html', plan=metro.plan)

if __name__ == '__main__':
    app.run(debug=True)
