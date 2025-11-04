#!/usr/bin/env python3
"""
EKS Resource Management Script for ResearchOps Agent

Manages lifecycle of EKS deployments including:
- Status monitoring and health checks
- Updates and rollbacks
- Resource cleanup and recreation
- Cost tracking and optimization
- Backup and restore
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None


class Colors:
    """ANSI color codes"""
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'


class EKSManager:
    """Manages EKS resources for ResearchOps Agent"""

    def __init__(self, cluster: str, region: str, namespace: str = "research-ops", verbose: bool = False):
        self.cluster = cluster
        self.region = region
        self.namespace = namespace
        self.verbose = verbose
        self.project_root = Path(__file__).parent
        self.k8s_dir = self.project_root / "k8s"

    def log(self, message: str, level: str = "info"):
        """Print colored log messages"""
        color_map = {
            "info": Colors.BLUE,
            "success": Colors.GREEN,
            "warning": Colors.YELLOW,
            "error": Colors.RED,
            "highlight": Colors.CYAN
        }
        color = color_map.get(level, Colors.NC)
        print(f"{color}{message}{Colors.NC}")

    def run_command(self, cmd: List[str], capture: bool = True, check: bool = True) -> Tuple[int, str, str]:
        """Execute command with error handling"""
        if self.verbose:
            self.log(f"Running: {' '.join(cmd)}", "info")

        try:
            if capture:
                result = subprocess.run(cmd, capture_output=True, text=True, check=check)
                return result.returncode, result.stdout, result.stderr
            else:
                result = subprocess.run(cmd, check=check)
                return result.returncode, "", ""
        except subprocess.CalledProcessError as e:
            if check:
                self.log(f"Command failed: {' '.join(cmd)}", "error")
                raise
            return e.returncode, "", str(e)

    def update_kubeconfig(self):
        """Update kubectl context for cluster"""
        self.log(f"Updating kubeconfig for cluster {self.cluster}...", "info")
        self.run_command([
            "aws", "eks", "update-kubeconfig",
            "--name", self.cluster,
            "--region", self.region
        ])

    def get_pod_status(self) -> List[Dict]:
        """Get status of all pods in namespace"""
        returncode, stdout, _ = self.run_command([
            "kubectl", "get", "pods",
            "-n", self.namespace,
            "-o", "json"
        ])

        if returncode != 0:
            return []

        try:
            data = json.loads(stdout)
            pods = []
            for item in data.get("items", []):
                pod = {
                    "name": item["metadata"]["name"],
                    "status": item["status"]["phase"],
                    "ready": "Unknown",
                    "restarts": 0,
                    "age": item["metadata"]["creationTimestamp"]
                }

                # Calculate ready status
                container_statuses = item["status"].get("containerStatuses", [])
                if container_statuses:
                    ready_count = sum(1 for c in container_statuses if c.get("ready", False))
                    total_count = len(container_statuses)
                    pod["ready"] = f"{ready_count}/{total_count}"
                    pod["restarts"] = sum(c.get("restartCount", 0) for c in container_statuses)

                pods.append(pod)

            return pods
        except json.JSONDecodeError:
            return []

    def get_service_endpoints(self) -> List[Dict]:
        """Get service endpoints and LoadBalancer IPs"""
        returncode, stdout, _ = self.run_command([
            "kubectl", "get", "svc",
            "-n", self.namespace,
            "-o", "json"
        ])

        if returncode != 0:
            return []

        try:
            data = json.loads(stdout)
            services = []
            for item in data.get("items", []):
                svc = {
                    "name": item["metadata"]["name"],
                    "type": item["spec"]["type"],
                    "cluster_ip": item["spec"].get("clusterIP", "None"),
                    "external_ip": "Pending",
                    "ports": []
                }

                # Get external IP
                if svc["type"] == "LoadBalancer":
                    ingress = item["status"].get("loadBalancer", {}).get("ingress", [])
                    if ingress:
                        svc["external_ip"] = ingress[0].get("hostname", ingress[0].get("ip", "Pending"))

                # Get ports
                for port in item["spec"].get("ports", []):
                    svc["ports"].append(f"{port.get('port')}:{port.get('targetPort')}/{port.get('protocol', 'TCP')}")

                services.append(svc)

            return services
        except json.JSONDecodeError:
            return []

    def get_resource_usage(self) -> Dict:
        """Get resource usage statistics"""
        # Node resources
        returncode, stdout, _ = self.run_command(["kubectl", "top", "nodes"], check=False)
        node_usage = stdout if returncode == 0 else "Metrics not available"

        # Pod resources
        returncode, stdout, _ = self.run_command([
            "kubectl", "top", "pods",
            "-n", self.namespace
        ], check=False)
        pod_usage = stdout if returncode == 0 else "Metrics not available"

        return {
            "nodes": node_usage,
            "pods": pod_usage
        }

    def status(self, detailed: bool = False):
        """Display cluster and deployment status"""
        self.log("="*70, "info")
        self.log(f"ResearchOps Agent - EKS Status", "highlight")
        self.log("="*70, "info")
        self.log(f"Cluster: {self.cluster}", "info")
        self.log(f"Region: {self.region}", "info")
        self.log(f"Namespace: {self.namespace}", "info")
        self.log("="*70, "info")

        # Update kubeconfig
        self.update_kubeconfig()

        # Pods
        self.log("\n📦 Pods:", "highlight")
        pods = self.get_pod_status()
        if pods:
            for pod in pods:
                status_color = "success" if pod["status"] == "Running" else "warning"
                self.log(
                    f"  {pod['name']:<40} {pod['status']:<12} Ready: {pod['ready']:<6} Restarts: {pod['restarts']}",
                    status_color
                )
        else:
            self.log("  No pods found", "warning")

        # Services
        self.log("\n🌐 Services:", "highlight")
        services = self.get_service_endpoints()
        if services:
            for svc in services:
                self.log(f"  {svc['name']:<30} Type: {svc['type']:<15} External: {svc['external_ip']}", "info")
                if detailed:
                    self.log(f"    Ports: {', '.join(svc['ports'])}", "info")
        else:
            self.log("  No services found", "warning")

        # Resource usage
        if detailed:
            self.log("\n📊 Resource Usage:", "highlight")
            usage = self.get_resource_usage()
            self.log("\nNode Resources:", "info")
            print(usage["nodes"])
            self.log("\nPod Resources:", "info")
            print(usage["pods"])

        self.log("\n" + "="*70, "info")

    def logs(self, deployment: str, follow: bool = False, tail: int = 100):
        """View logs from a deployment"""
        self.update_kubeconfig()

        self.log(f"📋 Fetching logs from {deployment}...", "info")

        cmd = [
            "kubectl", "logs",
            f"deployment/{deployment}",
            "-n", self.namespace,
            f"--tail={tail}"
        ]

        if follow:
            cmd.append("-f")

        # Don't capture if following
        self.run_command(cmd, capture=False)

    def restart(self, deployment: str):
        """Restart a deployment"""
        self.update_kubeconfig()

        self.log(f"🔄 Restarting deployment/{deployment}...", "info")

        self.run_command([
            "kubectl", "rollout", "restart",
            f"deployment/{deployment}",
            "-n", self.namespace
        ])

        self.log(f"✅ Restart initiated for {deployment}", "success")
        self.log("Watching rollout status...", "info")

        self.run_command([
            "kubectl", "rollout", "status",
            f"deployment/{deployment}",
            "-n", self.namespace
        ], capture=False)

    def scale(self, deployment: str, replicas: int):
        """Scale a deployment"""
        self.update_kubeconfig()

        self.log(f"📊 Scaling {deployment} to {replicas} replicas...", "info")

        self.run_command([
            "kubectl", "scale",
            f"deployment/{deployment}",
            f"--replicas={replicas}",
            "-n", self.namespace
        ])

        self.log(f"✅ Scaled {deployment} to {replicas} replicas", "success")

    def update(self, manifests: Optional[List[str]] = None):
        """Apply updates to deployments"""
        self.update_kubeconfig()

        if not manifests:
            # Default: update all manifests
            manifests = [
                "namespace.yaml",
                "secrets.yaml",
                "reasoning-nim-deployment.yaml",
                "embedding-nim-deployment.yaml",
                "vector-db-deployment.yaml",
                "agent-orchestrator-deployment.yaml",
                "web-ui-deployment.yaml"
            ]

        self.log("🔄 Applying updates...", "info")

        for manifest in manifests:
            manifest_path = self.k8s_dir / manifest
            if manifest_path.exists():
                self.log(f"  → Applying {manifest}...", "info")
                self.run_command(["kubectl", "apply", "-f", str(manifest_path)])
            else:
                self.log(f"  ⚠️  {manifest} not found", "warning")

        self.log("✅ Updates applied", "success")

    def rollback(self, deployment: str, revision: Optional[int] = None):
        """Rollback a deployment to previous version"""
        self.update_kubeconfig()

        self.log(f"↩️  Rolling back {deployment}...", "info")

        cmd = [
            "kubectl", "rollout", "undo",
            f"deployment/{deployment}",
            "-n", self.namespace
        ]

        if revision:
            cmd.extend([f"--to-revision={revision}"])

        self.run_command(cmd)

        self.log(f"✅ Rollback initiated for {deployment}", "success")
        self.log("Watching rollout status...", "info")

        self.run_command([
            "kubectl", "rollout", "status",
            f"deployment/{deployment}",
            "-n", self.namespace
        ], capture=False)

    def recreate(self, components: Optional[List[str]] = None):
        """Delete and recreate deployments"""
        self.update_kubeconfig()

        if not components:
            self.log("⚠️  No components specified for recreation", "warning")
            self.log("Available components: reasoning-nim, embedding-nim, vector-db, agent-orchestrator, web-ui", "info")
            return

        self.log(f"🗑️  Recreating components: {', '.join(components)}", "warning")
        confirm = input("This will cause downtime. Continue? (yes/no): ")

        if confirm.lower() != "yes":
            self.log("Cancelled", "info")
            return

        for component in components:
            deployment_name = component
            manifest_name = f"{component}-deployment.yaml"

            # Delete deployment
            self.log(f"  → Deleting {deployment_name}...", "info")
            self.run_command([
                "kubectl", "delete", "deployment", deployment_name,
                "-n", self.namespace,
                "--ignore-not-found"
            ])

            # Wait a moment for cleanup
            time.sleep(5)

            # Recreate from manifest
            manifest_path = self.k8s_dir / manifest_name
            if manifest_path.exists():
                self.log(f"  → Recreating {deployment_name}...", "info")
                self.run_command(["kubectl", "apply", "-f", str(manifest_path)])
            else:
                self.log(f"  ⚠️  Manifest {manifest_name} not found", "warning")

        self.log("✅ Recreation complete", "success")

    def cleanup(self, level: str = "namespace"):
        """Clean up resources"""
        self.update_kubeconfig()

        if level == "namespace":
            self.log(f"🗑️  Deleting namespace {self.namespace}...", "warning")
            self.log("This will delete all resources in the namespace", "warning")
            confirm = input("Continue? (yes/no): ")

            if confirm.lower() == "yes":
                self.run_command(["kubectl", "delete", "namespace", self.namespace])
                self.log("✅ Namespace deleted", "success")
            else:
                self.log("Cancelled", "info")

        elif level == "cluster":
            self.log(f"🗑️  Deleting cluster {self.cluster}...", "warning")
            self.log("This will delete the entire EKS cluster and all resources", "error")
            self.log(f"Estimated cost savings: ~$2/hour (~$1,500/month)", "info")
            confirm = input(f"Type the cluster name to confirm: ")

            if confirm == self.cluster:
                self.run_command([
                    "eksctl", "delete", "cluster",
                    "--name", self.cluster,
                    "--region", self.region
                ])
                self.log("✅ Cluster deletion initiated", "success")
            else:
                self.log("Cancelled - cluster name did not match", "info")

        elif level == "pods":
            self.log(f"🗑️  Deleting all pods in {self.namespace}...", "warning")
            confirm = input("Continue? (yes/no): ")

            if confirm.lower() == "yes":
                self.run_command([
                    "kubectl", "delete", "pods",
                    "--all",
                    "-n", self.namespace
                ])
                self.log("✅ Pods deleted (will be recreated by deployments)", "success")
            else:
                self.log("Cancelled", "info")

    def cost_estimate(self):
        """Estimate current EKS costs"""
        self.log("="*70, "info")
        self.log("💰 Cost Estimation", "highlight")
        self.log("="*70, "info")

        # Get node information
        returncode, stdout, _ = self.run_command([
            "kubectl", "get", "nodes",
            "-o", "json"
        ])

        if returncode != 0:
            self.log("Could not fetch node information", "error")
            return

        try:
            data = json.loads(stdout)
            nodes = data.get("items", [])

            self.log(f"\n📊 Cluster Resources:", "info")
            self.log(f"  Nodes: {len(nodes)}", "info")

            # Estimate costs
            g5_2xlarge_hourly = 1.006  # us-east-2 pricing
            eks_control_plane_hourly = 0.10

            total_hourly = (len(nodes) * g5_2xlarge_hourly) + eks_control_plane_hourly
            total_daily = total_hourly * 24
            total_monthly = total_hourly * 24 * 30

            self.log(f"\n💵 Estimated Costs (assuming g5.2xlarge nodes):", "highlight")
            self.log(f"  Hourly:  ${total_hourly:.2f}", "info")
            self.log(f"  Daily:   ${total_daily:.2f}", "info")
            self.log(f"  Monthly: ${total_monthly:.2f}", "info")

            self.log(f"\n💡 Cost Optimization Tips:", "info")
            self.log(f"  • Scale down to 1 node when not in use: Save ${g5_2xlarge_hourly:.2f}/hour", "info")
            self.log(f"  • Delete cluster when not needed: Save ${total_hourly:.2f}/hour", "info")
            self.log(f"  • Use Spot instances: Save up to 70%", "info")

        except json.JSONDecodeError:
            self.log("Could not parse node information", "error")

        self.log("="*70, "info")

    def backup(self, output_dir: str = "backup"):
        """Backup current deployment configuration"""
        self.update_kubeconfig()

        backup_dir = Path(output_dir) / f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        backup_dir.mkdir(parents=True, exist_ok=True)

        self.log(f"💾 Creating backup in {backup_dir}...", "info")

        # Backup all resources
        resources = ["deployments", "services", "configmaps", "secrets", "pods"]

        for resource in resources:
            self.log(f"  → Backing up {resource}...", "info")
            returncode, stdout, _ = self.run_command([
                "kubectl", "get", resource,
                "-n", self.namespace,
                "-o", "yaml"
            ], check=False)

            if returncode == 0:
                output_file = backup_dir / f"{resource}.yaml"
                with open(output_file, "w") as f:
                    f.write(stdout)

        self.log(f"✅ Backup complete: {backup_dir}", "success")

    def health_check(self) -> bool:
        """Comprehensive health check"""
        self.update_kubeconfig()

        self.log("🏥 Running health checks...", "info")

        all_healthy = True

        # Check pods
        pods = self.get_pod_status()
        unhealthy_pods = [p for p in pods if p["status"] != "Running"]

        if unhealthy_pods:
            self.log(f"❌ {len(unhealthy_pods)} pods not running:", "error")
            for pod in unhealthy_pods:
                self.log(f"  - {pod['name']}: {pod['status']}", "error")
            all_healthy = False
        else:
            self.log(f"✅ All {len(pods)} pods running", "success")

        # Check services
        services = self.get_service_endpoints()
        pending_services = [s for s in services if s["type"] == "LoadBalancer" and s["external_ip"] == "Pending"]

        if pending_services:
            self.log(f"⚠️  {len(pending_services)} services pending external IP:", "warning")
            for svc in pending_services:
                self.log(f"  - {svc['name']}", "warning")

        return all_healthy


def main():
    parser = argparse.ArgumentParser(
        description="Manage ResearchOps Agent EKS Deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  status     Show cluster and deployment status
  logs       View logs from a deployment
  restart    Restart a deployment
  scale      Scale a deployment
  update     Apply configuration updates
  rollback   Rollback to previous version
  recreate   Delete and recreate components
  cleanup    Clean up resources
  cost       Show cost estimation
  backup     Backup current configuration
  health     Run health checks

Examples:
  # Show detailed status
  ./manage-eks.py status --detailed

  # View logs from agent orchestrator
  ./manage-eks.py logs agent-orchestrator --follow

  # Restart a deployment
  ./manage-eks.py restart reasoning-nim

  # Scale web-ui to 3 replicas
  ./manage-eks.py scale web-ui --replicas 3

  # Recreate reasoning NIM
  ./manage-eks.py recreate --components reasoning-nim

  # Cleanup namespace
  ./manage-eks.py cleanup --level namespace

  # Backup configuration
  ./manage-eks.py backup --output-dir ./backups
        """
    )

    parser.add_argument("command", choices=[
        "status", "logs", "restart", "scale", "update",
        "rollback", "recreate", "cleanup", "cost", "backup", "health"
    ])

    parser.add_argument("deployment", nargs="?", help="Deployment name (for logs, restart, rollback)")
    parser.add_argument("--cluster", default="research-ops-cluster", help="EKS cluster name")
    parser.add_argument("--region", default="us-east-2", help="AWS region")
    parser.add_argument("--namespace", default="research-ops", help="Kubernetes namespace")
    parser.add_argument("--detailed", action="store_true", help="Show detailed information")
    parser.add_argument("--follow", "-f", action="store_true", help="Follow logs")
    parser.add_argument("--tail", type=int, default=100, help="Number of log lines")
    parser.add_argument("--replicas", type=int, help="Number of replicas for scaling")
    parser.add_argument("--components", nargs="+", help="Components to recreate")
    parser.add_argument("--level", choices=["namespace", "cluster", "pods"], default="namespace")
    parser.add_argument("--output-dir", default="backup", help="Backup output directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    manager = EKSManager(
        cluster=args.cluster,
        region=args.region,
        namespace=args.namespace,
        verbose=args.verbose
    )

    try:
        if args.command == "status":
            manager.status(detailed=args.detailed)

        elif args.command == "logs":
            if not args.deployment:
                print("Error: deployment name required for logs command")
                return 1
            manager.logs(args.deployment, follow=args.follow, tail=args.tail)

        elif args.command == "restart":
            if not args.deployment:
                print("Error: deployment name required for restart command")
                return 1
            manager.restart(args.deployment)

        elif args.command == "scale":
            if not args.deployment or args.replicas is None:
                print("Error: deployment name and --replicas required for scale command")
                return 1
            manager.scale(args.deployment, args.replicas)

        elif args.command == "update":
            manager.update()

        elif args.command == "rollback":
            if not args.deployment:
                print("Error: deployment name required for rollback command")
                return 1
            manager.rollback(args.deployment)

        elif args.command == "recreate":
            manager.recreate(components=args.components)

        elif args.command == "cleanup":
            manager.cleanup(level=args.level)

        elif args.command == "cost":
            manager.cost_estimate()

        elif args.command == "backup":
            manager.backup(output_dir=args.output_dir)

        elif args.command == "health":
            healthy = manager.health_check()
            return 0 if healthy else 1

        return 0

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 130
    except Exception as e:
        print(f"\nError: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
