# LUMA-K-
ai voice assistant

# To run Backend
uvicorn TaskManagement:app --reload

Task
|_ TaskManagement.py -- main fastapi
|_ firebase_config.py -- config firebase 
|_ models.py -- Task schema
|_ services
|  |__task_service.py -- CRUD task
|  |__ai_service.py -- function classify_task_text
|_ loaders
|  |__model_loader.py
|_ model
|_
