# 🔗 Connecting Frontend to Python Scanner

Guide to connect the CodePhoenix frontend to the GitHub Threat Hunting Script.

## 🎯 **Project Structure**

```bash
parent-directory/
├── codephoenix-frontend/    # Frontend repository
│   ├── frontend/           # Web interface files
│   │   ├── assets/        # Static assets
│   │   │   └── icons/    # Icons and images
│   │   ├── js/           # JavaScript files
│   │   │   ├── app.js    # Main application logic
│   │   │   └── bridge.js # Scanner bridge
│   │   ├── css/          # CSS files (if needed)
│   │   └── index.html    # Main HTML file
│   ├── scripts/          # Shell scripts
│   │   └── serve.sh     # Frontend server script
│   └── README.md         # Documentation
│
└── scanner/              # Backend repository
    ├── github_scan.py
    ├── run_frontend_scan.py
    └── requirements.txt
```

## 🚀 **Setup Instructions**

### 1. Clone Both Repositories
```bash
# Create a parent directory
mkdir github-scanner
cd github-scanner

# Clone frontend
git clone https://github.com/your-username/codephoenix-frontend

# Clone scanner
git clone https://github.com/LeuAlmeida/codephoenix-threat-hunting scanner
```

### 2. Setup Scanner
```bash
cd scanner

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Frontend
```bash
cd ../codephoenix-frontend
./serve.sh
```

## 🔄 **How It Works**

### Data Flow
```
[Frontend HTML] 
      ↓ (Generates command)
[Terminal/Python]
      ↓ (Executes scanner)
[GitHub API]
      ↓ (Returns results)
[JSON File]
      ↓ (Manual upload)
[Frontend HTML]
```

## 📝 **Usage Examples**

### Search for Emails
```bash
cd scanner
python run_frontend_scan.py \
  --token "ghp_your_token" \
  --search-terms "@google.com,@company.com" \
  --pages 3
```

### Search for Tokens
```bash
cd scanner
python run_frontend_scan.py \
  --token "ghp_your_token" \
  --search-terms "ghp_,sk-,AKIA" \
  --pages 2 \
  --sleep-time 3
```

### With Date Filter
```bash
cd scanner
python run_frontend_scan.py \
  --token "ghp_your_token" \
  --search-terms "@company.com" \
  --start-date "2020-01-01" \
  --end-date "2024-12-31"
```

## 🔧 **Available Parameters**

| Parameter | Required | Example | Description |
|-----------|----------|---------|-------------|
| `--token` | ✅ | `ghp_abc123` | GitHub Token |
| `--search-terms` | ✅ | `@email.com,token` | Comma-separated terms |
| `--results-per-page` | ❌ | `30` | Results per page (10-100) |
| `--pages` | ❌ | `5` | Number of pages (1-34) |
| `--sleep-time` | ❌ | `2` | Delay between requests (seconds) |
| `--start-date` | ❌ | `2020-01-01` | Start date (YYYY-MM-DD) |
| `--end-date` | ❌ | `2024-12-31` | End date (YYYY-MM-DD) |
| `--output-file` | ❌ | `results.json` | Output file |

## 🛡️ **Security Best Practices**

### ✅ **Do's**
- Keep scanner in a separate directory
- Use tokens with minimal permissions (`public_repo`)
- Delete results files after use
- Use virtual environment for Python

### ❌ **Don'ts**
- Never commit tokens to repositories
- Don't share results files containing sensitive data
- Don't expose scanner directory to web

## 🐛 **Troubleshooting**

### Scanner Not Found
```bash
# Make sure you're in the correct directory structure
ls ../scanner/run_frontend_scan.py
```

### Python Environment Issues
```bash
# Activate virtual environment
cd ../scanner
source venv/bin/activate
```

### Results File Not Found
```bash
# Check if file was created in scanner directory
cd ../scanner
ls scan_results.json
```

## 🚀 **Production Setup**

For production environments:

1. **Directory Structure**:
   ```bash
   /opt/codephoenix/
   ├── frontend/     # Served by web server
   └── scanner/      # Protected directory
   ```

2. **Web Server Configuration**:
   ```nginx
   # Nginx example
   location / {
       root /opt/codephoenix/frontend;
       try_files $uri $uri/ /index.html;
   }
   ```

3. **Security Measures**:
   - Place scanner outside web root
   - Use HTTPS
   - Implement authentication
   - Set proper file permissions

## 💡 **Tips**

1. **Quick Access**:
   ```bash
   # Add to your .bashrc or .zshrc
   alias cdscanner="cd /path/to/scanner"
   alias cdfrontend="cd /path/to/frontend"
   ```

2. **Result Management**:
   ```bash
   # Clean up old results
   find ../scanner -name "scan_results*.json" -mtime +7 -delete
   ```

3. **Scanner Updates**:
   ```bash
   # Update scanner
   cd ../scanner
   git pull origin main
   pip install -r requirements.txt
   ```

---

**This setup provides a secure and efficient way to use both components independently!** 🎯 