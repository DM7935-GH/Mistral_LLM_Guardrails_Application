# Mistral LLM Guardrails Application
This application uses a microservices architecture in order to implement simple customisable guardrails for the Mistral LLM.

### Overview
Guardrails are safety measures used to control the inputs and outputs of LLMs (Large Language Models). Common uses include preventing harmful content from being generated, or sensitive information from being revealed. This application enables the creation, modification, and deletion of guardrails that modify the inputs and outputs of the Mistral LLM. It uses a microservices architecture, with each service implemented as a local RESTful API.

### Implementation
Each guardrail consists of a regular expression that specifies what (within the LLM input/output) should be replaced, and a replacement string that specifies what to replace it with. For example, the guardrail {"cat", "fox"} would result in "The cat sat on the mat" being transformed into "The fox sat on the mat".  

The application consists of the following three microservices, each of which are run using Flask:
- LLM service - Sends input prompts to the Mistral LLM and returns the responses as outputs.
- Guardrails service - Used to create, update, and delete guardrails. A Firebase realtime database is used to store guardrails (in JSON tree format). Note that the database specified by the URL within `firebase_database.py` is currently set to private and cannot be used.
- Auberge service - Combines the functionality of the other two services by comparing the LLM inputs and outputs to the current set of guardrails.

 ### Repository Contents
- `mistral.py` - Makes API calls to the Mistral LLM and receives its responses.
- `llm.py` - Uses `mistral.py` to provide the LLM service.
- `firebase_database.py` - Communicates with the Firebase database.
- `guardrails.py` - Uses `firebase_database.py` to provide the guardrails service.
- `auberge.py` - Uses the other modules to provide the Auberge service.
- `tests.py` - Contains Python unit tests for assessing the individual and combined functionality of the microservices.
