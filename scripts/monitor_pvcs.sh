#!/bin/bash
# Script to monitor PVC status and related pods

set -euo pipefail
IFS=$' \n\t'

# Error handler: print script context on failure
trap 'echo "Error in $0 at line $LINENO: command failed with exit code $?" >&2; echo "Last command: $BASH_COMMAND" >&2; exit 1' ERR

NAMESPACE="research-ops"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 PVC Status Monitor - $(date '+%Y-%m-%d %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📦 Persistent Volume Claims:"
echo "───────────────────────────────────────────────────────────────────────────────"
kubectl get pvc -n "$NAMESPACE" -o wide
echo ""

echo "🔍 Detailed PVC Information:"
echo "───────────────────────────────────────────────────────────────────────────────"
# Batch fetch all PVC metadata in a single kubectl call
kubectl get pvc -n "$NAMESPACE" -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\t"}{.spec.storageClassName}{"\t"}{.spec.volumeName}{"\t"}{.status.capacity.storage}{"\t"}{.metadata.annotations.volume\.kubernetes\.io/selected-node}{"\n"}{end}' | while IFS=$'\t' read -r pvc status storage_class volume capacity node; do
    echo ""
    echo "PVC: $pvc"
    echo "───────────────────────────────────────────────────────────────────────────────"
    echo "  Status:        ${status:-<unknown>}"
    echo "  Storage Class: ${storage_class:-<not set>}"
    echo "  Volume:        ${volume:-<not created>}"
    echo "  Capacity:      ${capacity:-<pending>}"
    echo "  Selected Node: ${node:-<not selected>}"
    
    # Get recent events
    echo "  Recent Events:"
    kubectl get events -n "$NAMESPACE" --field-selector involvedObject.name="$pvc" --sort-by='.lastTimestamp' | tail -3 | awk '{print "    "$0}' || echo "    (no recent events)"
done

echo ""
echo "🐳 Related Pods:"
echo "───────────────────────────────────────────────────────────────────────────────"
kubectl get pods -n "$NAMESPACE" -o wide | grep -E "NAME|nim|qdrant"
echo ""

echo "📋 Pod Scheduling Issues (if any):"
echo "───────────────────────────────────────────────────────────────────────────────"
for pod in $(kubectl get pods -n "$NAMESPACE" -o jsonpath='{.items[?(@.status.phase=="Pending")].metadata.name}'); do
    if [ -n "$pod" ]; then
        echo ""
        echo "Pod: $pod"
        kubectl describe pod "$pod" -n "$NAMESPACE" | grep -A 10 "Events:" | tail -5
    fi
done

echo ""
echo "💾 Storage Classes:"
echo "───────────────────────────────────────────────────────────────────────────────"
kubectl get storageclass

echo ""
echo "🔧 EBS CSI Driver Status:"
echo "───────────────────────────────────────────────────────────────────────────────"
kubectl get pods -n kube-system -l app=ebs-csi-controller 2>/dev/null || echo "  EBS CSI controller not found in kube-system"
kubectl get pods -n kube-system -l app=ebs-csi-node 2>/dev/null || echo "  EBS CSI node driver not found in kube-system"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

