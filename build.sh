#!/bin/bash
# Build script for Render deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating necessary directories..."
mkdir -p database
mkdir -p uploads

echo "Initializing database..."
python backend/seed_data.py

echo "Build completed successfully!"
