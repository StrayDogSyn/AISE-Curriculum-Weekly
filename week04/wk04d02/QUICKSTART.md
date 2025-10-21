# 🚀 Quick Start Guide - W4D2 Breakout Activity 1

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (1 minute)

```bash
# Navigate to the directory
cd week04/wk04d02

# Install required packages
pip install fastapi uvicorn pydantic
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Start the API Server (30 seconds)

```bash
python breakout03.py
```

You should see:

```text
============================================================
🚀 Starting Personal Information API...
============================================================

📖 Swagger Documentation: http://localhost:8000/docs
📚 ReDoc Documentation:   http://localhost:8000/redoc

🧪 Available Endpoints:
   GET    /               - API information
   GET    /health         - Health check
   GET    /me             - Get personal info
   PUT    /me             - Update personal info
   GET    /hobbies        - List all hobbies
   ...
```

### Step 3: Open Interactive Documentation (10 seconds)

Open your browser to: **<http://localhost:8000/docs>**

### Step 4: Try Your First API Call (1 minute)

In the Swagger UI:

1. Click on **GET /hobbies**
2. Click **"Try it out"**
3. Click **"Execute"**
4. See the response! 🎉

### Step 5: Test All Endpoints (2 minutes)

Try these in order:

1. **GET /me** - See your personal info
2. **POST /hobbies** - Create a new hobby
   - Example: `{"name": "Guitar", "skill_level": "beginner", "years_experience": 1}`
3. **GET /hobbies?skill_level=intermediate** - Filter hobbies
4. **PUT /hobbies/1** - Update a hobby
5. **GET /stats** - See statistics

## 🧪 Automated Testing (Optional)

Run the complete test suite:

```bash
# In a new terminal (keep the API running)
python test_api.py
```

Expected output:

```text
🎯🎯🎯... W4D2 BREAKOUT ACTIVITY 1 - API TEST SUITE ...🎯🎯🎯
============================================================
  TEST 1: Root Endpoint
============================================================
Status Code: 200
✅ PASSED
...
============================================================
  ✅ ALL TESTS PASSED!
============================================================
```

## 📋 Common Tasks

### View All Hobbies

```bash
curl http://localhost:8000/hobbies
```

### Add a New Hobby

```bash
curl -X POST http://localhost:8000/hobbies \
  -H "Content-Type: application/json" \
  -d '{"name":"Photography","skill_level":"beginner","years_experience":1}'
```

### Filter by Skill Level

```bash
curl "http://localhost:8000/hobbies?skill_level=intermediate"
```

### Get Statistics

```bash
curl http://localhost:8000/stats
```

## 🐛 Troubleshooting

### Problem: "Import fastapi could not be resolved"

**Solution**: Install the dependencies

```bash
pip install -r requirements.txt
```

### Problem: "Port 8000 is already in use"

**Solution**: Either:

1. Stop the other process using port 8000
2. Change the port in `breakout03.py` (line 705): `port=8001`

### Problem: "Connection refused"

**Solution**: Make sure the server is running

```bash
python breakout03.py
```

## 📚 Next Steps

1. ✅ Explore all endpoints in Swagger UI
2. ✅ Try the query parameters (skill_level, min_experience)
3. ✅ Run the automated test suite
4. ✅ Review the code in `breakout03.py`
5. ✅ Read the full documentation in `README.md`

## 🎓 Learning Resources

- **Full Documentation**: See `README.md`
- **Implementation Summary**: See `IMPLEMENTATION_SUMMARY.md`
- **Code**: See `breakout03.py` (extensively commented)
- **Tests**: See `test_api.py`

## 💡 Tips

- Use Swagger UI for visual testing (easiest)
- Use curl for command-line testing
- Use `test_api.py` for automated verification
- Check the terminal for server logs
- All responses are in JSON format

---

**Total Setup Time**: ~5 minutes  
**Ready to**: Build amazing APIs! 🚀
