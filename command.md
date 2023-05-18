# Command

pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn python-dotenv

docker-compose build
docker-compose up -d
docker-compose run app alembic revision --autogenerate -m "new migration"
docker-compose run app alembic upgrade head

pip install pyjwt 'passlib[bcrypt]'
