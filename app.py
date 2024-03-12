from flask import Flask, render_template, request, jsonify
import json
import matplotlib.pyplot as plt

app = Flask(__name__)
STATIC_FOLDER = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        content = file.read()
        data = json.loads(content)

        if 'compare' in request.form:
            product_info = data.get('Produktinformationen')
            quality_tests = data.get('Qualitätsprüfungen')
            historical_data = data.get('HistorischeDaten')
            image_path = create_pie_chart(historical_data)
            return jsonify({'product_info': product_info, 'quality_tests': quality_tests, 'historical_data': historical_data, 'image_path': image_path})
        else:
            product_info = data.get('Produktinformationen')
            quality_tests = data.get('Qualitätsprüfungen')
            return jsonify({'product_info': product_info, 'quality_tests': quality_tests})

def create_pie_chart(historical_data):
    labels = ['Bestanden', 'Nicht bestanden']
    sizes = [0, 0]

    for prufung in historical_data['Prüfungen']['Einzelprüfungen']:
        for _, data in prufung.items():
            if data['Ergebnisse'] == 'Bestanden':
                sizes[0] += 1
            else:
                sizes[1] += 1

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    image_path = 'static/pie_chart.png'
    plt.title('Erfolg vergangener Prüfungen')
    plt.savefig(image_path)
    plt.close()

    return image_path

if __name__ == '__main__':
    app.run(debug=True)
