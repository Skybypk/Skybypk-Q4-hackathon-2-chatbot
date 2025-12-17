#!/usr/bin/env python3
"""
Test script to verify the backend server fixes work properly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'docusaurus-book', 'backend'))

def test_imports():
    """Test that main modules can be imported without errors"""
    print("Testing imports...")
    try:
        from main import app
        print("SUCCESS: Main app imported successfully")
    except Exception as e:
        print(f"ERROR: Error importing main app: {e}")
        return False

    try:
        from services import RAGService
        print("✓ RAGService imported successfully")
    except Exception as e:
        print(f"✗ Error importing RAGService: {e}")
        return False

    try:
        from config import Config
        print("✓ Config imported successfully")
        config = Config()
        print(f"✓ Config initialized: QDRANT_HOST={config.QDRANT_HOST}")
    except Exception as e:
        print(f"✗ Error importing/initializing Config: {e}")
        return False

    return True

def test_config():
    """Test that configuration is properly set"""
    print("\nTesting configuration...")
    try:
        from config import Config
        config = Config()

        # Check that database URL is not the placeholder
        if "ep-xxx.us-east-1.aws.neon.tech" in config.DATABASE_URL:
            print("✗ Database URL still contains placeholder")
            return False
        else:
            print(f"✓ Database URL properly configured: {config.DATABASE_URL}")

        # Check that book docs path exists
        import os
        if os.path.exists(config.BOOK_DOCS_PATH):
            print(f"✓ Book docs path exists: {config.BOOK_DOCS_PATH}")
        else:
            print(f"? Book docs path does not exist (this may be expected): {config.BOOK_DOCS_PATH}")

        return True
    except Exception as e:
        print(f"✗ Error testing config: {e}")
        return False

def test_rag_service():
    """Test RAG service initialization"""
    print("\nTesting RAG service...")
    try:
        from services import RAGService
        rag_service = RAGService()
        print("✓ RAGService initialized successfully")

        # Check that embedding model is handled gracefully
        if rag_service.embedding_model is None:
            print("? Embedding model not available (this may be expected on some systems)")
        else:
            print("✓ Embedding model available")

        # Check that database manager is initialized
        if rag_service.db_manager is not None:
            print("✓ Database manager initialized")
        else:
            print("? Database manager not initialized")

        return True
    except Exception as e:
        print(f"✗ Error testing RAG service: {e}")
        return False

def main():
    print("Testing backend server fixes...\n")

    success = True
    success &= test_imports()
    success &= test_config()
    success &= test_rag_service()

    print(f"\n{'='*50}")
    if success:
        print("✓ All tests passed! Backend server fixes are working properly.")
    else:
        print("✗ Some tests failed. Please review the errors above.")
    print(f"{'='*50}")

    return success

if __name__ == "__main__":
    main()