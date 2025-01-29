# streamlit-gpt
Web application using Streamlit that serves an OpenAI LLM via API, integrates search functionality, and is deployed with Docker.

## Project Overview  

This project aims to provide a web-based interface for interacting with an advanced Large Language Model (LLM) from OpenAI via API. Built with Python and Streamlit, the application offers an intuitive and accessible way for users to generate text-based responses, enhanced by an integrated search functionality for improved information retrieval.  

By implementing this solution, users benefit from a streamlined and efficient method of accessing AI-powered assistance, whether for research, content generation, or customer support applications. The search capability allows for quick access to relevant insights, making the application more practical and user-friendly.  

To ensure scalability and portability, the entire project is containerized using Docker. This approach guarantees a controlled environment for deployment across different infrastructures, from local machines to cloud-based servers. The application follows best development practices, including modularized code structure, environment variable management for secure API key handling, and dependency management within a well-defined Docker environment.  

With this architecture, the project combines usability, performance, and flexibility, making AI-powered text generation easily accessible and deployable.  


```bash
    # Create the image
    docker build -t streamlit-gpt -f .\images\Dockerfile .

    # Create the container
    docker run --name streamlit-container -d -p 8501:8501 streamlit-gpt

    # Initialize the container
    docker start streamlit-container

    # Exec the terminal
    docker exec -it streamlit-container bash

    # Stop the container
    docker stop streamlit-container

    # Remove the container
    docker rm streamlit-container

```