from flask import Flask, request
import firebase_database

app = Flask(__name__)


@app.route("/guardrails/<string:id>", methods=["PUT"])
def create_guardrail(id):
	request_js = request.get_json()
	status_code = firebase_database.add_gr_database(id, request_js)[0]
	empty = firebase_database.add_gr_database(id, request_js)[1] # This will always be {}
	return empty, status_code


@app.route("/guardrails/<string:id>", methods=["GET"])
def read_guardrail(id):
	status_code = firebase_database.read_gr_database(id)[0]
	guardrail = firebase_database.read_gr_database(id)[1]
	return guardrail, status_code


@app.route("/guardrails/<string:id>", methods=["DELETE"])
def delete_guardrail(id):
	status_code = firebase_database.add_gr_database(id)[0]
	empty = firebase_database.add_gr_database(id)[1] # This will always be {}
	return empty, status_code


@app.route("/guardrails", methods=["GET"])
def list_guardrails():
	status_code = firebase_database.list_gr_database(id)[0]
	guardrail_list = firebase_database.list_gr_database(id)[1]
	return guardrail_list, status_code


if __name__ == "__main__":
	app.run(host = "localhost", port=3001)