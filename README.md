# Text Summariser and Instagram Post Generator

This application fetches relevant articles based on a query, summarises the content, and then creates a compelling Instagram post based on the summarised content.

This idea was inspired by AIJason!

## Getting Started

Follow these steps to set up and run the Streamlit app on your local machine.

## Prerequisites

- Python (>=3.9)
- pip (Python package manager)

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/timooo-thy/text-summariser.git
   cd text-summariser

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   
3. Install the required packages:

   ```bash
   pip install -r requirements.txt

## Setup Environment Variables

1. Create a `.env` file in the root directory of the project.

2. Add your API tokens information to the `.env` file in the following format:
   SERP_API_KEY=your_serp_api_key
   OPENAI_API_KEY=your_openai_api_key

3. Make sure to include `.env` in your `.gitignore` file to keep your sensitive information secure.

## Running the App

1. Open a terminal and navigate to the project directory.

2. Activate the virtual environment if you created one:

   ```bash
   source venv/bin/activate # On Windows: venv\Scripts\activate
   
3. Run the Streamlit app:

   ```bash
   streamlit run app.py

4. The app should open in your default web browser.

## Deploying to Production

For deploying the app to a production environment, consider deploying from Streamlit. Be sure to adjust configurations and follow deployment instructions for your chosen platform.

## Author

©Timothy Lee
