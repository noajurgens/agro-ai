# Agro-AI
The goal of this Capstone project is to build trust among farmers in the application of artificial intelligence in agriculture. The aim is to achieve this by enabling users to interact with an active learning system. Through this interaction, users provide input to a machine learning algorithm and observe how their input influences the accuracy of the algorithm.

## Overview
This project, featuring a Python Flask application with a JavaScript frontend, offers a user-friendly interface for interacting with the active learning system and machine learning model. Key features include:
- Intuitive interface with clear instructions for easy navigation.
- Display of corn leaf images for classification.
- Dynamic evaluation of AI confidence level.
- Seamless integration of active learning.
- Option for model retraining based on user feedback.

Overall, the web application empowers users to actively contribute to improving AI-driven decision-making in agriculture, fostering trust and collaboration in the farming community.

## User Interaction with the Application
### Picture Classification Process
#### Initial Classification:
- The user is presented with 10 pictures of corn leaves.
- For each picture, the user decides whether the leaf is healthy or unhealthy and labels it accordingly.
  
#### AI Confidence Evaluation:
- After classifying the initial set of images, the AI evaluates its confidence level.
- If the AI's confidence is above 70%:
  - The user is directed to a results page where the AI showcases its classification for the remaining images.
  - Checkboxes are provided under the classified images, allowing the user to indicate disagreement with the AI's choices.
  - Upon selecting images where they disagree with the AI, the user can trigger a retraining of the model by hitting the "Retrain Model" button. This updates the model to classify the disagreed images opposite to the AI's choice.

#### Training Iteration:
- If the AI's confidence is below 70% after the initial 10 images:
  - A "Keep Training" button is available for the user to request another batch of images.
  - This additional training data aims to improve the AI's confidence level above 70%.

## Dataset and Algorithm Details
### Dataset
The dataset utilized in this project is made available by Cornell University Agricultural Experiment Station. It comprises 18,000 field images of maize leaves, some exhibiting symptoms of northern leaf blight. The images are divided into three sets based on the camera used: drone, boom camera, and handheld camera. Each image in the dataset is accompanied by "ground truth" annotations, indicating expert evaluations of health and disease (including regions considered blighted).

For this implementation, focus was on a subset of the dataset, specifically selecting 200 handheld images:
- 100 images representing healthy leaves (without blight)
- 100 images depicting unhealthy leaves (with blighted spots)

Fifteen features were extracted from the selected images for training the machine learning model.

### Machine Learning Algorithm: Random Forest
The chosen machine learning algorithm is the random forest model. Random forest is an ensemble learning method consisting of a collection of decision trees. Each decision tree is trained to recognize labels based on features most frequently associated with them. The final classification is determined through a voting mechanism among the decision trees.

Additionally, confidence in predictions is calculated using k-fold cross-validation.

## Recent Advances to the Project 
- Checking and submitting the checkboxes now initiates the active learning process.
- The checkbox/active learning flow has been seamlessly integrated into the general user experience flow.
- The professional diagnosis of plants as health "H" or blighted "B" now appears on the final results page.
- Simple yet impactful changes to the user interface to enhance usability and aesthetics.

## Setting Up the Project Locally
To run the application locally on your machine, follow these steps:
- Clone the project repository to your local machine using Git
- Navigate to the project directory in your terminal and try to run the app using the command 'python flask_app.py'
	- If any packages are missing, the terminal will display error messages indicating which packages need to be installed. Use 'pip' to install these packages
	- Once all dependencies and packages are installed, you can run the Flask application using the command 'python flask_app.py'
- Once the server is running, open a web browser and go to the localhost it's running on to access the application
- You should now be able to interact with the application's user interface and classify corn leaf images

By following these steps, you'll be able to set up and run the project locally on your machine. If you encounter any issues during the setup process, refer to the error messages in the terminal for guidance on resolving missing dependencies or other configuration issues.

