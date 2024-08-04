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

This project leverages GitHub Actions to automate code linting on every push to the repository. The `.github/workflows/main.yml` file defines a workflow that runs the following jobs.

**1. check-code Job:**

* **Checkout:** This job begins by checking out the code from the repository.
* **Uses:** It uses the `actions/checkout@v3` action to perform the checkout step.
* **Runs on:** The job runs on the `ubuntu-latest` runner environment provided by GitHub Actions.
* **Steps:**
    * **Use PEP8 Action:** This step installs and utilizes the `PEP8 Action` action to perform code linting.
        * `uses:github/PEP8 Action@v1`: This line specifies the SuperLinter action and its version.

**2. build-and-push Job:**

* **Needs:** This job depends on the successful completion of the `check-code` job (`needs: check-code`). This enforces code quality checks before proceeding with building and pushing images.
* **Runs on:** This job runs on the `ubuntu-latest` runner environment.
* **Steps:**
    1. **Checkout code:** Identical to the `check-code` job, this step retrieves the code from the repository using `actions/checkout@v3`.
    2. **Create .env file:** This step creates a `.env` file within the `app` directory. It securely stores your OpenAI API key (`API_KEY`) using a secret (`{{ secrets.OPENAI_API_KEY }}`) to prevent exposure.
    3. **Set up Docker Buildx:** This step leverages the `docker/setup-buildx-action@v1` action to configure Docker Buildx, providing enhanced build capabilities (optional, adjust based on your needs).
    4. **Setup docker-compose:** This step utilizes the `KengoTODA/actions-setup-docker-compose@v1.2.2` action to set up Docker Compose within the workflow. It provides access to `docker-compose` commands within your workflow steps. The `GITHUB_TOKEN` secret is required for authentication purposes.
    5. **Login to DockerHub:** This step securely logs in to Docker Hub using the `docker/login-action@v1` action. It requires the `DOCKERHUB_USERNAME` environment variable (set elsewhere) and your Docker Hub token stored in the `DOCKERHUB_TOKEN` secret.
    6. **Build and push Docker images (working directory: app):**
        - **Verify directory (optional):** This line (`ls -la`) can be used for debugging purposes to confirm the working directory is set correctly.
        - **Build & push using docker-compose:** This primary approach utilizes `docker-compose build` and `docker-compose push` commands to build and push the images defined in your `docker-compose.yml` file.
        - **OR tag then push individually with docker (optional):** This section provides an alternative approach where you can comment out the above lines and uncomment these to tag and push each image separately using `docker tag` and `docker push` commands.
    7. **Verify pushed images (optional):** This step (`docker images`) can be used to verify the successfully pushed images to Docker Hub after the build and push process.

**Getting Started:**

1. Clone this repo to your local machine
2. Create a `.env` file in your project directory and add your OpenAI API key: `OPENAI_API_KEY=your_openai_api_key`.
3. Run `docker-compose up -d` to build and start the application.
4. Access the application in your web browser at `http://localhost:8501`.

**Note:**

* You will need an OpenAI API key to use the LLM.
* This is a basic example, and further customization might be required depending on your specific needs.

This project demonstrates a powerful approach for combining retrieval and generation tasks to create an informative and interactive user experience.
