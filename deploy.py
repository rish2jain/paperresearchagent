#!/usr/bin/env python3
"""
Unified deployment script for ResearchOps Agent
Supports local Docker, AWS EKS, and validation workflows
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None  # Will warn if trying to read secrets.yaml


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class DeploymentManager:
    """Manages deployment across different targets"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = Path(__file__).parent
        self.k8s_dir = self.project_root / "k8s"
        self._ngc_api_key = None  # Cache for NGC API key

    def log(self, message: str, level: str = "info"):
        """Print colored log messages"""
        color_map = {
            "info": Colors.BLUE,
            "success": Colors.GREEN,
            "warning": Colors.YELLOW,
            "error": Colors.RED
        }
        color = color_map.get(level, Colors.NC)
        print(f"{color}{message}{Colors.NC}")

    def run_command(
        self,
        cmd: List[str],
        check: bool = True,
        capture: bool = False,
        env: Optional[Dict[str, str]] = None
    ) -> Tuple[int, str, str]:
        """Execute shell command with error handling"""
        if self.verbose:
            self.log(f"Running: {' '.join(cmd)}", "info")

        try:
            if capture:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=check,
                    env={**os.environ, **(env or {})}
                )
                return result.returncode, result.stdout, result.stderr
            else:
                result = subprocess.run(
                    cmd,
                    check=check,
                    env={**os.environ, **(env or {})}
                )
                return result.returncode, "", ""
        except subprocess.CalledProcessError as e:
            if check:
                self.log(f"Command failed: {' '.join(cmd)}", "error")
                raise
            return e.returncode, "", str(e)

    def get_ngc_key_from_secrets(self) -> Optional[str]:
        """Extract NGC_API_KEY from k8s/secrets.yaml if it exists"""
        secrets_file = self.k8s_dir / "secrets.yaml"
        
        if not secrets_file.exists():
            return None
        
        if yaml is None:
            self.log("⚠️  PyYAML not installed, cannot read secrets.yaml", "warning")
            self.log("Install with: pip install pyyaml", "info")
            return None
            
        try:
            with open(secrets_file) as f:
                docs = yaml.safe_load_all(f)
                for doc in docs:
                    if doc and doc.get('metadata', {}).get('name') == 'nvidia-ngc-secret':
                        string_data = doc.get('stringData', {})
                        if 'NGC_API_KEY' in string_data:
                            return string_data['NGC_API_KEY']
        except Exception as e:
            self.log(f"Could not read NGC_API_KEY from secrets.yaml: {e}", "warning")
            
        return None
    
    def get_ngc_key(self) -> Optional[str]:
        """Get NGC_API_KEY from environment or secrets.yaml"""
        if self._ngc_api_key:
            return self._ngc_api_key
            
        # Try environment first
        ngc_key = os.getenv("NGC_API_KEY")
        if ngc_key:
            self._ngc_api_key = ngc_key
            return ngc_key
            
        # Try secrets.yaml
        ngc_key = self.get_ngc_key_from_secrets()
        if ngc_key:
            self.log("✅ Found NGC_API_KEY in k8s/secrets.yaml", "success")
            self._ngc_api_key = ngc_key
            return ngc_key
            
        return None

    def check_prerequisites(self, target: str) -> bool:
        """Validate required tools are installed"""
        self.log("🔍 Checking prerequisites...", "info")

        required_tools = {
            "docker": ["docker", "--version"],
            "docker-compose": ["docker-compose", "--version"]
        }

        if target == "eks":
            required_tools.update({
                "kubectl": ["kubectl", "version", "--client"],
                "aws": ["aws", "--version"]
            })

        missing_tools = []
        for tool_name, check_cmd in required_tools.items():
            returncode, _, _ = self.run_command(check_cmd, check=False, capture=True)
            if returncode != 0:
                missing_tools.append(tool_name)

        if missing_tools:
            self.log(f"❌ Missing required tools: {', '.join(missing_tools)}", "error")
            self.log("Please install missing tools and try again", "error")
            return False

        self.log("✅ All prerequisites satisfied", "success")
        return True

    def validate_environment(self, target: str) -> bool:
        """Validate environment variables"""
        self.log("🔍 Validating environment variables...", "info")

        required_vars = []
        optional_vars = []

        if target == "eks":
            # Check NGC_API_KEY (from env or secrets.yaml)
            ngc_key = self.get_ngc_key()
            if not ngc_key:
                self.log(f"❌ NGC_API_KEY not found", "error")
                self.log("Set it as environment variable OR add to k8s/secrets.yaml", "error")
                self.log("Get NGC API key from: https://ngc.nvidia.com/setup", "warning")
                return False
            
            self.log(f"✅ NGC_API_KEY found ({len(ngc_key)} characters)", "success")
            
            optional_vars.extend([
                "SEMANTIC_SCHOLAR_API_KEY",
                "IEEE_API_KEY",
                "ACM_API_KEY",
                "SPRINGER_API_KEY"
            ])

        missing_optional = [var for var in optional_vars if not os.getenv(var)]
        if missing_optional:
            self.log(f"⚠️  Optional environment variables not set:", "warning")
            for var in missing_optional:
                self.log(f"  - {var}", "warning")

        self.log("✅ Environment validation passed", "success")
        return True

    def build_docker_images(self, push: bool = False, registry: Optional[str] = None):
        """Build Docker images for the application"""
        self.log("🐳 Building Docker images...", "info")

        images = [
            ("orchestrator", "Dockerfile.orchestrator", "agent-orchestrator"),
            ("ui", "Dockerfile.ui", "web-ui")
        ]

        for name, dockerfile, tag in images:
            self.log(f"Building {name} image...", "info")

            image_tag = f"{registry}/{tag}:latest" if registry else f"research-ops-{tag}:latest"

            cmd = [
                "docker", "build",
                "-f", str(self.project_root / dockerfile),
                "-t", image_tag,
                str(self.project_root)
            ]

            self.run_command(cmd)
            self.log(f"✅ Built {image_tag}", "success")

            if push and registry:
                self.log(f"Pushing {image_tag}...", "info")
                self.run_command(["docker", "push", image_tag])
                self.log(f"✅ Pushed {image_tag}", "success")

    def deploy_local_docker(self):
        """Deploy using Docker Compose"""
        self.log("🚀 Deploying with Docker Compose...", "info")

        compose_file = self.project_root / "docker-compose.yml"
        if not compose_file.exists():
            self.log("❌ docker-compose.yml not found", "error")
            return False

        # Stop existing containers
        self.log("Stopping existing containers...", "info")
        self.run_command(["docker-compose", "down"], check=False)

        # Start services
        self.log("Starting services...", "info")
        self.run_command(["docker-compose", "up", "-d"])

        # Wait for services to be healthy
        self.log("Waiting for services to be healthy...", "info")
        time.sleep(10)

        # Check service status
        returncode, stdout, _ = self.run_command(
            ["docker-compose", "ps"],
            capture=True
        )

        self.log("✅ Docker Compose deployment complete", "success")
        self.log("\nServices:", "info")
        print(stdout)

        self.log("\n🌐 Access points:", "info")
        self.log("  Web UI: http://localhost:8501", "success")
        self.log("  API: http://localhost:8080", "success")
        self.log("\nView logs: docker-compose logs -f", "info")

        return True

    def deploy_eks(self, cluster_name: str = "research-ops-cluster", region: str = "us-east-2"):
        """Deploy to AWS EKS"""
        self.log(f"🚀 Deploying to AWS EKS (cluster: {cluster_name}, region: {region})...", "info")

        # Check if cluster exists
        self.log("Checking EKS cluster...", "info")
        returncode, _, _ = self.run_command(
            ["aws", "eks", "describe-cluster", "--name", cluster_name, "--region", region],
            check=False,
            capture=True
        )

        if returncode != 0:
            self.log(f"⚠️  Cluster {cluster_name} not found", "warning")
            self.log(f"A new EKS cluster will be created (takes 15-20 minutes)", "info")
            create = input(f"Create EKS cluster '{cluster_name}' in {region}? (yes/no): ")

            if create.lower() != "yes":
                self.log("Deployment cancelled by user", "warning")
                return False

            self.create_eks_cluster(cluster_name, region)
        else:
            self.log(f"✅ Cluster {cluster_name} already exists", "success")

        # Update kubeconfig
        self.log("Updating kubeconfig...", "info")
        self.run_command([
            "aws", "eks", "update-kubeconfig",
            "--name", cluster_name,
            "--region", region
        ])

        # Create NGC registry secret
        self.log("Creating NGC registry secret...", "info")
        ngc_key = self.get_ngc_key()  # Use new method instead of os.getenv
        self.run_command([
            "kubectl", "create", "secret", "docker-registry", "ngc-secret",
            "--docker-server=nvcr.io",
            "--docker-username=$oauthtoken",
            f"--docker-password={ngc_key}",
            "--namespace=default",
            "--dry-run=client",
            "-o", "yaml"
        ], capture=True)

        # Apply it
        self.run_command(["kubectl", "apply", "-f", "-"], check=False)

        # Apply Kubernetes manifests
        self.log("Applying Kubernetes manifests...", "info")

        manifests = [
            "namespace.yaml",
            "secrets.yaml",
            "reasoning-nim-deployment.yaml",
            "embedding-nim-deployment.yaml",
            "vector-db-deployment.yaml",
            "agent-orchestrator-deployment.yaml",
            "web-ui-deployment.yaml"
        ]

        for manifest in manifests:
            manifest_path = self.k8s_dir / manifest
            if manifest_path.exists():
                self.log(f"  → Applying {manifest}...", "info")

                # Handle secrets specially to substitute NGC_API_KEY
                if manifest == "secrets.yaml":
                    with open(manifest_path) as f:
                        content = f.read()
                    content = content.replace("YOUR_NGC_API_KEY_HERE", ngc_key)

                    # Apply via stdin
                    process = subprocess.Popen(
                        ["kubectl", "apply", "-f", "-"],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    process.communicate(input=content)
                else:
                    self.run_command(["kubectl", "apply", "-f", str(manifest_path)])

        # Wait for deployments
        self.log("⏳ Waiting for deployments (this may take 10-20 minutes)...", "warning")

        deployments = [
            ("reasoning-nim", 1200),  # 20 minutes for TensorRT compilation
            ("embedding-nim", 1200),
            ("qdrant", 300),
            ("agent-orchestrator", 300),
            ("web-ui", 300)
        ]

        for deployment, timeout in deployments:
            self.log(f"  → Waiting for {deployment}...", "info")
            try:
                self.run_command([
                    "kubectl", "wait",
                    "--for=condition=available",
                    f"--timeout={timeout}s",
                    f"deployment/{deployment}",
                    "-n", "research-ops"
                ])
                self.log(f"  ✅ {deployment} ready", "success")
            except subprocess.CalledProcessError:
                self.log(f"  ⚠️  {deployment} not ready (check with kubectl logs)", "warning")

        # Get service endpoints
        self.log("\n✅ Deployment complete!", "success")
        self.log("\n" + "="*50, "info")
        self.log("Service Endpoints:", "info")
        self.log("="*50, "info")

        # Get LoadBalancer IPs
        returncode, stdout, _ = self.run_command([
            "kubectl", "get", "svc",
            "-n", "research-ops",
            "-o", "wide"
        ], capture=True)

        print(stdout)

        self.log("\n" + "="*50, "info")
        self.log("Useful commands:", "info")
        self.log("="*50, "info")
        self.log("View logs:", "info")
        self.log("  kubectl logs -f deployment/reasoning-nim -n research-ops", "info")
        self.log("  kubectl logs -f deployment/agent-orchestrator -n research-ops", "info")
        self.log("\nCheck status:", "info")
        self.log("  kubectl get pods -n research-ops", "info")
        self.log("  kubectl get svc -n research-ops", "info")

        return True

    def create_eks_cluster(self, cluster_name: str, region: str):
        """Create EKS cluster with GPU nodes"""
        self.log(f"Creating EKS cluster {cluster_name}...", "warning")

        cmd = [
            "eksctl", "create", "cluster",
            "--name", cluster_name,
            "--region", region,
            "--node-type", "g5.2xlarge",
            "--nodes", "2",
            "--nodes-min", "1",
            "--nodes-max", "3",
            "--managed",
            "--version", "1.28"
        ]

        self.run_command(cmd)
        self.log(f"✅ Cluster {cluster_name} created", "success")

    def cleanup(self, target: str):
        """Clean up deployment resources"""
        self.log("🧹 Cleaning up resources...", "info")

        if target == "docker":
            self.run_command(["docker-compose", "down", "-v"], check=False)
            self.log("✅ Docker Compose cleanup complete", "success")

        elif target == "eks":
            response = input("Delete entire namespace? This removes all deployed resources. (yes/no): ")
            if response.lower() == "yes":
                self.run_command([
                    "kubectl", "delete", "namespace", "research-ops"
                ], check=False)
                self.log("✅ EKS cleanup complete", "success")


def main():
    parser = argparse.ArgumentParser(
        description="ResearchOps Agent Deployment Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Deploy locally with Docker Compose
  ./deploy.py --target docker

  # Deploy to AWS EKS
  ./deploy.py --target eks --cluster my-cluster --region us-west-2

  # Build and push images to registry
  ./deploy.py --build --push --registry my-registry.io/research-ops

  # Clean up resources
  ./deploy.py --cleanup --target docker
        """
    )

    parser.add_argument(
        "--target",
        choices=["docker", "eks"],
        default="docker",
        help="Deployment target (default: docker)"
    )

    parser.add_argument(
        "--build",
        action="store_true",
        help="Build Docker images"
    )

    parser.add_argument(
        "--push",
        action="store_true",
        help="Push images to registry (requires --registry)"
    )

    parser.add_argument(
        "--registry",
        help="Docker registry for images (e.g., myregistry.io/project)"
    )

    parser.add_argument(
        "--cluster",
        default="research-ops-cluster",
        help="EKS cluster name (default: research-ops-cluster)"
    )

    parser.add_argument(
        "--region",
        default="us-east-2",
        help="AWS region (default: us-east-2)"
    )

    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up deployment resources"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    manager = DeploymentManager(verbose=args.verbose)

    # Cleanup mode
    if args.cleanup:
        manager.cleanup(args.target)
        return 0

    # Check prerequisites
    if not manager.check_prerequisites(args.target):
        return 1

    # Validate environment
    if not manager.validate_environment(args.target):
        return 1

    # Build images if requested
    if args.build:
        manager.build_docker_images(push=args.push, registry=args.registry)

    # Deploy to target
    if args.target == "docker":
        success = manager.deploy_local_docker()
    elif args.target == "eks":
        success = manager.deploy_eks(cluster_name=args.cluster, region=args.region)
    else:
        manager.log(f"Unknown target: {args.target}", "error")
        return 1

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())