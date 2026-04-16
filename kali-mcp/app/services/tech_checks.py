def tech_specific_checks(technologies):
    checks = []

    for tech in technologies:
        tech_lower = tech.lower()

        if "wordpress" in tech_lower:
            checks.append("Run WordPress plugin and theme enumeration")

        if "graphql" in tech_lower:
            checks.append("Test GraphQL introspection and GraphiQL exposure")

        if "aws" in tech_lower:
            checks.append("Check for exposed S3 buckets and public assets")

        if "tomcat" in tech_lower:
            checks.append("Check for manager panel and default credentials")

        if "jenkins" in tech_lower:
            checks.append("Check Jenkins dashboard exposure")

        if "grafana" in tech_lower:
            checks.append("Check Grafana anonymous access")

        if "kibana" in tech_lower:
            checks.append("Check Kibana dashboard exposure")

    return list(set(checks))