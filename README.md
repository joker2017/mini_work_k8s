# MiniBank Test Project

This project is a test REST API application called MiniBank, built using Django. It consists of two microservices that interact with a single PostgreSQL database. Nginx Unit serves as the application server. 

CI/CD is implemented using GitHub Actions for automated testing, building, storing Docker images on Docker Hub, and deployment to Kubernetes in Yandex Cloud. Both microservices are thoroughly tested with mocks to avoid dependencies on the database. This project addresses several Django-related issues, such as testing without a database, foreign key challenges with one database and two applications, deployment scripts for Yandex Cloud Kubernetes, and more.


**Account Service:**  
[![Account Badge](https://codecov.io/gh/joker2017/mini_work_k8s/graph/badge.svg?token=88NZMRH8CR&flag=account)](https://codecov.io/gh/joker2017/mini_work_k8s)

**Profile Service:**  
[![Profile Badge](https://codecov.io/gh/joker2017/mini_work_k8s/graph/badge.svg?token=88NZMRH8CR&flag=profile)](https://codecov.io/gh/joker2017/mini_work_k8s)

## Blue-Green Deployment
The application employs a blue-green deployment strategy, facilitated by GitHub Actions, Helm, and Argo Rollouts. This approach ensures zero downtime during updates and allows for quick rollback if issues are detected post-deployment.

## Feature Flags
Feature flags are implemented to manage and roll out new features without needing to restart the application. This functionality is controlled through the admin panel, providing a flexible and dynamic way to test new features in a live environment.

For more details on how to set up and manage feature flags or to contribute to the project, please refer to the [documentation](https://github.com/joker2017/mini_work_k8s/wiki).
