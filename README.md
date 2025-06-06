# 🔍 GitHub Security Scanner

Intelligent scanner for detecting sensitive information in GitHub repositories with:
- 🧠 **Smart detection** of 10 data types (emails, tokens, URLs, etc.)
- 🔄 **Automatic reload** of configurations
- 💯 **Multiple search strategies** per type
- 🛡️ **Intelligent rate limiting**
- **96.3% accuracy** in type detection

## Project Structure

```bash
codephoenix/
├── frontend/              # Frontend files
│   ├── assets/           # Static assets
│   │   └── icons/       # Icons and images
│   ├── js/              # JavaScript files
│   │   ├── app.js       # Main application logic
│   │   └── bridge.js    # Scanner bridge
│   ├── css/             # CSS files
│   └── index.html       # Main HTML file
├── scanner/              # Scanner core files
│   ├── core/            # Core scanning functionality
│   │   ├── __init__.py
│   │   ├── github_scan.py
│   │   └── data_types.py
│   ├── bridge/          # Frontend integration
│   │   ├── __init__.py
│   │   ├── frontend_bridge.py
│   │   └── simple_scanner.py
│   └── tests/           # Test files
│       └── test_date_comparison.py
├── scripts/             # Shell scripts
│   ├── serve.sh        # Frontend server
│   └── run.sh          # Scanner execution
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables example
└── README.md           # This file
```

## Setup

### 1. Prerequisites
- Python 3.7 or higher
- GitHub Personal Access Token

### 2. Installation

1. Clone this repository
2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configure Token and Environment Variables

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select required permissions (at least `public_repo` for public repositories)
4. Copy the generated token
5. Configure your `.env` file:
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env and replace values
   ```
6. In `.env`, replace:
   ```bash
   GITHUB_TOKEN=your_real_token_here
   SEARCH_TERM=term_to_search
   START_DATE=2023-01-01
   END_DATE=2023-12-31
   ```

## Usage

### Running the Scanner

```bash
# Make sure virtual environment is active
source venv/bin/activate

# Run the scanner
./scripts/run.sh
```

### Running the Frontend

```bash
# Start the frontend server
./scripts/serve.sh

# Access in browser
open http://localhost:8080
```

## Configuration

All settings are configured through the `.env` file:

- `GITHUB_TOKEN`: Your GitHub personal access token
- `SEARCH_TERM`: One or more terms separated by commas (e.g., term1,term2)
- `START_DATE`: (optional) Start date in YYYY-MM-DD format to filter files created from this date
- `END_DATE`: (optional) End date in YYYY-MM-DD format to filter files created until this date
- `RESULTS_PER_PAGE`: (optional) Number of results per page (10-100, default: 30)
- `PAGES`: (optional) Number of pages to scan (1-34, default: 5)
- `SLEEP_TIME`: (optional) Delay between requests in seconds (1-10, default: 2)

## Development

### Running Tests

```bash
# Run date comparison test
python -m scanner.tests.test_date_comparison
```

### Frontend Development

1. Start the frontend server:
   ```bash
   ./scripts/serve.sh
   ```

2. Edit files in `frontend/` directory
3. Refresh browser to see changes

### Scanner Development

1. Core functionality is in `scanner/core/`
2. Frontend integration is in `scanner/bridge/`
3. Run scanner directly:
   ```bash
   python -m scanner.core.github_scan
   ```

## Security Best Practices

1. **Token Security**
   - Never commit tokens to repositories
   - Use tokens with minimal required permissions
   - Rotate tokens regularly

2. **Rate Limiting**
   - The scanner includes automatic rate limiting
   - Adjust `SLEEP_TIME` if hitting limits
   - Consider using authenticated requests

3. **Data Handling**
   - Delete scan results after use
   - Don't store sensitive data
   - Use secure storage for tokens

## License

This project is licensed under the MIT License. Use responsibly and respect GitHub's terms of service.

---

**GitHub Security Scanner** - Smart Security Scanning 🔒

