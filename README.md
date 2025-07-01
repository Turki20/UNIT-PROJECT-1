# 📦 Inventory Management System

An interactive, integrated inventory management system built with **Python** using an advanced Terminal interface. It integrates AI-driven features and smart reporting to simplify sales and purchase operations, monitor stock levels, and support smart decision-making.

---

## System Objectives

- Simplify product management within inventory.
- Reduce human errors during sales and purchase operations.
- Generate analytical reports to support decision-making.
- Utilize AI to forecast consumption and restocking needs.
- Enhance user experience through intelligent and automated features.

---

## User Roles & Permissions

| Role             | Permissions                                                                 |
|:----------------|:----------------------------------------------------------------------------|
| **System Admin**   | Full access to all system features including user management.               |

---

## Key Features

### Product Management
- Add, edit, delete, and list products.


### Sales & Purchase Operations
- Record sales and automatically deduct stock quantities with barcode support.
- Record purchases, increase quantities, and calculate tax.
- Auto-generate invoices as CSV files for both sales and purchases.

### Reporting
- Real-time inventory status report.

---


## ER Diagram:
![ER Diagram](https://github.com/user-attachments/assets/043f6ef3-c4d0-4898-8605-2845b85044b1)

---
## 📦 How to Run the Inventory Management System

To start the program on Windows, open your terminal (Command Prompt or PowerShell), navigate to the project directory, and run the following command:

```bash
python -m terminal_interface.main
```

### Default User:
- username: admin
- password: 12345
---

## Future Work
- Search products by name, barcode, or category.
- Categorize products under specific classifications.
- Manual report creation and export as PDF.
- Auto-generated monthly reports emailed to management.
- Custom reports upon request.
- Edit warehouse capacity, space, and dedicated shelves for products.
- **Smart Stock Depletion Alerts** based on consumption rates.
- **Purchase Order Suggestions** predicting required quantities before running out.

| Role             | Permissions                                                                 |
|:----------------|:----------------------------------------------------------------------------|
| **System Admin**   | Full access to all system features including user management.               |
| **Inventory Staff**| Manage products, and record sales and purchase operations.                  |
| **Read-Only User** | View data and reports only, without editing permissions.                    |
