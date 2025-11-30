#!/usr/bin/env python3
"""Test script to diagnose API key issues"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

print("=" * 60)
print("API Key Diagnostic Test")
print("=" * 60)

if not api_key:
    print("❌ ERROR: No API key found in environment variables")
    print("   Checked: GEMINI_API_KEY, GOOGLE_API_KEY")
    exit(1)

# Clean the key
api_key = api_key.strip()

print(f"✓ API key found")
print(f"  Length: {len(api_key)}")
print(f"  Starts with 'AIza': {api_key.startswith('AIza')}")
print(f"  First 20 chars: {api_key[:20]}...")
print(f"  Last 10 chars: ...{api_key[-10:]}")

# Check for common issues
issues = []
if not api_key.startswith("AIza"):
    issues.append("❌ Key doesn't start with 'AIza' - invalid format")
if len(api_key) < 35 or len(api_key) > 45:
    issues.append(f"⚠️  Key length ({len(api_key)}) seems unusual (expected ~39)")

if " " in api_key:
    issues.append("❌ Key contains spaces - check .env file formatting")

if issues:
    print("\n⚠️  Potential Issues:")
    for issue in issues:
        print(f"  {issue}")

# Try to initialize the client
print("\n" + "=" * 60)
print("Testing Client Initialization")
print("=" * 60)

try:
    from google import genai
    
    # Set as GOOGLE_API_KEY in case library checks that
    os.environ["GOOGLE_API_KEY"] = api_key
    
    print("Attempting to initialize Client with explicit api_key...")
    client = genai.Client(api_key=api_key)
    print("✓ Client initialized successfully with explicit api_key")
    
    # Try a simple test call
    print("\nTesting API call...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[{"role": "user", "parts": [{"text": "Say hello"}]}]
        )
        print("✓ API call successful!")
        print(f"  Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ API call failed: {e}")
        print("\nThis suggests the API key might be:")
        print("  1. Expired or invalid")
        print("  2. Not activated for Gemini API")
        print("  3. Has restrictions that block your IP/domain")
        print("  4. Doesn't have the required permissions")
        print("\nTry:")
        print("  - Creating a new API key at https://aistudio.google.com/apikey")
        print("  - Checking API key restrictions in Google Cloud Console")
        print("  - Ensuring Gemini API is enabled for your project")
        
except ImportError as e:
    print(f"❌ Failed to import google.genai: {e}")
    print("   Make sure you've installed: pip install google-genai")
except Exception as e:
    error_str = str(e)
    print(f"❌ Client initialization failed: {error_str}")
    
    if "API key expired" in error_str or "API_KEY_INVALID" in error_str:
        print("\n🔍 Diagnosis: API Key Authentication Issue")
        print("\nPossible causes:")
        print("  1. The API key has expired (even if it's 'new', it might have been created")
        print("     with an expiration date)")
        print("  2. The API key is invalid or was revoked")
        print("  3. The API key doesn't have Gemini API enabled")
        print("  4. The API key has IP/domain restrictions")
        print("\nSolutions:")
        print("  1. Go to https://aistudio.google.com/apikey")
        print("  2. Create a NEW API key (don't reuse an old one)")
        print("  3. Make sure 'Generative Language API' is enabled")
        print("  4. Check for any restrictions on the key")
        print("  5. Update your .env file with the new key")
    elif "400" in error_str or "INVALID_ARGUMENT" in error_str:
        print("\n🔍 Diagnosis: Invalid Request")
        print("   This might be a model name issue or API version issue")
    else:
        print(f"\n🔍 Full error details: {error_str}")

print("\n" + "=" * 60)

