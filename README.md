# Workshop demo
 Запускаем minikube, проверяем что все работает
 
```bash
minikube start
kubectl get pods -A
```

Подготавливаем docker-образ для приложения

```bash
git clone git@github.com:ssfilatov/k8s-conf-demo.git
cd k8s-conf-demo/app
export YOURNAME=<your-name>
docker build .
docker tag <hash> $YOURNAME/myapp:v0.0.1
docker push $YOURNAME/myapp:v0.0.1
```

Готовый образ можно достать по адресу:
sfilatov/myapp:v0.0.1

```bash
kubectl create -f manifests/deployment.yaml
kubectl create -f manifests/service.yaml
```

```bash
kubectl delete -f manifests/deployment.yaml
kubectl delete -f manifests/service.yaml
```

### Helm

```bash
helm init
helm ls
helm create newapp
helm install --name myapp ./app-chart
helm upgrade myapp ./app-chart
```

### Prometheus Operator

```
kubectl apply -f https://raw.githubusercontent.com/helm/charts/master/stable/prometheus-operator/crds/crd-alertmanager.yaml
kubectl apply -f https://raw.githubusercontent.com/helm/charts/master/stable/prometheus-operator/crds/crd-podmonitor.yaml
kubectl apply -f https://raw.githubusercontent.com/helm/charts/master/stable/prometheus-operator/crds/crd-prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/helm/charts/master/stable/prometheus-operator/crds/crd-prometheusrules.yaml
kubectl apply -f https://raw.githubusercontent.com/helm/charts/master/stable/prometheus-operator/crds/crd-servicemonitor.yaml

helm install stable/prometheus-operator --version=4.3.6 --name=monitoring --namespace=monitoring --    values=manifests/prom-values.yaml
```

### Grafana

```bash
kubectl proxy
```
http://127.0.0.1:8001/api/v1/namespaces/monitoring/services/monitoring-grafana:80/proxy

Логин/пароль: admin/prom-operator

Добавляем в deployment:
```yaml
- name: GF_SERVER_ROOT_URL
  value: "/api/v1/namespaces/monitoring/services/monitoring-grafana:80/proxy"
```

### Prometheus

Таргеты:
http://127.0.0.1:8001/api/v1/namespaces/monitoring/services/monitoring-prometheus-oper-prometheus:9090/proxy

 Собираем версию приложения с мониторингом, выкатываем:
 ```bash
 helm upgrade myapp ./app-chart
 ```

Деплоим servicemonitor:
```bash
kubectl create -f manifests/servicemonitor.yaml
```

Добавляем
```yaml
labels:
    release: monitoring
```

PromQl: rate(flask_http_request_total[30s])

Удаляем за собой:
```
helm del --purge monitoring
```

### Jaeger

```bash
helm install stable/jaeger-operator --name myjaeger
kubectl create -f manifests/simple-jaeger.yaml
```

Удаляем ресурсы:

```bash
helm del --purge myjaeger
```

### Логи

Ставим Elasticsearch
```bash
helm repo add elastic https://helm.elastic.co
helm install --name elasticsearch elastic/elasticsearch --values=manifests/es-values.yaml
kubectl get pods --namespace=default -l app=elasticsearch-master -w
```

Ставим fluentbit:
```
kubectl create namespace logging
kubectl create -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-service-account.yaml
kubectl create -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-role.yaml
kubectl create -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-role-binding.yaml
kubectl create -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/output/elasticsearch/fluent-bit-configmap.yaml
kubectl create -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/output/elasticsearch/fluent-bit-ds-minikube.yaml
```
выставляем es host в "elasticsearch-master.default.svc.cluster.local" 
Ставим kibana:

```bash
helm install --name kibana elastic/kibana
```



