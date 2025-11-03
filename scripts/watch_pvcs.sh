#!/bin/bash
# Continuous watch script for PVCs

NAMESPACE="research-ops"

echo "🔍 Watching PVCs in namespace: $NAMESPACE"
echo "Press Ctrl+C to stop"
echo ""

watch -n 5 -d '
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 PVC Status - $(date +%H:%M:%S)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
kubectl get pvc -n '"$NAMESPACE"'
echo ""
echo "Related Pods:"
kubectl get pods -n '"$NAMESPACE"' -o wide | grep -E "NAME|nim|qdrant"
'

