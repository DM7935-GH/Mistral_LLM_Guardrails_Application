from flask import Flask, request
import json
import re
import mistral
import firebase_database

app = Flask(__name__)


def reg_ex_replace(string : str, regx : str, sub : str):
	return re.sub(regx, sub, string)


@app.route("/auberge", methods=["POST"])
def auberge_endpoint():
	request_js = request.get_json()

	if "prompt" not in request_js or type(request_js["prompt"]) != str:
		# If the JSON object does not have a string 'prompt' attribute
		return {}, 400
	
	# Retrieve the guardrail IDs from the firebase database
	list_response = firebase_database.list_gr_database()

	if list_response[0] == 500:
		return {}, 500
	
	# Retrieve the guardrails from the firebase database
	guardrails = []
	for guardrail_id in list_response[1]:
		read_response = firebase_database.read_gr_database(guardrail_id)

		if read_response[0] != 200:
			return {}, read_response[0]
		
		guardrails.append(read_response[1])

	prompt = request_js["prompt"]

	# Sanitise the input prompt using the guardrails
	for guardrail in guardrails:
		prompt = reg_ex_replace(prompt, guardrail["regx"], guardrail["sub"])

	# Pass the santised input to the mistral LLM, and get its output
	llm_output = mistral.new_prompt_mistral(prompt)
	if type(llm_output) != str:
		return {}, llm_output
	
	# Sanitise the LLM output using the guardrails
	for guardrail in guardrails:
		llm_output = reg_ex_replace(llm_output, guardrail["regx"], guardrail["sub"])

	response_js = {"output" : llm_output}
	return response_js, 200


if __name__ == "__main__":
	app.run(host = "localhost", port=3002)