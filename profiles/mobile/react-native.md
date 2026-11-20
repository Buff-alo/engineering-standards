# React Native Engineering Profile

**ID:** `mobile/react-native`  
**Persona:** Senior Mobile Platform Engineer  
**Scope:** React Native, Expo, TypeScript, Expo Router, TanStack Query, Zustand, secure storage, offline sync, EAS  
**When to use:** Building or modifying React Native or Expo mobile applications.  
**Companion profiles:** `None`

## Profile Contract

This profile supplements `core/ENGINEERING.md`, `core/PERSONAS.md`, `core/WORKFLOW.md`, and `core/QUALITY-GATES.md`.

If rules conflict, follow the precedence and override boundaries in `core/WORKFLOW.md` (Section 1.4):
1. Applicable platform, safety, security constraints, and non-negotiable `core/` invariants.
2. Explicit task requirements.
3. Repository-specific instructions and project contracts for stack, tooling, and workflow specialization.
4. Remaining universal standards in `core/`.
5. This profile and any required companion profiles.
6. Existing project conventions unless explicitly changed.

---

## 1. Stack

Preferred:

- React Native
- Expo
- TypeScript
- Expo Router
- TanStack Query

---

## 2. Navigation

Preferred:

```text
Expo Router
```

Use React Navigation directly when project requirements justify it.

---

## 3. State

Server state:

```text
TanStack Query
```

Local state:

```text
Zustand
```

Do not duplicate server state unnecessarily.

---

## 4. Secure Storage

Sensitive information:

```text
expo-secure-store
```

Non-sensitive cache:

```text
AsyncStorage
```

STRICTLY FORBIDDEN:

- passwords in AsyncStorage
- authentication secrets in AsyncStorage
- hardcoded credentials

---

## 5. API Architecture

Preferred:

```text
Screen
 ↓
Component
 ↓
Hook
 ↓
Service
 ↓
API Client
 ↓
Backend
```

---

## 6. Networking

Mobile networks are unreliable.

Handle:

- timeouts
- retries
- offline state
- reconnects
- foreground/background transitions

Do not implement infinite retries.

---

## 7. Offline Support

Where required:

- persist TanStack Query cache
- support optimistic updates
- queue appropriate mutations
- reconcile server state after reconnect

Never assume the device is continuously connected.

---

## 8. Notifications

Preferred:

- Expo Notifications
- Firebase Cloud Messaging when required

Notification handling must be resilient to:

- revoked permissions
- offline devices
- duplicate notifications
- expired tokens

---

## 9. Security

Never put secrets in the application bundle.

Remember:

> Mobile applications are client-side software and can be inspected.

Authorization must always be enforced by the backend.

---

## 10. Testing

Preferred:

- Jest
- React Native Testing Library
- Detox or equivalent E2E tooling where required

Test:

- authentication
- offline behavior
- navigation
- critical workflows
- API failure states

---

## 11. Build & Deployment

Preferred:

- EAS Build
- EAS Update where appropriate

Maintain separate:

- development
- preview
- production

configurations.
