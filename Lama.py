import os
from octoai.client import OctoAI
from octoai.text_gen import ChatMessage
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_success = load_dotenv(dotenv_path)

# Replace with your actual API key
llama_api_key = os.getenv('LLAMA_API_KEY')

client = OctoAI(api_key=llama_api_key)

def task_prompt(semester, subject):
    if subject == "AI":
        return f""" 
            Generate a new and unique task for {semester} semester Bachelor of AI students. 
            As a responsible AI Task Manager, your role is to develop an AI-related task that involves implementing a machine learning or deep learning algorithm, 
            using Python and relevant libraries (e.g., TensorFlow, PyTorch). The task should include:
            <h1>Title:</h1> 
            <h2>subheadings</h2>
            Data Preprocessing: Provide a dataset and require students to perform necessary data cleaning, normalization, and feature engineering.
            Model Training: Instruct students to build and train a machine learning or deep learning model suitable for the given problem.
            Evaluation: Guide students to evaluate their model using appropriate metrics and validation techniques.
            Interpretation of Results: Require students to analyze and interpret the results, discussing the model’s performance and any potential improvements.
            
            Ensure the task complexity is appropriate for {semester} semester students and aligns with current industry standards and practices.
            Format the task with HTML tags, using `<h1>` for the title, `<h2>` for subheadings.
        """
    elif subject == "Backend":
        return f"""
            Generate a new and unique task for {semester} semester Bachelor of Computer Science students specializing in backend development.
            As a responsible Backend Development Task Manager, your role is to create a backend development task that requires building or extending a 
            web application using Python and Flask. The task should include:
            <h1>Title:</h1> 
            <h2>subheadings</h2>
            Setting up Routes: Define endpoints for the application and require students to implement the necessary route handling.
            Handling Requests and Responses: Instruct students to process incoming requests, perform necessary logic, and return appropriate responses.
            Database Integration: Guide students to integrate a SQLAlchemy database, including creating models and performing CRUD operations.
            Authentication and Authorization: Require students to implement user authentication and authorization mechanisms to secure the application.
            
            Ensure the task complexity is appropriate for {semester} semester students and aligns with current industry standards and practices.
            Format the task with HTML tags, using `<h1>` for the title, `<h2>` for subheadings.
        """
    elif subject == "Frontend":
        return f"""
            Generate a new and unique task for {semester} semester Bachelor of Computer Science students specializing in frontend development.
            As a responsible Frontend Development Task Manager, your role is to design a frontend development task that involves creating a responsive
            and interactive user interface using HTML, CSS, and JavaScript. The task should include:
            <h1>Title:</h1> 
            <h2>subheadings</h2>
            Designing Web Pages: Provide a design mockup or requirements for students to create web pages using HTML and CSS.
            Implementing User Interactions: Instruct students to add interactivity using JavaScript, enhancing user experience.
            Using a Frontend Framework: Optionally guide students to use a frontend framework like React or Vue.js to build more complex functionality.
            Responsiveness: Ensure students make the web pages responsive and usable on various devices and screen sizes.
           
            Ensure the task complexity is appropriate for {semester} semester students and aligns with current industry standards and practices.
            Format the task with HTML tags, using `<h1>` for the title, `<h2>` for subheadings.
        """

def task_manager(semester, subject):
    completion = client.text_gen.create_chat_completion(
        max_tokens=131072,
        messages=[
            ChatMessage(
                role="system",
                content=task_prompt(semester, subject),
            ),
            ChatMessage(
                role="user",
                content=f"semester: {semester}\nsubject: {subject}",
            )
        ],
        model="meta-llama-3.1-405b-instruct",
        presence_penalty=0,
        temperature=0,
    )
    return completion.choices[0].message.content
