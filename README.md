# Replication Package
This repository contains the artifacts and all experimental data for the paper: "Holistic Workload Quantification for Rapid Microservice Autoscaling under Synchronous API Invocations."

# Artifacts
| Type           | Name                | URL                                                         | License                    |
|----------------|---------------------|-------------------------------------------------------------|----------------------------|
| Benchmark        | Sock Shop           | https://github.com/microservices-demo/microservices-demo                      |            Apache License Version 2.0                |
|                | Online Boutique             | https://github.com/GoogleCloudPlatform/microservices-demo                         |          Apache License Version 2.0                  |
| Baselines      | SHOWAR           | https://github.com/WHU-AISE/ScalerEval      | MIT License                |
|                | Microscaler            | https://github.com/WHU-AISE/PBScaler |   MIT License    |
|                | PBScaler       | https://github.com/WHU-AISE/PBScaler                |            MIT License                |
|                | Derm             | https://github.com/liaochan/Derm            |                            |
|                | KHPA           | https://github.com/kubernetes/kubernetes/tree/master/pkg/controller/podautoscaler                     |             Apache License Version 2.0               |


<!-- ## Project Structure
```text
.
├── Figure 3-12/            # Raw data and plotting scripts for Figures 3 through 12 in the paper.
└── artifact/             # Core replication package including benchmarks and source code.
    ├── onlineboutique/    # Deployment manifests (YAML) and workload injection scripts for Online Boutique.
    ├── sockshop/          # Deployment manifests (YAML) and workload injection scripts for SockShop.
    ├── prometheus/        # Configuration and deployment files for the Prometheus monitoring stack.
    ├── Squanler/          # Source code of the Squanler autoscaling components.
    └── test_bedapplication/ # Dockerfiles and source code for the custom test-bed applications.
``` -->

# Experimental Environment Setup:
Docker: Version 27.5.1 or later is recommended.
Kubernetes (k8s): Version v1.20.4 is recommended.
Istio: Version v1.10 is recommended.
Monitoring: Your cluster must be equipped with Prometheus for metric collection:
```code
cd artifact
kubectl apply -f prometheus/prometheus.yaml
```

# Quick Start: Running Squanler in Your Cluster
### 1. Deploy Online Boutique and Inject Workload
First, create the hipster namespace, enable Istio sidecar injection, and deploy the Online Boutique benchmark:
```bash
cd artifact
kubectl create namespace hipster
kubectl label namespace hipster istio-injection=enabled
kubectl apply -f onlineboutique/onlineboutique.yaml
```

Deploy the Istio manifests to allow external traffic to enter the cluster via istio-ingressgateway and be forwarded to the frontend service:
```bash
kubectl apply -f onlineboutique/istio-manifest.yaml
```

Deploy Telemetry and WasmPlugin. This enables Prometheus to query the latency and RPS of Online Boutique at the API/interface granularity:
```bash
kubectl create -f onlineboutique/telemetry.yaml
kubectl create -f onlineboutique/wasmPlugin.yaml
```

Obtain your cluster's GATEWAY_IP and GATEWAY_PORT as the targets for workload injection. GATEWAY_IP: Run 
```bash
kubectl get nodes -o wide
```
to find the External-IP or Internal-IP of your nodes.

GATEWAY_PORT: Run 
```bash
kubectl get svc istio-ingressgateway -n istio-system
```
and identify the NodePort (e.g., 31380) mapped to port 80.

Inject workload into the five Online Boutique APIs using Locust in headless mode:
```bash
locust -f onlineboutique/locust/1.py --host="http:{GATEWAY_IP}//:<GATEWAY_PORT>" --headless
locust -f onlineboutique/locust/2.py --host="http:{GATEWAY_IP}//:<GATEWAY_PORT>" --headless
locust -f onlineboutique/locust/3.py --host="http:{GATEWAY_IP}//:<GATEWAY_PORT>" --headless
locust -f onlineboutique/locust/4.py --host="http:{GATEWAY_IP}//:<GATEWAY_PORT>" --headless
locust -f onlineboutique/locust/5.py --host="http:{GATEWAY_IP}//:<GATEWAY_PORT>" --headless
```


### 2 Configure and Run Squanler
Install the dependencies listed in requirements.txt using a Conda environment:
```bash
cd Squanler
conda create -n autoscale_env python=3.9 -y
conda activate autoscale_env
pip install -r requirement.txt
```

Replace the placeholder with the admin.conf file specific to your cluster (typically found at /etc/kubernetes/admin.conf on the master node).

Configure the necessary runtime parameters by following the detailed instructions provided in Config.py.

Execute Squanler:
```bash
python main.py
```
If the configuration is successful, you should observe a significant reduction in tail latency across all APIs via the Prometheus UI.
