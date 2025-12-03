#!/bin/bash
set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║            🚀 RAG Production App Starting...              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check for OpenAI API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ ERROR: OPENAI_API_KEY is not set!"
    echo ""
    echo "Create a .env file with:"
    echo "  OPENAI_API_KEY=sk-your-key-here"
    echo ""
    echo "Then run:"
    echo "  docker run --env-file .env -p 8501:8501 -p 8288:8288 -v /var/run/docker.sock:/var/run/docker.sock -v rag_data:/qdrant/storage familorujov/rag-app"
    echo ""
    exit 1
fi
echo "✅ OpenAI API Key found"

# Start Qdrant container if not running
echo "🗄️  Setting up Qdrant..."
if docker ps --format '{{.Names}}' | grep -q '^rag-qdrant$'; then
    echo "✅ Qdrant already running"
else
    # Remove old container if exists
    docker rm -f rag-qdrant 2>/dev/null || true
    
    # Start Qdrant
    docker run -d --name rag-qdrant \
        -p 6333:6333 \
        -v rag_data:/qdrant/storage \
        qdrant/qdrant > /dev/null 2>&1
    
    echo "✅ Qdrant container started"
fi

# Wait for Qdrant to be ready
echo "⏳ Waiting for Qdrant..."
until curl -s "http://host.docker.internal:6333/readyz" > /dev/null 2>&1 || curl -s "http://172.17.0.1:6333/readyz" > /dev/null 2>&1; do
    sleep 1
done
echo "✅ Qdrant ready"

# Set Qdrant URL (try host.docker.internal first, fallback to docker bridge)
if curl -s "http://host.docker.internal:6333/readyz" > /dev/null 2>&1; then
    export QDRANT_URL="http://host.docker.internal:6333"
else
    export QDRANT_URL="http://172.17.0.1:6333"
fi

# Start FastAPI in background
echo "🔧 Starting FastAPI..."
uv run uvicorn main:app --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &

sleep 2

# Start Inngest Dev Server in background
echo "📊 Starting Inngest..."
npx inngest-cli@latest dev \
    -u http://localhost:8000/api/inngest \
    --no-discovery \
    --port 8288 > /dev/null 2>&1 &

sleep 2

echo "🎨 Starting Streamlit..."
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    🎉 Ready!                              ║"
echo "╠═══════════════════════════════════════════════════════════╣"
echo "║  📊 App:               http://localhost:8501              ║"
echo "║  📈 Inngest Dashboard: http://localhost:8288              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

exec uv run streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
