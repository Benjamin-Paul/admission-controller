## Custom admission controller scope
This is a small admission controller for Kubernetes. The webhook server, written in Python, will proxy any request to the Kubernetes API that satisfies the following conditions : 
- It is a CREATE or UPDATE request
- The object of the request is a DEPLOYMENT
- The request is not made in system or monitoring related namespaces
This scope is defined in the Kubernetes cluster through a ValidatingWebhookConfiguration object (manifest not inclulded here) : [see the Kubernetes documentation for more information](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/)

## Custom admission controller logic 
This controller enforces the following policy:
- When a deployment is created, the "kubernetes.io/change-cause" entry must be specified
- When a deployment is updated, the "kubernetes.io/change-cause" entry must be different from the previous one
This helps ensure the deployment rollout history is organized and readable.