def evaluator_prompt(semester, task, subject):
    if subject == "AI":
        return f"""
            Evaluate the completed tasks submitted by {semester} semester Bachelor of AI students. As a responsible AI Task Evaluator, 
            your role is to assess the correctness and efficiency of the implemented algorithm. The evaluation criteria should include:

            Algorithm Implementation: Assess the correctness, efficiency, and innovation of the implemented machine learning or deep learning algorithm.
            Data Preprocessing: Evaluate the quality of data cleaning, normalization, and feature engineering.
            Model Performance: Review the performance metrics of the model, ensuring appropriate metrics and validation techniques were used.
            Result Interpretation: Examine the clarity and insightfulness of the result interpretation, 
                including discussion on model performance and potential improvements.
            Code Quality: Consider code quality, proper use of libraries, and adherence to best practices.
            Provide constructive feedback highlighting strengths and areas for improvement, ensuring the evaluation is thorough and fair, 
            but do not give code suggestion you can generate the evaluation only in english language.
            considering the student's semester level and the complexity of the task.
            Use the following format for the report card:
            ### Subject: 

            | Task     | Remarks        |
            |----------|----------------|
            | 1        | remarks        | 
            | 2        | remarks        | 

            **remarks:** satisfactory or need improvement

            ### Analysis
            - Overall performance:
            - Areas for Improvement:

            **Task**: {task}
        """
    elif subject == "Backend":
        return f"""
            Evaluate the completed tasks submitted by {semester} semester Bachelor of Computer Science students specializing in backend development.
            As the Backend Development Task Evaluator, your role is to review the functionality and robustness of the web application. 
            The evaluation criteria should include:

            Route Handling: Assess the correctness and efficiency of the implemented endpoints and route handling.
            Request and Response Processing: Evaluate the logic and correctness of request processing and response generation.
            Database Integration: Review the integration and use of the SQLAlchemy database, including model creation and CRUD operations.
            Authentication and Authorization: Examine the security measures implemented for user authentication and authorization.
            Code Organization: Consider the overall code organization, cleanliness, and adherence to Flask best practices.
            
            Provide constructive feedback highlighting strengths and areas for improvement, ensuring the evaluation is thorough and fair, 
            but do not give code suggestion you can generate the evaluation only in english language.
            considering the student's semester level and the complexity of the task.
            Use the following format for the report card:
            ### Subject: 

            | Task     | Remarks        |
            |----------|----------------|
            | 1        | remarks        | 
            | 2        | remarks        | 

            **remarks:** satisfactory or need improvement

            ### Analysis
            - Overall performance:
            - Areas for Improvement:
            **Task**: {task}
        """
    elif subject == "Frontend":
        return f"""
            Evaluate the completed tasks submitted by {semester} semester Bachelor of Computer Science students specializing in frontend development. 
            As a responsible Frontend Development Task Evaluator, your role is to examine the design and responsiveness of the user interface.
            The evaluation criteria should include:

            Design Quality: Assess the design of web pages, including layout, aesthetics, and adherence to provided mockups or requirements.
            User Interactions: Evaluate the implementation and quality of user interactions using JavaScript.
            Frontend Framework Usage: If applicable, review the use of a frontend framework (e.g., React, Vue.js) to build complex functionality.
            Responsiveness: Examine the responsiveness and usability of the web pages across various devices and screen sizes.
            Code Cleanliness: Consider the overall code cleanliness, organization, and adherence to HTML, CSS, and JavaScript best practices.
            
            Provide constructive feedback highlighting strengths and areas for improvement, ensuring the evaluation is thorough and fair, 
            but do not give code suggestion you can generate the evaluation only in english language.
            considering the student's semester level and the complexity of the task.
            Use the following format for the report card:          
            ### Subject: 

            | Task     | Remarks        |
            |----------|----------------|
            | 1        | remarks        | 
            | 2        | remarks        | 

            **remarks:** satisfactory or need improvement

            ### Analysis
            - Overall performance:
            - Areas for Improvement:
            **Task**: {task}
        """


def task_evaluator(semester,task, subject, solved_text):
    completion = client.text_gen.create_chat_completion(
        max_tokens=131072,
        messages=[
            ChatMessage(
                role="system",
                content=evaluator_prompt(semester, task,subject),
            ),
            ChatMessage(
                role="user",
                content=f"solved task:\n{solved_text}",
            )
        ],
        model="meta-llama-3.1-405b-instruct",
        presence_penalty=0,
        temperature=0,
    )
    return completion.choices[0].message.content