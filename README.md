# SecureFlow - Backend API Security Project

## Overview

SecureFlow is a backend-focused web application I built to simulate real-world security vulnerabilities.

Instead of just learning what CSRF or IDOR is, I wanted to actually see how these vulnerabilities show up in a system and how they can be exploited.

## Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Attack Demo
![Attack](screenshots/attack.png)

### Admin KPI
![KPI](screenshots/kpi.png)

---

## How to Run

1. Clone the repo
2. Install Flask
3. Run `python app.py`
4. Open `http://127.0.0.1:5000`

---
## Features
- Session-based login
- Role-based access control (user, admin, boss)
- Secure vs vulnerable mode
- Admin KPI dashboard
- Boss financial page
- Attack demo page

## Demo Flow
In vulnerable mode:
1. Login as a normal user
2. Change your role through `/change_role`
3. Escalate to boss
4. Access `/boss/financials`

In secure mode:
- role checks block unauthorized access

---
## Vulnerabilities I Explored

### 1. CSRF - /api/update_email  
The system allows a logged-in user's email to be changed without checking if the request was actually made by the user.  
So if a user clicks on a malicious link, their email can be changed without them knowing.

---

### 2. IDOR / Broken Access Control - /api/get_user  
The API trusts the user input (user_id) and does not check if the user should have access to that data.  
This allows users to view other users’ information.

---

### 3. Missing Authentication - /api/reset_password  
The password reset endpoint does not verify who is making the request.  
Anyone can reset any user's password just by knowing their email.

---

### 4. CSRF + Business Logic Flaw - /admin/delete_user  
Admin actions can be triggered without verifying user intent.  
The system also allows deleting important users like the last admin, which can break the system.

---

## Example Attack Chain

One thing I focused on was how small vulnerabilities can connect together.

For example:
- Use CSRF to change the victim’s email  
- Trigger password reset  
- Take over the account  

This helped me understand that vulnerabilities are not always dangerous by themselves, but can become serious when combined.

---

## What I Learned

- Authentication is not enough, authorization must also be checked  
- The system should not trust user input for access control  
- Sensitive actions need extra protection (like CSRF tokens)  
- Security problems often come from how the system is designed  

---

## Tech Stack

- Python (Flask)
- HTML (Jinja templates)
