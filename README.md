
<html>
<head>
    <title>MiniBank Project Description</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/highlight.min.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>
</head>
<body>

    <h2>MiniBank Project</h2>

    <!-- Badges -->
    <div>
        <span>Account: <img src="your-badge-url-here" alt="Account Badge"></span>
        <span>Profile: <img src="your-badge-url-here" alt="Profile Badge"></span>
    </div>

    <!-- Project Description -->
    <section>
        <p>The "MiniBank" project is a REST API application developed using the Django framework. It embodies two microservices that interact with a single PostgreSQL database. To ensure high-performance operation of applications, Nginx Unit is used as the server.</p>

        <p>During development, a continuous integration and delivery (CI/CD) infrastructure was implemented using GitHub Actions. This includes automatic code testing, building and hosting images in Docker Hub, and deploying applications in Kubernetes on Yandex Cloud. Special attention is paid to testing: both microservices are covered with mock tests, avoiding database dependencies during testing.</p>

        <p>The project utilizes a blue-green deployment strategy in Kubernetes, ensuring seamless transitions between versions with minimal downtime. Moreover, it features an advanced feature flags system that allows for dynamic management of application features directly from the Django admin interface without the need for application restarts. This flexibility ensures that new features can be tested and rolled out with greater control and minimal impact on the current users' experience.</p>

        <p>The "MiniBank" project focuses on solving a number of specific issues related to Django development. In particular, attention is paid to handling foreign keys in a single database for two applications, which is a non-trivial task in Django. Moreover, the project has implemented scripts for easy deployment in Yandex Cloud using Kubernetes, allowing for effective application scaling.</p>

        <p>Although the project is a test, it addresses many current issues of web application development and deployment, offering practical solutions for working with Django, databases, containerization, and orchestration. "MiniBank" can serve as an excellent example for studying and applying modern approaches in application development and deployment.</p>
    </section>

</body>

