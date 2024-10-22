import os
import re


# Ensure the base folder exists
base_folder = "generated_files"
os.makedirs(base_folder, exist_ok=True)

def extract_and_save_code(response: str):
    # Folder structure regex to identify file paths
    folder_file_pattern = re.compile(r'#### ([\w/]+\.py|requirements\.txt)\n```(?:python|plaintext)?\n(.*?)```', re.DOTALL)

    # Extract each file's path and its code content
    matches = folder_file_pattern.findall(response)

    for match in matches:
        file_path = match[0]  # File path, e.g., 'app/main.py'
        file_content = match[1]  # File content

        # Create the necessary folder structure
        folder = os.path.dirname(file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        # Add this line inside the function where the file path is used.
        full_file_path = os.path.join(base_folder, file_path)

        # Write the file with its content
        with open(full_file_path, 'w') as f:
            f.write(file_content)

# Example usage:
response_string = """{
  "text": "Certainly! Below is the fully functional code for each file in the specified folder structure for a FastAPI application that handles user registration and login, along with the necessary packages and implementations.\n\n### Folder Structure\n```\napp/\n    __init__.py\n    main.py\nmodels/\n    __init__.py\n    user.py\nschemas/\n    __init__.py\n    user.py\nroutes/\n    __init__.py\n    auth.py\ndatabase.py\nrequirements.txt\n```\n\n### Code Implementation\n\n#### requirements.txt\n```plaintext\nfastapi\nuvicorn\nsqlalchemy\npydantic\nbcrypt\ndatabases\n```\n\n#### app/__init__.py\n```python\n# This file is intentionally left blank.\n```\n\n#### app/main.py\n```python\nfrom fastapi import FastAPI\nfrom routes.auth import router as auth_router\nfrom database import database, metadata\n\napp = FastAPI()\n\napp.include_router(auth_router)\n\n@app.on_event(\"startup\")\nasync def startup():\n    # Connect to the database\n    await database.connect()\n\n@app.on_event(\"shutdown\")\nasync def shutdown():\n    # Disconnect from the database\n    await database.disconnect()\n```\n\n#### models/__init__.py\n```python\n# This file is intentionally left blank.\n```\n\n#### models/user.py\n```python\nfrom sqlalchemy import Column, Integer, String\nfrom database import metadata, database\n\nclass User:\n    __tablename__ = \"users\"\n    \n    id = Column(Integer, primary_key=True, index=True)\n    name = Column(String(length=50), index=True)\n    email = Column(String(length=100), unique=True, index=True)\n    password = Column(String(length=100))\n\n# Create the table (this should be done using migrations in production)\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker\n\nengine = create_engine('sqlite:///./test.db')\nmetadata.create_all(engine)\n```\n\n#### schemas/__init__.py\n```python\n# This file is intentionally left blank.\n```\n\n#### schemas/user.py\n```python\nfrom pydantic import BaseModel, EmailStr\n\nclass UserCreate(BaseModel):\n    name: str\n    email: EmailStr\n    password: str\n\nclass UserResponse(BaseModel):\n    id: int\n    name: str\n    email: EmailStr\n\n    class Config:\n        orm_mode = True\n```\n\n#### routes/__init__.py\n```python\n# This file is intentionally left blank.\n```\n\n#### routes/auth.py\n```python\nfrom fastapi import APIRouter, HTTPException\nfrom sqlalchemy import select\nfrom sqlalchemy.orm import Session\nfrom models.user import User\nfrom schemas.user import UserCreate, UserResponse\nfrom database import database\nimport bcrypt\n\nrouter = APIRouter()\n\n@router.post(\"/register\", response_model=UserResponse)\nasync def register_user(user: UserCreate):\n    query = select(User).where(User.email == user.email)\n    existing_user = await database.fetch_one(query)\n    \n    if existing_user:\n        raise HTTPException(status_code=400, detail=\"Email already registered\")\n    \n    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())\n    new_user = User(name=user.name, email=user.email, password=hashed_password.decode('utf-8'))\n    \n    query = User.__table__.insert().values(name=user.name, email=user.email, password=new_user.password)\n    await database.execute(query)\n    \n    return new_user\n\n@router.post(\"/login\")\nasync def login_user(user: UserCreate):\n    query = select(User).where(User.email == user.email)\n    existing_user = await database.fetch_one(query)\n\n    if not existing_user or not bcrypt.checkpw(user.password.encode('utf-8'), existing_user.password.encode('utf-8')):\n        raise HTTPException(status_code=400, detail=\"Invalid credentials\")\n\n    return {\"message\": \"Login successful\"}\n```\n\n#### database.py\n```python\nfrom sqlalchemy import create_engine, MetaData\nfrom databases import Database\n\nDATABASE_URL = \"sqlite:///./test.db\"\n\ndatabase = Database(DATABASE_URL)\nmetadata = MetaData()\n\n# Create an engine\nengine = create_engine(DATABASE_URL)\n\n# Create all tables\nmetadata.create_all(engine)\n```\n\n### Instructions to Run\n1. Ensure you have Python and pip installed.\n2. Create a virtual environment and activate it (optional but recommended).\n3. Install the required packages:\n   ```sh\n   pip install -r requirements.txt\n   ```\n4. Run the FastAPI application:\n   ```sh\n   uvicorn app.main:app --reload\n   ```\n5. Access the API documentation at `http://127.0.0.1:8000/docs`.\n\nThis code creates a basic user registration and login system with password hashing using bcrypt. It uses SQLAlchemy for database interactions and Pydantic for request validation. Adjust the `DATABASE_URL` in `database.py` according to your database configuration for production use."
}"""
extract_and_save_code(response_string)
