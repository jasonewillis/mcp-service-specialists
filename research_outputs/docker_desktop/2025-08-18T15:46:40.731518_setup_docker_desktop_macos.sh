#!/bin/bash
# Docker Desktop Setup Script for Fed Job Advisor (macOS)
# Generated: 2025-08-18T15:46:40.731518

set -e

echo "🐳 Setting up Docker Desktop for Fed Job Advisor development..."

# Check if Docker Desktop is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker Desktop is not installed"
    echo "📥 Download from: https://desktop.docker.com/mac/main/amd64/Docker.dmg"
    echo "🍎 For Apple Silicon: https://desktop.docker.com/mac/main/arm64/Docker.dmg"
    exit 1
fi

# Check if Docker Desktop is running
if ! docker info &> /dev/null; then
    echo "🚀 Starting Docker Desktop..."
    open /Applications/Docker.app
    echo "⏳ Waiting for Docker Desktop to start..."
    sleep 30
    
    # Wait for Docker to be ready
    timeout=60
    while ! docker info &> /dev/null && [ $timeout -gt 0 ]; do
        echo "⏳ Waiting for Docker daemon..."
        sleep 5
        timeout=$((timeout-5))
    done
    
    if ! docker info &> /dev/null; then
        echo "❌ Docker Desktop failed to start"
        exit 1
    fi
fi

echo "✅ Docker Desktop is running"

# Check resource allocation
echo "🔍 Checking Docker resource allocation..."
docker system df

# Enable BuildKit
echo "🚀 Enabling BuildKit..."
echo 'export DOCKER_BUILDKIT=1' >> ~/.bashrc
echo 'export COMPOSE_DOCKER_CLI_BUILD=1' >> ~/.bashrc

# Create Fed Job Advisor network
echo "🌐 Creating Fed Job Advisor network..."
docker network create fja-network 2>/dev/null || echo "Network already exists"

# Pull base images
echo "📥 Pulling base images..."
docker pull node:18-alpine
docker pull python:3.11-slim
docker pull postgres:15-alpine
docker pull redis:7-alpine

# Create volumes
echo "💾 Creating persistent volumes..."
docker volume create fja-postgres-data 2>/dev/null || echo "Volume already exists"
docker volume create fja-redis-data 2>/dev/null || echo "Volume already exists"

# Test setup
echo "🧪 Testing Docker setup..."
docker run --rm hello-world

echo "✅ Docker Desktop setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Navigate to your Fed Job Advisor project directory"
echo "2. Run: docker-compose up"
echo "3. Open http://localhost:3000 for frontend"
echo "4. Open http://localhost:8000/docs for API docs"
echo ""
echo "🔧 Recommended Docker Desktop settings:"
echo "  Memory: 8GB"
echo "  CPU: 4 cores"
echo "  Disk: 100GB"
echo "  File Sharing: Enable for project directory"
