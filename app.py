"""
Financial Analysis System - Main Entry Point
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from app import create_ui

if __name__ == "__main__":
    print("🚀 Starting Financial Analysis System...")
    print("📍 Production-ready version")
    
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
