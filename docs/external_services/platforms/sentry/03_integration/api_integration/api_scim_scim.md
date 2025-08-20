---
title: "SCIM"
source_url: "https://docs.sentry.io/api/scim/"
scraped_date: "2025-08-19T18:29:31.613862"
description: ""
platform: "sentry"
category: "error_monitoring"
stack: "fed_job_advisor"
note: "Documentation focused on Fed Job Advisor production deployment"
---
**Note: This documentation is focused on production deployment for Fed Job Advisor**

HomeAPI ReferenceSCIM Copy pageSCIMSystem for Cross-Domain Identity Management (SCIM) is a standard implemented by Identity Providers and applications in order to facilitate federated identity management. Through these APIs you can add and delete members as well as teams. Sentry SaaS customers must be on a Business Plan with SAML2 Enabled. SCIM uses a bearer token for authentication that is created when SCIM is enabled. For how to enable SCIM, see our docs here. Sentry's SCIM API does not currently support syncing passwords, or setting any User attributes other than active.Delete an Individual TeamDelete an Organization Member via SCIMList an Organization's Paginated TeamsList an Organization's SCIM MembersProvision a New Organization MemberProvision a New TeamQuery an Individual Organization MemberQuery an Individual TeamUpdate a Team's AttributesUpdate an Organization Member's AttributesWas this helpful?Yes 👍No 👎How can we improve this page?Submit feedback