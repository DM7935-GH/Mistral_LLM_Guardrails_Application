from flask import Flask, request
import mistral


app = Flask(__name__)

@app.route("/llm", methods=["POST"])
def llm_endpoint():
	request_js = request.get_json()

	if "prompt" not in request_js or type(request_js["prompt"]) != str:
		# If the JSON object does not have a string 'prompt' attribute
		return {}, 400
	else:
		response = mistral.new_prompt_mistral(request_js["prompt"])
		if type(response) == str:
			response_js = {"output" : response}
			return response_js, 200
		else:
			return {}, response

if __name__ == "__main__":
	app.run(host = "localhost", port=3000)