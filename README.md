# VulnApp - OWASP Top 5 Vulnerability Demonstration

⚠️ **WARNING: This application intentionally contains security vulnerabilities for educational purposes only. NEVER use these patterns in production!**

## Overview

VulnApp is a deliberately vulnerable Flask web application designed to demonstrate the **OWASP 2021 Top 5** most critical web application security risks. This project serves as an educational tool for:

- Security professionals learning about web vulnerabilities
- Developers understanding common security pitfalls
- Students studying application security
- Penetration testers practicing vulnerability identification

## OWASP 2021 Top 5 Vulnerabilities Demonstrated

### A01:2021 - Broken Access Control
- **Admin panel accessible without authentication** (`/admin`)
- **Direct object reference** vulnerabilities (`/users/<id>`)
- **Missing access control** checks on sensitive endpoints
- **Dashboard accessible** without proper authentication

### A02:2021 - Cryptographic Failures
- **Hardcoded secret key** in source code (`app.secret_key = "hardcoded-secret-123"`)
- **Plaintext password storage** in database
- **Exposed configuration** details (`/settings`)
- **Weak session management**

### A03:2021 - Injection
- **SQL injection** in login form (vulnerable query construction)
- **Cross-Site Scripting (XSS)** in user profiles
- **Server-Side Template Injection** possibilities
- **Command injection** endpoints (if implemented)

### A04:2021 - Insecure Design
- **Missing security controls** in application architecture
- **Poor authentication flow** design
- **Inadequate input validation**
- **Flawed business logic** in user access patterns

### A05:2021 - Security Misconfiguration
- **Debug mode enabled** in production (`app.config['DEBUG'] = True`)
- **Verbose error messages** exposing stack traces
- **Server-Side Request Forgery (SSRF)** in URL fetcher
- **Default configurations** and unnecessary features enabled

## Project Structure

```
vuln-webapp/
├── app.py                 # Main Flask application with vulnerabilities
├── requirements.txt       # Python dependencies
├── vulnerable.db         # SQLite database (created automatically)
├── templates/            # Jinja2 templates with Tailwind CSS
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage with vulnerability overview
│   ├── login.html        # Login page (SQL injection vulnerable)
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── admin.html        # Admin panel (no auth required)
│   ├── profile.html      # User profile (XSS vulnerable)
│   ├── search.html       # URL fetcher (SSRF vulnerable)
│   └── settings.html     # App settings (config exposure)
└── README.md            # This documentation
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Local Development Setup

1. **Clone or create the project directory:**
   ```bash
   mkdir vuln-webapp
   cd vuln-webapp
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   - Open browser to `http://localhost:5000`
   - The database will be created automatically on first run

### Deployment on Render (Free Tier)

1. **Push code to GitHub** (public repository required for free tier)

2. **Connect to Render:**
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub account
   - Create new Web Service

3. **Configure deployment:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Add `PORT` (automatically provided by Render)

4. **Deploy:** Your app will be available at `https://your-app-name.onrender.com`

## Usage & Testing

### Default Test Credentials

| Username | Password | Role  | Purpose |
|----------|----------|-------|---------|
| admin    | admin123 | admin | Admin user with elevated privileges |
| user1    | password | user  | Regular user account |
| test     | test123  | user  | Test user for demonstrations |

### Vulnerability Testing Guide

#### A01: Broken Access Control
1. **Direct Admin Access:**
   - Navigate directly to `/admin` without logging in
   - Observe full user database access

2. **Direct Object Reference:**
   - Access `/users/1`, `/users/2`, etc. without authentication
   - View other users' data

#### A02: Cryptographic Failures
1. **Exposed Secrets:**
   - Visit `/settings` to see hardcoded secret key
   - Check database for plaintext passwords

2. **Weak Session Management:**
   - Inspect cookies and session data
   - Test session hijacking scenarios

#### A03: Injection Attacks
1. **SQL Injection (Login Form):**
   ```sql
   Username: ' OR '1'='1' --
   Password: [anything]
   ```

   ```sql
   Username: admin'--
   Password: [leave empty]
   ```

   ```sql
   Username: ' UNION SELECT 1,username,password,email,role FROM users--
   Password: [anything]
   ```

2. **XSS (Profile Page):**
   ```html
   <script>alert('XSS Attack!');</script>
   ```

   ```html
   <img src=x onerror=alert('XSS')>
   ```

#### A05: Security Misconfiguration - SSRF
1. **Internal Service Access:**
   - URL: `http://localhost:5000`
   - URL: `http://127.0.0.1:22`
   - URL: `http://169.254.169.254/latest/meta-data/` (AWS metadata)

## Educational Value

This application demonstrates:

### Common Developer Mistakes
- Using string formatting in SQL queries
- Storing sensitive data in plaintext
- Missing authentication checks
- Exposing configuration details
- Running debug mode in production

### Security Best Practices (What NOT to do)
- ❌ Never use hardcoded secrets
- ❌ Never store passwords in plaintext
- ❌ Never skip input validation
- ❌ Never run debug mode in production
- ❌ Never expose internal configuration

### Remediation Examples
Each vulnerability includes comments explaining:
- Why it's dangerous
- How it can be exploited
- Proper secure alternatives
- Industry best practices

## Security Warnings

### ⚠️ CRITICAL - Production Safety

**NEVER deploy this application on:**
- Production servers
- Public-facing networks
- Shared hosting environments
- Corporate networks

**ONLY use this application for:**
- Local development testing
- Isolated lab environments
- Educational demonstrations
- Security training purposes

### Recommended Safe Usage

1. **Isolated Environment:** Run only on isolated VMs or containers
2. **Network Isolation:** Use private networks or localhost only
3. **Temporary Usage:** Shut down after each learning session
4. **No Real Data:** Never input actual personal or sensitive information

## Vulnerability Impact Examples

### Real-World Attack Scenarios

1. **Data Breach via SQL Injection:**
   - Attacker extracts entire user database
   - Plaintext passwords compromise user accounts
   - Lateral movement to other systems

2. **Admin Takeover via Access Control:**
   - Direct access to admin functions
   - User account manipulation
   - System configuration changes

3. **XSS-based Account Hijacking:**
   - Session cookie theft
   - User impersonation
   - Malicious payload distribution

## Learning Resources

### OWASP Resources
- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)

### Additional Vulnerable Applications
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)
- [DVWA (Damn Vulnerable Web Application)](https://dvwa.co.uk/)
- [Mutillidae](https://github.com/webpwnized/mutillidae)

## Contributing

This is an educational project. If you'd like to contribute:

1. **Add more vulnerabilities** from OWASP Top 10
2. **Improve documentation** and explanations
3. **Add security testing examples**
4. **Create tutorial content**

## License

This project is released under MIT License for educational purposes.

## Disclaimer

This application is provided "as is" for educational purposes only. The authors are not responsible for any misuse or damage caused by this software. Users assume all responsibility for testing in safe, isolated environments only.

---

**Remember: The goal is to learn secure development practices by understanding what NOT to do!**
