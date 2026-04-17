# SecureFlow - Backend API Security Project

## Overview
Secureflow is a backend-focused web application I built to simulate real-world security vulnerabilities and understand how they can be exploited and fixed.

The goal of this project is to go beyond just learning concepts and actually see how vulnerabilities like CSRF, IDOR, and broken access control happen in real systems.

---

## Vulnerabilities I Explored

### 1. CSRF - /api/update_email
The system allows a logged-in user's email to be changed without verifying user intent. An attacker can trick the user into making this request.

### 2. IDOR / Broken Access Control - /api/get_user
The API trusts user input 'user_id' without checking if the user is allowed to access that data. This allows users to view other users' information.

### 3. Missing Authentication - /api/reset_password
The password reset endpoint does not verify who is making the request. Anyone can reset any user's password using just an email.

### 4. CSRF + Business Logic Flaw - /admin/delete_user
Admin actions can be triggered without verifying intent. The system also allows self-deletion and removing the last admin, which can break the system.

---

## Example Attack Chain

One of the main things I focused on was chaining vulnerabilities together: 

1. Use CSRF to change victim's email
2. Trigger password reset
3. Take over the account

This helped me understand how small issues can combine into a serious attack.

---

## Fixes / What I learned

- Always verify user intent (CSRF protection)
- Never trust user-controlled input for authorization
- Authentication is not enough, authorization must be enforced as well
- Sensitive actions should require stronger verification
- Security should be designed into the system, not added later

---

## Tech Stack

- Python (Flask)
- HTML (Jinja2 templates)








