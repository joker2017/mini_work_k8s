# MiniBank Test Project

This project is a test REST API application called MiniBank, built using Django. It consists of two microservices that interact with a single PostgreSQL database. Nginx Unit serves as the application server. 

CI/CD is implemented using GitHub Actions for automated testing, building, storing Docker images on Docker Hub, and deployment to Kubernetes in Yandex Cloud. Both microservices are thoroughly tested with mocks to avoid dependencies on the database. This project addresses several Django-related issues, such as testing without a database, foreign key challenges with one database and two applications, deployment scripts for Yandex Cloud Kubernetes, and more.

**Account Service:**  
[![Account Badge](https://codecov.io/gh/joker2017/mini_work_k8s/graph/badge.svg?token=88NZMRH8CR&flag=account)](https://codecov.io/gh/joker2017/mini_work_k8s)

**Profile Service:**  
[![Profile Badge](https://codecov.io/gh/joker2017/mini_work_k8s/graph/badge.svg?token=88NZMRH8CR&flag=profile)](https://codecov.io/gh/joker2017/mini_work_k8s)

## API Description

### User Profile API

#### Admin Panel URL
- **URL:** `/profile/admin/`
- **Description:** Administrative panel for user profile management.

#### Search for user profiles
- **URL:** `/profile/usersearch/`
- **Method:** GET
- **Description:** Search for user profiles.
- **Enabled/Disabled:** Depends on the `SEARCHS_FLAG` flag.

#### Create a new user profile
- **URL:** `/profile/create/`
- **Method:** POST
- **Description:** Create a new user profile.
- **Enabled/Disabled:** Depends on the `USERS_CREATE_FLAG` flag.

#### Update an existing user profile
- **URL:** `/profile/update/<str:pk>/`
- **Method:** PUT
- **Description:** Update an existing user profile.
- **Enabled/Disabled:** Depends on the `USERS_UPDATE_FLAG` flag.

#### Delete an existing user profile
- **URL:** `/profile/destroy/<str:pk>/`
- **Method:** DELETE
- **Description:** Delete an existing user profile.
- **Enabled/Disabled:** Depends on the `USERS_DESTROY_FLAG` flag.

#### View details of a specific user profile
- **URL:** `/profile/detail/<str:id>/`
- **Method:** GET
- **Description:** View details of a specific user profile.
- **Enabled/Disabled:** Depends on the `USERSDETAIL_FLAG` flag.

### Account API

#### Admin Panel URL
- **URL:** `/account/admin/`
- **Description:** Administrative panel for account management.

#### List all accounts
- **URL:** `/account/list/`
- **Method:** GET
- **Description:** List all accounts.
- **Enabled/Disabled:** Depends on the `ACCOUNT_LIST_FLAG` flag.

#### Create a new account
- **URL:** `/account/create/`
- **Method:** POST
- **Description:** Create a new account.
- **Enabled/Disabled:** Depends on the `ACCOUNT_CREATE_FLAG` flag.

#### Update an existing account
- **URL:** `/account/update/<str:pk>/`
- **Method:** PUT
- **Description:** Update an existing account.
- **Enabled/Disabled:** Depends on the `ACCOUNT_UPDATE_FLAG` flag.

#### Destroy an existing account
- **URL:** `/account/destroy/<str:pk>/`
- **Method:** DELETE
- **Description:** Destroy an existing account.
- **Enabled/Disabled:** Depends on the `ACCOUNT_DESTROY_FLAG` flag.

#### Retrieve the details of a specific account
- **URL:** `/account/detail/<str:usernameid>/`
- **Method:** GET
- **Description:** Retrieve the details of a specific account.
- **Enabled/Disabled:** Depends on the `ACCOUNT_DETAIL_FLAG` flag.

For more details on how to set up and manage feature flags or to contribute to the project, please refer to the [documentation](https://github.com/joker2017/mini_work_k8s/wiki).