from flask import Flask, render_template, url_for, request, redirect
import csv

app = Flask(__name__)


def write_to_file(data):
	with open('database.txt', mode='a') as database:
		name = data['name']
		email = data['email']
		category = data['category']
		message = data['message']
		try:
			if data['copy']:
				copy = True
		except KeyError as err:
			copy = False
		file = database.write(f'{name}, {email}, {category}, {copy}\n{message}\n')

def write_to_csv(data):
	with open('database.csv', mode='a', newline='') as database:
		name = data['name']
		email = data['email']
		category = data['category']
		message = data['message']
		try:
			if data['copy']:
				copy = True
		except KeyError as err:
			copy = False
		csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting= csv.QUOTE_MINIMAL)
		csv_writer.writerow([name, email, category, copy, message])


@app.route('/')
def main_index():
	return render_template('index.html')


@app.route('/<string:page>')
def my_index(page):
	page += '.html'
	return render_template(page)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
	if request.method == 'POST':
		try:
			data = request.form.to_dict()
			del data['human']
			name = data['name'].split()[0]
			write_to_csv(data)
			return render_template('form_submitted.html', name=name)
		except:
			return 'did not save'
	else:
		return 'Oh, no! Bad Form Submit!'