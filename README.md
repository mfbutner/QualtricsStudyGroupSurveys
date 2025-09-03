# QualtricsStudyGroupSurveys
A program for creating study group surveys administered through Qualtrics

- Run the app with ```streamlit run main.py```
- Build docker image with: ```docker build -t qualtrics_app .```
- Run docker image with: ```docker run --rm -p 8501:8501 --env-file .env qualtrics_app```
