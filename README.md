# 🏦 BankPro – Banking Management System

## 📌 About the Project

**BankPro** is a web-based Banking Management System developed using Python, Django, and MySQL. It provides a simple and efficient platform for managing essential banking operations through a modern and user-friendly interface.

The application helps administrators manage customers, bank accounts, deposits, withdrawals, and transaction records. It also includes an interactive dashboard with charts and a reporting system for better monitoring of banking activities.

## ✨ Features

- 📊 **Interactive Dashboard** – View banking statistics and graphical reports.
- 👥 **Customer Management** – Add, view, update, and delete customer details.
- 💳 **Account Management** – Create and manage bank accounts.
- 💰 **Deposit Management** – Process deposits and update account balances.
- 💸 **Withdrawal Management** – Process withdrawals with balance validation.
- 🔄 **Transaction History** – Maintain and manage transaction records.
- 📈 **Reports & Analytics** – Filter transactions by date and transaction type.
- 📥 **CSV Export** – Export transaction reports as CSV files.
- 🔐 **Authentication** – Login system with protected pages.
- ⚙️ **Admin Panel** – Manage banking data through the administration interface.
- 🎨 **Modern UI** – Clean, responsive, and user-friendly design.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Backend programming |
| 🌐 Django | Web framework |
| 🗄️ MySQL | Database management |
| 🎨 HTML5 | Page structure |
| 🎨 CSS3 | Styling and layout |
| ⚡ JavaScript | Interactive functionality |
| 📊 Chart.js | Dashboard charts |
| 🔣 Font Awesome | Icons |
| 💻 VS Code | Development environment |
| 🔗 Git & GitHub | Version control |

## 📂 Project Structure

```text
Banking_management_system/
│
├── accounts/
├── banking_project/
├── customers/
├── transactions/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── accounts/
│   ├── admin/
│   ├── customers/
│   └── transactions/
│
├── .gitignore
├── manage.py
└── README.md
```

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/josephrionmachado/BankPro-Banking-Management-System.git
```

### 2️⃣ Navigate to the Project Folder

```bash
cd BankPro-Banking-Management-System
```

### 3️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4️⃣ Install Required Packages

```bash
pip install Django==5.2.19 mysqlclient==2.3.1 python-dotenv==1.2.4
```

### 5️⃣ Configure Environment Variables

Create a `.env` file in the project root and configure your own local settings:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

DB_NAME=banking_management
DB_USER=your-mysql-username
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

⚠️ Never upload your `.env` file or share your actual credentials.

### 6️⃣ Create the MySQL Database

Open MySQL and execute:

```sql
CREATE DATABASE banking_management;
```

### 7️⃣ Apply Database Migrations

```bash
python manage.py migrate
```

### 8️⃣ Create an Admin Account

```bash
python manage.py createsuperuser
```

Follow the instructions to create your administrator account.

### 9️⃣ Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

**http://127.0.0.1:8000/**

## 🎯 Project Objective

The main objective of BankPro is to demonstrate the development of a banking management application using modern web technologies. It aims to simplify banking operations, maintain organized financial records, and provide an efficient interface for managing banking activities.

## 🚀 Future Enhancements

- 🔄 Fund transfer functionality
- 📱 Customer self-service portal
- 📄 PDF report generation
- 📧 Email notifications
- 🔒 Enhanced security features

## 👨‍💻 Developer

**Joseph Rion Machado**

GitHub: [@josephrionmachado](https://github.com/josephrionmachado)

## ⭐ Support

If you find this project interesting, consider giving the repository a **star ⭐** on GitHub!

---

<p align="center">
  Made with ❤️ using Python & Django
</p>

<p align="center">
  © 2026 BankPro – Banking Management System
</p>
