# 🌐 CodePhoenix Frontend

A modern web interface for GitHub Security Scanner with intelligent data type detection.

## 📁 Project Structure

```bash
codephoenix-frontend/
├── frontend/              # Web interface files
│   ├── assets/           # Static assets
│   │   └── icons/       # Icons and images
│   ├── js/              # JavaScript files
│   │   ├── app.js       # Main application logic
│   │   └── bridge.js    # Scanner bridge
│   ├── css/             # CSS files (if needed)
│   └── index.html       # Main HTML file
├── scripts/             # Shell scripts
│   └── serve.sh        # Frontend server script
└── README.md           # This file

# Required companion repository
scanner/                # Backend scanner (separate repository)
└── ...                # Scanner files
```

## 🚀 Quick Start

### 1. Clone Both Repositories

```bash
# Create a parent directory
mkdir github-scanner
cd github-scanner

# Clone the frontend (this repository)
git clone https://github.com/your-username/codephoenix-frontend

# Clone the backend scanner
git clone https://github.com/LeuAlmeida/codephoenix-threat-hunting scanner
```

### 2. Start the Frontend

```bash
cd codephoenix-frontend
./scripts/serve.sh
```

### 3. Access the Application
Open [http://localhost:8080](http://localhost:8080) in your browser

## 📝 How to Use

### 1. Configure GitHub Token
- Go to [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
- Create a new token with `public_repo` permission
- Copy and paste the token into the "GitHub Token" field

### 2. Set Search Terms
Enter one or more search terms, separated by commas. Examples:
```
@company.com,github.com
ghp_,sk-,AKIA
api.company.com,mongodb://
```

### 3. Configure Advanced Options (Optional)
- Results per page (10-100)
- Number of pages to scan (1-34)
- Sleep time between requests (1-10 seconds)
- Date filters (optional)

### 4. Run the Scan
1. Click "Start Scan"
2. Copy the generated Python command
3. Open Terminal in the scanner directory
4. Paste and run the command
5. Wait for the scan to complete
6. Upload the results file (scan_results.json)

## 🔍 Supported Search Types

The scanner automatically detects and categorizes:
- **📧 Emails**: `user@company.com`
- **🌐 URLs**: `https://api.company.com`
- **🔑 Tokens**: `ghp_abc123...`
- **🗝️ API Keys**: `sk-abc123...`
- **☁️ AWS Keys**: `AKIA...`
- **🗄️ Database URLs**: `mongodb://...`

## 🛠️ Development

### Project Structure
```
frontend/
├── index.html          # Main interface
├── app.js             # Frontend logic
└── python_bridge.js   # Scanner bridge

serve.sh               # Frontend server script
```

### Customization
- **Colors**: Edit `tailwind.config` in `index.html`
- **UI**: Adjust components in `index.html`
- **Logic**: Modify behavior in `app.js`
- **Scanner Bridge**: Update integration in `python_bridge.js`

## 🐛 Troubleshooting

### Invalid Token
```bash
# Verify token format
echo $GITHUB_TOKEN | cut -c1-4  # Should show "ghp_"
```

### Command Not Found
```bash
# Make sure you're in the scanner directory
cd ../scanner
ls run_frontend_scan.py  # Should exist
```

### No Results Found
```bash
# Test with a common term
python run_frontend_scan.py \
  --token "your_token" \
  --search-terms "@gmail.com" \
  --pages 1
```

### Rate Limiting
```bash
# Increase delay between requests
python run_frontend_scan.py \
  --token "your_token" \
  --search-terms "your_term" \
  --sleep-time 5
```

## 🚀 Production Mode

For production deployment, consider:

1. **Web Server**: Use Nginx or Apache
2. **HTTPS**: SSL certificates
3. **Authentication**: Login system
4. **Rate Limiting**: Usage control

## 💫 Next Steps

- [ ] WebSocket for real-time results
- [ ] Results export (CSV, JSON)
- [ ] Scan history
- [ ] Metrics dashboard
- [ ] Integration with other APIs (GitLab, Bitbucket)
- [ ] Alert system
- [ ] Complete REST API

## 🔗 Related Projects

- [GitHub Threat Hunting Script](https://github.com/LeuAlmeida/codephoenix-threat-hunting) - The backend scanner used by this frontend

## 📄 License

This project is licensed under the MIT License. Use responsibly and respect GitHub's terms of service.

---

**CodePhoenix Frontend** - Modern GitHub Security Scanning 🔒 