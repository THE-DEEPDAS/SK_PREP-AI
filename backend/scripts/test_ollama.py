import requests
import json

def test_ollama_connection():
    """Test Ollama connection"""
    print("Testing Ollama connection...")
    
    try:
        # Test if Ollama is running
        response = requests.get("http://localhost:11434/api/tags")
        
        if response.status_code == 200:
            print("✓ Ollama is running!")
            models = response.json()
            print(f"✓ Available models: {models}")
            return True
        else:
            print(f"✗ Ollama returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Ollama. Make sure it's running:")
        print("  Run: ollama serve")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_ollama_chat():
    """Test Ollama chat functionality"""
    print("\nTesting Ollama chat...")
    
    try:
        url = "http://localhost:11434/api/generate"
        
        payload = {
            "model": "llama2:7b-chat",
            "prompt": "What is the capital of India? Answer in one sentence.",
            "stream": False
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Ollama chat working!")
            print(f"Response: {result.get('response', '')[:200]}...")
            return True
        else:
            print(f"✗ Chat failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("OLLAMA CONNECTION TEST")
    print("=" * 50)
    
    if test_ollama_connection():
        test_ollama_chat()
    
    print("\n" + "=" * 50)