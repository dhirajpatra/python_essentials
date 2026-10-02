uvicorn main:app --reload

# Create
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com","age":30}'

# List
curl http://localhost:8000/users

# Filter + paginate
curl "http://localhost:8000/users?min_age=25&limit=10&skip=0"

# Get one
curl http://localhost:8000/users/<id>

# Update
curl -X PATCH http://localhost:8000/users/<id> \
  -H "Content-Type: application/json" \
  -d '{"age":31}'

# Delete
curl -X DELETE http://localhost:8000/users/<id>

# Stats (aggregation)
curl http://localhost:8000/users/stats/by-age