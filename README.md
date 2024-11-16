# FastAPI App base

Backend app based on FastAPI and PostgreSQL

## Building project

### 1. Download from github

```bash
git clone https://github.com/IvVlasov/todo_app
```

### 2. Install dependencies

```bash
cd todo_app
python3 -m venv .venv && source .venv/bin/activate
pip install .
pip install -e '.[code-quality]'
```

### 3. Start the app

> Launch from project root folder

Fill env from [example file](./env.template)
Default values provided in  [settings file](./backend/settings.py)


Required env parameters
```
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
APP_TOKEN=
JWT_SECRET_KEY=
JWT_ALGORITHM=
JWT_LIFETIME_MINUTES=
```

Run migrations
```bash
python migrate.py
```

Run app
```bash
uvicorn main:app
```

### Code quality

Install dependencies: `pip install -e '.[code-quality]'`  
  
##### Run code quality check

```bash
./code_quality_check.sh
```
#### Run tests

```bash
pytest
```
