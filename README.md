## AI Act Law Retrieval Augmented Generation with LangChain

This project provides a conversational interface for users to ask questions about the AI Act Law using a collection of PDFs as reference. It leverages the following technologies:

* **Backend (FastAPI):**
    * Processes uploaded PDFs and extracts text.
    * Creates a vector store for efficient retrieval of relevant information from the extracted text.
    * Uses LangChain to handle the conversation flow and generate responses to user queries.
    * LangChain integrates retrieval augmentation, where retrieved information from the PDFs is used to contextually tailor the responses from the large language model (LLM).
* **Frontend (Streamlit):**
    * Provides a user-friendly chat interface for users to ask questions.
    * Uploads and processes PDFs through the backend API.
    * Displays the conversation history and the LLM's generated responses.

**Key Features:**

* **Expertise in AI Act Law:** The LLM was given information related to the AI Act Law, making it a valuable resource for users seeking expert advice on the topic. You can modify the `prompt.py` file + the PDFs you upload to serve a different task 
* **Retrieval Augmentation:** By incorporating retrieved information from the uploaded PDFs, the LLM can generate more focused and relevant responses to user queries.
* **Conversational Interface:** The chat-based interface allows for a natural and interactive way to explore the information contained within the PDFs.

**Dockerized Deployment:**

The project utilizes Docker Compose to manage and deploy the backend and frontend services as a single application. This allows for easy deployment and ensures all required components run seamlessly together.

**CI/CD Pipeline**

This project leverages GitHub Actions to automate code linting on every push to the repository. The `.github/workflows/main.yml` file defines a workflow that runs a  job named `superlint`.

**Superlinter Job:**

* **Checkout:** This job begins by checking out the code from the repository.
* **Uses:** It uses the `actions/checkout@v6` action to perform the checkout step.
* **Runs on:** The job runs on the `ubuntu-latest` runner environment provided by GitHub Actions.
* **Steps:**
    * **Use SuperLinter:** This step installs and utilizes the `super-linter` action to perform code linting.
        * `uses:github/super-linter@v6`: This line specifies the SuperLinter action and its version.
    * **Lint:** The SuperLinter action runs various linters specific to the project's programming languages (e.g., Pylint for Python) to identify potential code issues.

**Getting Started:**

1. Create a `.env` file in your project directory and add your OpenAI API key: `OPENAI_API_KEY=your_openai_api_key`.
2. Run `docker-compose up -d` to build and start the application.
3. Access the application in your web browser at `http://localhost:8501`.

**Note:**

* You will need an OpenAI API key to use the LLM.
* This is a basic example, and further customization might be required depending on your specific needs.

This project demonstrates a powerful approach for combining retrieval and generation tasks to create an informative and interactive user experience.
