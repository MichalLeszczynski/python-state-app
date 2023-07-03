
# Idea of a project

This project is meant to show various devops technologies at use together, so right now the scenario, that happens looks like that:
- Commit is pushed to the gitlab branch
- CI/CD is triggered
    - Black checks python code formatting
    - Pylint lints python code (fails if score < 3/10)
    - Docker builds app image and pushes it to gitlab container registry
- Kubernetes cluster is updated (in case of change in k8s manifests) automatically due to gitlab agent that pulls helm chart config from this repo

# Used technologies

### Python & flask
Simple web server with two endpoints seems to be a good use-case for flask framework as it's really lightweight comparing for example to django.

### Docker
Used to package an application to the portable image to be pushed and used by k8s later.

### k8s and helm
I've used helm as a nice tool for parameterizing and grouping k8s manifests.

### Gitlab
Gitlab serves as a remote git server, container registry and as a host for pipelines - I've managed to use 30-day free tier for this exercise.

## Container registry
In order to be able to pull my images from conatiner registry I had to add secret with token config - it enables readonly access to registry
## Gitlab agent
I've installed gitlab agent on my k8s cluster (hosted locally on my computer) and set up .gitlab dir with agent config updating my helm chart on any change automatically.

# Commands
## Docker commands to build and push docker image (happening anyway during ci/cd)

```
docker build . -t michalleszczyns/my-server:0.1.0

docker push michalleszczyns/my-server:0.1.0
```

## Install gitlab agent on your k8s cluster

```
helm repo add gitlab https://charts.gitlab.io
helm repo update
helm upgrade --install michal-k8s gitlab/gitlab-agent \
    --namespace gitlab-agent \
    --create-namespace \
    --set image.tag=v15.4.0 \
    --set config.token=NueGdkJz8RXFU2CJ9AgpWECbvGqHAzc8o3Phv8aV8YPseGzLfg \
    --set config.kasAddress=wss://kas.gitlab.com
```