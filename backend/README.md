# Kohyli-backend

FastAPI-based backend for the Kohyli project.

## Email Configuration

The backend sends order confirmation emails when orders are placed. Email sending is handled asynchronously using a background worker (arq).

### Setup Email

1. Configure SMTP settings in your `.env` file:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@kohyli.com
SMTP_FROM_NAME=Kohyli Bookstore
SMTP_USE_TLS=true
```

2. Start Redis (required for background tasks):

```bash
redis-server
```

3. Start the background worker to process email tasks:

```bash
python worker.py
```

4. Start the FastAPI backend:

```bash
just run-dev
```

### Email Features

- **Order Confirmation Emails**: Automatically sent when an order is successfully created
- **Background Processing**: Emails are queued and sent asynchronously to avoid blocking order creation
- **HTML Templates**: Professional HTML email templates with order details
- **Fallback**: If SMTP credentials are not configured, the system will log a warning but won't fail order creation

### Testing Email Locally

If you want to test email sending without a real SMTP server, you can use a service like [Mailtrap](https://mailtrap.io/) or run a local SMTP server:

```bash
# Install MailHog (simple SMTP testing server)
# Follow instructions at https://github.com/mailhog/MailHog

# Then configure your .env:
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USERNAME=
SMTP_PASSWORD=
```