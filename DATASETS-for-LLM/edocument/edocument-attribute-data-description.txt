# Policy Description: Edocument

*Vesion: v20250324*

This policy governs a SaaS electronic document processing application provided by eDocs, which facilitates the secure distribution of digital and printed documents for various organizations.

Tenants (eDocs customers) use the application to send documents such as invoices, contracts, and notifications to their employees or customers. Documents can be delivered digitally via email, through postal services, or integrated with other platforms.

The policy defines access rules for eDocs employees and specific tenants, such as Large Bank and NewsAgency. Permissions to view, send, or manage documents depend on factors such as the user’s role, department, managerial supervision, and assigned projects within eDocs. 

This policy is available as a case study in *Decat et al. (2014)*, which provides further details.

**Reference**: Maarten Decat, Jasper Bogaerts, Bert Lagaisse, and Wouter Joosen. *The e-document case study: functional analysis and access control requirements.* CW Reports CW655,
Department of Computer Science, KU Leuven, February 2014.

## Attributes

### Subject Attributes
The subjects of this policy are users within the system, including employees, helpdesk operators, application admins, and customers. The following attributes are used to describe the subjects.

| Attribute Name       | Multiplicity, Type      | Description                                      | Example Values                                |
|---------------------|----------------------|--------------------------------------------------|---------------------------------------------|
| uid                | Single, String       | User’s unique identifier                         | user0, user1, user2, etc.                   |
| role               | Single, String       | Role which the user fulfills                    | employee, customer, admin, helpdesk         |
| position           | Single, String       | User's job role or title within the organization | secretary, director, officeManager, etc.    |
| tenant             | Single, String       | Organization to which the user belongs           | largeBank, largeBankLeasing, etc.           |
| department         | Single, String       | Department to which the user belongs             | largeBankSales, largeBankAudit, etc.        |
| office            | Single, String       | Office where the user is located                | largeBankOffice1, largeBankOffice2, etc.    |
| registered         | Single, Boolean      | Indicates if the user is registered in the system | True, False                                 |
| projects          | Multi, Set\<String>   | Projects the user is assigned to                 | Resources IDs                               |
| supervisor        | Single, String       | Supervisor that oversees the user                | User ID                                     |
| supervisee        | Multi, Set\<String>   | Supervisees that the user oversees               | User IDs                                    |
| payrollingPermissions | Single, Boolean  | Users that have permissions to do payrolling     | True, False                                 |

### Resource Attributes
Resources in the system include documents and other entities that users may access. The following attributes are used to describe the resources.

| Attribute Name         | Multiplicity, Type    | Description                                    | Example Values                                |
|-----------------------|--------------------|------------------------------------------------|---------------------------------------------|
| rid                  | Single, String     | Resource’s unique identifier                   | doc0, doc1, doc2, etc.                      |
| type                 | Single, String     | Type of resource being accessed                | invoice, contract, paycheck, bankingNote, etc. |
| owner                | Single, String     | User who owns the resource                     | User ID                                     |
| tenant               | Single, String     | Organization to which the resource belongs     | largeBank, largeBankLeasing, etc.           |
| department           | Single, String     | Department to which the resource belongs       | largeBankSales, largeBankAudit, etc.        |
| office              | Single, String     | Office where the resource is sent or assigned | largeBankOffice1, largeBankOffice2, etc.    |
| recipients          | Multi, Set\<String> | Users authorized to access the document       | User IDs                                    |
| isConfidential      | Single, Boolean    | Indicates if the document is confidential      | True, False                                 |
| containsPersonalInfo | Single, Boolean    | Indicates if the document contains personal data | True, False                             |

