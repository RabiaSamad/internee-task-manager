# Internee Task Manager and Evaluator

**Internee Task Manager and Evaluator** is an innovative application designed to streamline the task management and evaluation process for university students, particularly those studying AI, backend, and frontend development. This app leverages the powerful LLaMA 3.1 model to generate and evaluate tasks, providing an automated solution for busy managers and effective learning opportunities for interns.

## Features

- **Automated Task Generation**: Generate tasks tailored to the intern's field of expertise (AI, Backend, Frontend) and current semester.
- **Code Evaluation**: Automatically evaluate the code submitted by interns based on the generated tasks.
- **Detailed Feedback**: Provide interns with detailed evaluation reports that highlight areas of improvement and strengths.
- **PDF Report Generation**: Generate downloadable PDF reports for interns to document their progress and share with managers.
- **Potential Integration**: The app has potential for integration with project management tools like Jira and Azure DevOps for seamless task tracking.

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Model**: LLaMA 3.1
- **PDF Generation**: ReportLab, PyPDF2
- **Environment Variables Management**: python-dotenv

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- pip (Python package installer)
- Git

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/RabiaSamad/InterneeTask_managment_and_evaluation.git
    cd InterneeTask_managment_and_evaluation
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up the environment variables. Create a `.streamlit/secrets.toml` file with your LLaMA API key:

    ```toml
    [general]
    LLAMA_API_KEY = "your_llama_api_key"
    ```

4. Run the application:

    ```sh
    streamlit run application1.py
    ```

## Responsible Use

We have adhered to Responsible Use Guidelines in the development of this application:

- **Ethical Use of AI**: Ensuring tasks and evaluations are fair and unbiased.
- **Data Privacy**: Protecting user data and maintaining confidentiality.
- **Transparency**: Providing clear information about task generation and evaluation processes.
- **Inclusive Design**: Ensuring the app is accessible and equitable for all users.

