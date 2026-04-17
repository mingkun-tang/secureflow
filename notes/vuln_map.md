# Vulnerability Map

## /api/update_email

**Vulnerability:**
CSRF (Cross-site Request Forgery)

**Attack:**
Attacker tricks a logged-in user into submitting a request that changes their email to attacker-controlled email.

**Impact:**
Account takeover via passowrd reset.

**Fix:**
Implement CSRF protection (CSRF token) to verify user intent before processing the request.


## /api/reset_password

**Vulnerability:**
Missing Authenticaiton / authorization

**Attack:**
Attackers can directly send a request with a victim;s eamil to reset their password, without needing to be logged in or verified.

**Impact:**
This will eventually lead to Full account takeover.

**Fix:**
Implement a secure password reset flow using token-based verfication.
Generate a random, time-limited, single-use reset token and require the user to prove ownership before allowing the password to be changed.


## /api/get_user

**Vulnerability:**
IDOR (Insecure direct Object Reference) / broken access control

**Attack:**
An attacker can modify the 'user_id' paramter to access other users' data, because the server deos not verify whether the logged-in user is authorized to veiw that account.

**Impact:**
Exposure of sensitive user data (data, role), which can lead to privacy breaches and targeting of privileged accounts.

**Fix:**
Enforce server-side authorization checks
Users should only be able to access their own data, or restrict access to admin users when querying other accounts.

## /admin/delete_user

**Vulnerability:**
CSRF (Cross-Site Request Forgery) and business logic flaw (self-delete / last admin removal)

**Attack:**
An attacker can trick a logged-in admin into submitting a malicious request that delets users. Additionally, the system deos not enforce rules preventing an admin from deleting themselves or removing the last remaining admin account.

**Impact:**
Unauthorized user deletion and potential loss of administrative control. If the last admin is removed. the system may become unmanageable.

**Fix:**
Implement CSRF protection (CSRF token) to verify admin intent. Enforce business rules to prevent self-deletion and ensure at least one admin acocunt always exists.
