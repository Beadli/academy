---
sidebar_position: 5
title: "Module 5 — Windows Server & Active Directory"
---

# Module 5 — Windows Server & Active Directory

:::warning Not yet published
This module is under construction.
:::

Install Windows Server, promote your first domain controller, and understand
what actually happened: DNS, the directory, Kerberos, OUs, users and groups,
and your first Group Policy.

```powershell
# The commented-script style used throughout the course:
# every non-obvious line says what it does and why.

# Get every computer object in the Servers OU, newest first.
Get-ADComputer -Filter * -SearchBase "OU=Servers,DC=lab,DC=cyber,DC=internal" |
  Sort-Object whenCreated -Descending
```
