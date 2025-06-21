# Oracle

Welcome to the Oracle repository! This project is a React application that allows users to explore various Street Fighter characters and their special moves.

![Oracle Interface](https://github.com/estudart/asimov-academy-oraculo/blob/main/my_oracle.png)

## Description

The Oracle project is a Python application that enables users to upload files from various sources, including YouTube, .pdf, and .txt formats. This functionality allows users to interact with the Agent and leverage the uploaded data for meaningful conversations and insights.

## Features

- Upload different types of files.
- Choose a given LLM model from your preference.
- Reset conversation history.
- Excel the power of AI on your daily tasks.

## Installation

To run the Oracle app locally, follow these steps:

1. Clone this repository to your local machine using:
    ```bash
    git clone https://github.com/estudart/asimov-academy-oraculo.git

2. Build the image from the Dockerfile:
    ```bash
    docker build -t my_oracle .

3. Run the image on a container:
    ```bash
    docker run \
    -p8501:8501 \
    -e AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxx \
    -e AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxx \
    -e AWS_DEFAULT_REGION=us-west-1 \
    my_oracle

4. Open your web browser and visit http://localhost:8501 to view the app.

## Usage

- Upon launching the app, you'll see the chat interface of the Oracle Agent.
- On the side bar select upload files and select the LLM model.
- Chat with the Oracle and ask questions related to the uploaded file.

## Technologies Used

- Python
- LangChain
- Streamlit

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for new features, please open an issue on the [GitHub repository](https://github.com/estudart/asimov-academy-oraculo). Pull requests are also encouraged.

