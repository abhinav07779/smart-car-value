# 🚗 Car Price Prediction Backend - Setup for Other Devices

## 🚨 **Quick Fix for Backend Not Working on Other Devices**

### **Prerequisites**
- Python 3.8 or higher
- Internet connection for downloading dependencies

### **Step 1: Check Python Version**
```bash
python --version
# Should show Python 3.8+ (e.g., Python 3.9.7, Python 3.11.2, etc.)
```

If Python version is too old, install Python 3.8+ from [python.org](https://python.org)

### **Step 2: Run Automated Setup**
```bash
python setup_other_device.py
```

This script will:
- ✅ Check Python version
- ✅ Install all dependencies
- ✅ Verify model files
- ✅ Test backend startup
- ✅ Create startup script

### **Step 3: Start the Backend**
```bash
python start_backend.py
```

### **Step 4: Test the API**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test main endpoint
curl http://localhost:8000/

# View API documentation
# Open browser: http://localhost:8000/docs
```

---

## 🔧 **Manual Setup (If Automated Setup Fails)**

### **Step 1: Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### **Step 2: Verify Model Files**
```bash
ls backend/models/
# Should show:
# - model.joblib
# - preprocessor.joblib
# - model_info.json
```

### **Step 3: Start Backend**
```bash
# Option 1: Using start script
python start.py

# Option 2: Direct uvicorn command
uvicorn backend.app:app --host 0.0.0.0 --port 8000

# Option 3: From backend directory
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 🐛 **Common Issues & Solutions**

### **Issue 1: "Python not found"**
**Solution:**
- Install Python from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation
- Restart command prompt/terminal

### **Issue 2: "pip not found"**
**Solution:**
```bash
# On Windows
python -m ensurepip --upgrade

# On Mac/Linux
sudo apt-get install python3-pip  # Ubuntu/Debian
brew install python3              # macOS
```

### **Issue 3: "Module not found" errors**
**Solution:**
```bash
# Install dependencies
pip install -r backend/requirements.txt

# If that fails, install individually:
pip install fastapi==0.115.5
pip install uvicorn[standard]==0.32.0
pip install pydantic==2.9.2
pip install pandas==2.2.3
pip install scikit-learn==1.5.2
pip install joblib==1.4.2
pip install numpy==2.1.3
```

### **Issue 4: "Model artifacts not found"**
**Solution:**
- Ensure `backend/models/` directory exists
- Check that all 3 files are present:
  - `model.joblib`
  - `preprocessor.joblib`
  - `model_info.json`

### **Issue 5: "Port already in use"**
**Solution:**
```bash
# Use different port
uvicorn backend.app:app --host 0.0.0.0 --port 8001

# Or kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### **Issue 6: "Permission denied"**
**Solution:**
```bash
# On Mac/Linux, use sudo if needed
sudo pip install -r backend/requirements.txt

# Or use user installation
pip install --user -r backend/requirements.txt
```

---

## 🌐 **Network Access (For Other Devices to Connect)**

### **Allow External Access**
The backend is configured to accept connections from other devices on your network.

**To access from another device:**
1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux
   ifconfig
   ```

2. Access from other device:
   ```
   http://YOUR_IP_ADDRESS:8000
   ```

### **Firewall Configuration**
**Windows:**
- Open Windows Defender Firewall
- Allow Python through firewall
- Or temporarily disable firewall for testing

**Mac:**
- System Preferences → Security & Privacy → Firewall
- Allow Python through firewall

**Linux:**
```bash
# Ubuntu/Debian
sudo ufw allow 8000

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

---

## 📱 **Testing from Mobile/Other Devices**

### **Test Health Endpoint**
```
http://YOUR_IP_ADDRESS:8000/health
```
Should return: `{"status":"ok"}`

### **Test Main API**
```
http://YOUR_IP_ADDRESS:8000/
```
Should return API information

### **View API Documentation**
```
http://YOUR_IP_ADDRESS:8000/docs
```
Interactive API documentation

---

## 🚀 **Production Deployment**

For production deployment, consider:
- **Railway**: Free hosting for Python apps
- **Render**: Free tier available
- **Heroku**: Free tier (limited)
- **DigitalOcean**: $5/month droplet

See `DEPLOYMENT.md` for detailed instructions.

---

## 📞 **Need Help?**

If you're still having issues:

1. **Run the diagnostic script:**
   ```bash
   python setup_other_device.py
   ```

2. **Check the logs:**
   - Look for error messages in the terminal
   - Check if all dependencies installed correctly

3. **Verify file structure:**
   ```
   your-project/
   ├── backend/
   │   ├── app.py
   │   ├── requirements.txt
   │   └── models/
   │       ├── model.joblib
   │       ├── preprocessor.joblib
   │       └── model_info.json
   ├── start.py
   └── setup_other_device.py
   ```

4. **Test step by step:**
   - Python version ✅
   - Dependencies installed ✅
   - Model files present ✅
   - Backend starts ✅
   - API responds ✅
