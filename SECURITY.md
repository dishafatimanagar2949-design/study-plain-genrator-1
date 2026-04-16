# Security Best Practices

Follow these guidelines to keep your application secure:

## 🔐 Environment Variables

✅ **DO**:
- Store `SECRET_KEY` in environment variables
- Use strong, random SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- Store database credentials in `.env`
- Use `.env.example` as template (no secrets in it)

❌ **DON'T**:
- Hardcode secrets in `app.py`
- Commit `.env` file to git
- Use weak secrets or default values
- Share your `.env` file with anyone

## 🛡️ Authentication

✅ **DO**:
- Validate all user inputs
- Use HTTPS in production (Vercel handles this)
- Implement rate limiting for login attempts
- Log authentication events

❌ **DON'T**:
- Store plaintext passwords (hash them properly)
- Accept SQL injection inputs
- Allow weak passwords
- Forget to validate form data

## 🔒 Database Security

✅ **DO**:
- Use parameterized queries (already done in `app.py`)
- Limit database access
- Backup regularly
- Encrypt sensitive data

❌ **DON'T**:
- Use string concatenation for SQL queries
- Store sensitive data unencrypted
- Skip database backups
- Expose database credentials

## 🚀 Deployment Security

**On Vercel**:
1. Always use production settings
2. Set `FLASK_DEBUG=False` in production
3. Use strong `SECRET_KEY`
4. Enable two-factor authentication on Vercel account
5. Monitor Vercel logs for suspicious activity

**On GitHub**:
1. Keep repository private if needed
2. Use SSH keys instead of passwords
3. Enable branch protection rules
4. Review pull requests carefully
5. Monitor access logs

## 📝 Code Security

- Use security headers (X-Frame-Options, CSP)
- Validate file uploads
- Sanitize user inputs
- Keep dependencies updated: `pip list --outdated`
- Run security checks: `pip install safety && safety check`

## 🔄 Regular Maintenance

- Update Flask: `pip install --upgrade flask`
- Update scikit-learn: `pip install --upgrade scikit-learn`
- Review requirements.txt for vulnerabilities
- Check for security advisories

## Example: Generating Secure SECRET_KEY

```python
# Run this once and add to .env
import secrets
secret_key = secrets.token_hex(32)
print(f"Add to .env: SECRET_KEY={secret_key}")
```

Output example:
```
Add to .env: SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/security/)
- [Python Security](https://python.readthedocs.io/en/latest/library/security_warnings.html)

---

**Remember**: Security is an ongoing process, not a one-time setup!
