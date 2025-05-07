# Cloud Workspace Automation with Django, EC2, and Wetty

This project creates a cloud-based workspace that accepts a CSV file via an API, automatically provisions system users, sends out email notifications, and enables live interaction with a server environment using [Wetty](https://github.com/butlerx/wetty).


---

## 🧠 Key Technologies Used

- **Django** – for API and backend logic
- **EC2** – for cloud infrastructure
- **Wetty** – for web-based SSH access

---

## 🚀 Features

- Accepts a CSV file via HTTP POST
- Dynamically creates system users with:
  - Home directories
  - Group assignments based on department
  - Temporary secure passwords
  - Password reset enforcement on first login
- Sends out email credentials to users
- Real time Cloud interactive WorkSpace access via Wetty

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/guderian120/workspace-system-management.git
cd cloud_workspace
````

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Django Server

```bash
python manage.py runserver
```

---

## 📂 API Endpoint

### `POST /upload/`

Uploads a CSV file and processes user creation.

#### ✅ Expected CSV Format

Your file should have the following headers:

```csv
username,full_name,department,email
```

* `username` – Linux system username
* `full_name` – Full name of the user
* `department` – Linux group to assign
* `email` – Email address for notification

#### 📥 Example CURL Request

```bash
curl -X POST -F "csv_file=@/path/to/users.csv" http://34.252.60.35:8080/upload/
```

---

## 📧 Email Notifications

The system uses a custom `email_server` module to notify users of their credentials. You can also configure it to notify admins about job status or errors.

---

## 🔐 Sudo Access Handling

This project uses `subprocess` to execute system-level commands such as:

* `useradd`
* `groupadd`
* `chpasswd`
* `chage`

All commands are executed with sudo. Ensure you configure your environment with the correct sudo password and permissions.

---

## 🌐 Web-Based Terminal Access via Wetty

While this project supports live shell access via Wetty, the Docker setup and deployment are left to users.

You can follow the official Wetty Docker instructions here:
👉 [Wetty GitHub Repository](https://github.com/butlerx/wetty)

---

## 🤖 Behind the Scenes

* Uses `pandas` to parse and process CSV input
* Automatically generates secure passwords
* Bypasses CSRF for the upload endpoint using Django’s `@csrf_exempt`
* Modular structure: Email handling is delegated to a custom `email_server.py`

---

## 🧪 Example Output

Upon successful upload, you will receive a JSON response like:

```json
{
  "message": "CSV processed successfully!",
  "data": [...]
}
```

If errors occurred:

```json
{
  "error": "Errors occurred during processing",
  "details": [...]
}
```

---

## 📌 Final Notes

* Ensure your EC2 security groups allow access on required ports (`8080` for Django, or proxy it to `80`/`443`).
* CSV data must be **clean and properly structured**.
* This tool is designed for **development and controlled environments** — avoid using it in production without security hardening.

---


