# OAuth Abuse Detection & Incident Response Lab Case Study

## Overview

This case study documents an **OAuth access token abuse scenario**, demonstrating how valid authentication can be misused post-login.  
The lab simulates a real-world scenario where an access token is exposed and reused, emphasizing the importance of **post-authentication monitoring**.

---

## Executive Summary

A valid OAuth access token issued through a legitimate login flow was exposed and subsequently abused to access protected user data via API calls.  

**Key takeaway:** Security failures often occur **after authentication succeeds**, highlighting the need for **behavioral monitoring and contextual token validation**.

---

## Incident Overview

- **Type:** OAuth Token Abuse / Session Replay  
- **Severity:** Medium  
- **Status:** Contained (Lab Simulation)  
- **Detection Method:** Manual behavioral analysis  
- **Affected Asset:** OAuth-protected API endpoints  
- **Data Impact:** User profile information accessible via API  

---

## Attack Narrative

1. User authenticates successfully via OAuth login.
2. Access token is issued with permissions to access user data.
3. Token is exposed through application logging/debug output.
4. Attacker extracts and reuses the token (simulated).
5. Token is used to call protected API endpoints.
6. API returns user data without triggering authentication alerts.

> No credentials were compromised and no MFA was bypassed.

---

## Indicators of Compromise (IOCs)

- Same OAuth token used from multiple IP addresses  
- API access without a recent login event  
- Unusually high request velocity  
- Access outside intended OAuth scope  
- Geographic or device context mismatch  

---

## Detection Gaps

- No monitoring for **post-authentication token behavior**  
- Tokens not bound to device or IP context  
- Lack of alerting for token reuse patterns  
- Overreliance on token validity alone  

---

## Impact Assessment

- Unauthorized access to protected user data  
- Potential silent data exposure in production environments  
- Attack appears legitimate in standard logs without context  

---

## Containment & Response Actions

1. Revoke the compromised access token  
2. Rotate related refresh tokens  
3. Invalidate active sessions  
4. Audit API access logs for data exposure  
5. Remove the source of token exposure  

---

## Root Cause Analysis

**Primary Cause:** Exposure of access tokens through logging.  

**Contributing Factors:**  
- Long-lived access tokens  
- Lack of device/IP binding  
- Insufficient post-authentication monitoring  

---

## Remediation & Recommendations

- Short-lived access tokens  
- Strict OAuth scope enforcement  
- Eliminate plaintext token logging  
- Monitor for abnormal token usage patterns:
  - Multiple IPs
  - High request frequency
  - Context mismatches  
- Improve visibility into token lifecycle events  

---

## Incident Timeline

T0 User logs in → Token issued
T1 Token used normally
T2 Token exposed via logs
T3 Token reused from new IP
T4 Protected data accessed
T5 Detection triggers

---

## MITRE ATT&CK Mapping

- **Technique:** Valid Accounts – Token Abuse  
- **Tactic:** Credential Access / Defense Evasion  



