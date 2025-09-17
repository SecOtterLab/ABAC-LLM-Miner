# Policy Description: Workforce

*Vesion: v20250308*

This policy governs a SaaS workforce management application provided by eWorkforce, which facilitates workflow planning and supply management for service appointments like installations and repairs.

Tenants (eWorkforce customers) create tasks for their customers, which are assigned to technicians working for eWorkforce, its workforce suppliers, or their subcontractors. Work orders are scheduled as needed, and warehouse operators handle supply requests.

The policy defines access rules for eWorkforce employees and specific tenants, such as PowerProtection (a power protection service provider) and TelCo (a telecommunications provider). Permissions to view, assign, and complete tasks depend on factors such as the user’s role, task assignments, managerial supervision, and contract associations within eWorkforce.

This policy is available as a case study in *Decat et al. (2014)*, which provides further details.

**Reference**: Maarten Decat, Jasper Bogaerts, Bert Lagaisse, and Wouter Joosen. *The workforce management case study: functional analysis and access control requirements.* CW Reports CW655,
Department of Computer Science, KU Leuven, February 2014.

## Attributes

### Subject/User Attributes
The subjects of this policy are employees of the system, including managers, helpdesk operators, warehouse operators, and technicians. The following attributes are used to describe the subjects.

| Attribute Name      | Multiplicity, Type     | Description                                               | Example Values                                     |
|--------------------|------------------|-----------------------------------------------------------|--------------------------------------------------|
| uid          | Single, String   | User’s unique identifier                                  | wfmgr001, tech001, etc.                         |
| position          | Single, String   | User's job role or title within the organization.        | workforceManager, technician, etc.             |
| department        | Single, String   | Department to which the user belongs.                     | workforce, warehouse, etc.                      |
| provider         | Single, String   | Organization who is providing the employee               | eWorkforce, telco, powerProtection, subContractor, etc |
| assignedTenant    | Single, String   | Tenant or subtenant assigned to the user for responsibilities. | telco, powerProtection                          |
| assignedRegion    | Single, String   | Region assigned to the user for work.                     | north, south                                    |
| managedStaff      | Multi, Set\<String>  | Staff assigned to a manager. (i.e. technicians assigned to a workforce manager) | {tech001, tech002}, etc. |
| certifications    | Multi, Set\<String>  | Certifications the user holds.                            | {telcoCertifiedTechnician, powerProtectionSpecialist}, etc. |
| isCustomerSupport | Single, Boolean     | Indicates whether a user is customer support or not.     | True, False                                     |
| group            | Single, String   | Indicates which group a user belongs to.                  | residentialSupport, companySupport, provisioning, techSupport |

### Resource Attributes
The resources of this system include work orders, contracts, tasks, resource requests, and stock refill requests. The following attributes are used to describe the resources.

| Attribute Name      | Multiplicity, Type     | Description                                               | Example Values                                     |
|--------------------|------------------|-----------------------------------------------------------|--------------------------------------------------|
| rid      | Single, String   | Resource’s unique identifier                             | contract001, workorder001, task001, etc.               |
| type             | Single, String   | Type of resource being accessed.                        | contract, workOrder, task, etc.                        |
| department       | Single, String   | Department associated with the resource                 | workforce, warehouse                             |
| tenant          | Single, String   | Tenant which a resource belongs to                      | telco, powerProtection                           |
| tenantType      | Single, String   | Type of tenant associated with the resource.            | primary, subtenant                               |
| resourceRegion   | Single, String   | Region in which the task or work order is executed.    | north, south                                     |
| contractStatus   | Single, String   | Status of the related contract or project.              | active, inactive                                |
| associatedContract | Single, String | Contract which a work order belongs to                 | contract001, contract002, etc.                                    |
| associatedWorkOrder | Single, String | Work order which a task belongs to                     | workorder001, workorder002, etc.                                     |
| createdBy       | Single, String   | Employee who created a work order.                     | wfmgr001, tech001, etc.                                         |
| assignedTechnician | Single, String | Technician assigned to complete a specific task or work order. | tech001, tech002, etc. |
| assignedEmployee | Single, String   | Employee assigned to a resource (primarily used for warehouse operators and requests) | whop001, whop002, etc. |
| requiredCertifications | Multi, Set\<String> | Certifications required to execute a specific work order or task. | {telcoCertifiedTechnician, powerProtectionSpecialist}, etc. |
| recurrence       | Single, Boolean     | Indicates whether a work order is one-time or recurring. | True, False                                     |
| isAppointment   | Single, Boolean     | Indicates whether a work order is an appointment. Only appears when recurrence is false. | True, False |
| isComplete   | Single, Boolean     | Indicates whether a resource request or stock refill request has been marked as complete. | True, False |
