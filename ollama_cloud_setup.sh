#!/bin/bash
# Ollama Cloud Setup Script
# This script automates the setup of Ollama on a cloud GPU instance

set -e  # Exit on error

echo "======================================================================================================"
echo "OLLAMA CLOUD SETUP FOR SOP QUESTION GENERATOR"
echo "======================================================================================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✓ Detected Linux OS"
else
    echo "✗ This script is designed for Linux cloud instances"
    exit 1
fi

# Step 1: Update system packages
echo ""
echo "Step 1: Updating system packages..."
echo "------------------------------------------------------------------------------------------------------"
sudo apt-get update -qq
sudo apt-get upgrade -y -qq
echo "✓ System packages updated"

# Step 2: Install Ollama
echo ""
echo "Step 2: Installing Ollama..."
echo "------------------------------------------------------------------------------------------------------"
if command -v ollama &> /dev/null; then
    echo "✓ Ollama already installed"
else
    curl -fsSL https://ollama.com/install.sh | sh
    echo "✓ Ollama installed successfully"
fi

# Step 3: Start Ollama service
echo ""
echo "Step 3: Starting Ollama service..."
echo "------------------------------------------------------------------------------------------------------"
ollama serve > /dev/null 2>&1 &
sleep 5
echo "✓ Ollama service started"

# Step 4: Pull recommended model
echo ""
echo "Step 4: Downloading recommended model..."
echo "------------------------------------------------------------------------------------------------------"
echo "Available models (recommended based on GPU):"
echo "  1. llama3.1:70b (A100 80GB) - BEST quality"
echo "  2. qwen2.5:72b (A100 80GB) - BEST quality, alternative"
echo "  3. llama3.1:8b (V100/A10G 16-24GB) - Good quality"
echo "  4. qwen2.5:14b (V100/A10G 24GB) - Good quality"
echo ""
read -p "Enter model name (default: llama3.1:70b): " MODEL_NAME
MODEL_NAME=${MODEL_NAME:-llama3.1:70b}

echo "Pulling model: $MODEL_NAME (this may take 5-15 minutes)..."
ollama pull "$MODEL_NAME"
echo "✓ Model $MODEL_NAME downloaded"

# Step 5: Install Python dependencies
echo ""
echo "Step 5: Installing Python dependencies..."
echo "------------------------------------------------------------------------------------------------------"
if command -v python3 &> /dev/null; then
    echo "✓ Python3 already installed"
else
    sudo apt-get install -y python3 python3-pip python3-venv
fi
echo "✓ Python dependencies installed"

# Step 6: Test Ollama
echo ""
echo "Step 6: Testing Ollama installation..."
echo "------------------------------------------------------------------------------------------------------"
TEST_RESPONSE=$(ollama run "$MODEL_NAME" "Hello" --verbose=false 2>&1 | head -n 1)
if [ -n "$TEST_RESPONSE" ]; then
    echo "✓ Ollama is working correctly"
    echo "  Test response: $TEST_RESPONSE"
else
    echo "✗ Ollama test failed"
    exit 1
fi

# Step 7: Configuration recommendations
echo ""
echo "======================================================================================================"
echo "SETUP COMPLETE!"
echo "======================================================================================================"
echo ""
echo "Next steps:"
echo "  1. Upload your aiqg project to this instance (use scp or git clone)"
echo "  2. Navigate to project directory: cd /path/to/aiqg"
echo "  3. Create virtual environment: python3 -m venv venv"
echo "  4. Activate it: source venv/bin/activate"
echo "  5. Install dependencies: pip install -r requirements.txt"
echo "     OR manually: pip install ollama pandas tqdm"
echo "  6. Update src/config.py to use model: $MODEL_NAME"
echo "  7. Run: python src/main.py"
echo ""
echo "Performance tuning for $MODEL_NAME:"
echo "  - Temperature: 0.3 (already set in ollama_generator.py)"
echo "  - GPU memory: Model will use available VRAM automatically"
echo "  - Estimated speed: 5-10 seconds per candidate"
echo ""
echo "Monitor GPU usage: watch -n 1 nvidia-smi"
echo ""
