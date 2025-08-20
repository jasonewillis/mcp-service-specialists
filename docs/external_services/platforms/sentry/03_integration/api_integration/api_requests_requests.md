---
title: "Requests"
source_url: "https://docs.sentry.io/api/requests/"
scraped_date: "2025-08-19T18:29:31.614222"
description: ""
platform: "sentry"
category: "error_monitoring"
stack: "fed_job_advisor"
note: "Documentation focused on Fed Job Advisor production deployment"
---
**Note: This documentation is focused on production deployment for Fed Job Advisor**

HomeAPI ReferenceRequests Copy pageRequestsAll API requests should be made to the /api/0/ prefix, and will return JSON as the response:BashHttpCopiedcurl -i https://sentry.io/api/0/ HTTP VerbsSentry makes an attempt to stick to appropriate HTTP verbs, but we always prioritize usability over correctness.MethodDescriptionDELETEUsed for deleting resources.GETUsed for retrieving resources.OPTIONSDescribes the given endpoint.POSTUsed for creating resources.PUTUsed for updating resources. Partial data is accepted where possible.Parameters and DataAny parameters not included in the URL should be encoded as JSON with a Content-Type of 'application/json':BashCopiedcurl -i https://sentry.io/api/0/organizations/acme/projects/1/groups/ \ -d '{"status": "resolved"}' \ -H 'Content-Type: application/json' Additional parameters are sometimes specified via the querystring, even for POST, PUT, and DELETE requests:BashCopiedcurl -i https://sentry.io/api/0/organizations/acme/projects/1/groups/?status=unresolved \ -d '{"status": "resolved"}' \ -H 'Content-Type: application/json' PreviousRate LimitsNextAlerts & NotificationsWas this helpful?Yes 👍No 👎How can we improve this page?Submit feedback