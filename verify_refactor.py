
import os
import sys
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

# Mock requirements that might fail without API keys during import if they initialize aggressively
# (Though our code seems safe, being careful)

def test_llm_factory():
    print("Testing get_llm...")
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy-key"}):
        from llm import get_llm
        from langchain_openai import ChatOpenAI
        
        llm = get_llm()
        assert isinstance(llm, ChatOpenAI)
        assert llm.model_name == "gpt-4o-mini"
        print("PASS: get_llm returns ChatOpenAI(gpt-4o-mini)")

def test_analysis_functions():
    print("Testing analysis functions structure...")
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy-key"}):
        from analysis import analyze_paper, synthesize_findings
        from llm import get_llm
        
        # We want to verify that llm.invoke() is called
        with patch('analysis.get_llm') as mock_get_llm:
            mock_llm_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.content = "Analysis Result"
            mock_llm_instance.invoke.return_value = mock_response
            mock_get_llm.return_value = mock_llm_instance
            
            # Test analyze_paper
            res = analyze_paper("some text", "Title")
            assert res == "Analysis Result"
            assert mock_llm_instance.invoke.called
            print("PASS: analyze_paper calls llm.invoke")

def test_writing_functions():
    print("Testing writing functions structure...")
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy-key"}):
        from writing import write_review_section
        
        with patch('writing.get_llm') as mock_get_llm:
            mock_llm_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.content = "Draft Section"
            mock_llm_instance.invoke.return_value = mock_response
            mock_get_llm.return_value = mock_llm_instance
            
            # Test write_review_section
            res = write_review_section("Abstract", "Synthesis")
            assert res == "Draft Section"
            assert mock_llm_instance.invoke.called
            print("PASS: write_review_section calls llm.invoke")

if __name__ == "__main__":
    try:
        test_llm_factory()
        test_analysis_functions()
        test_writing_functions()
        print("\nAll structure tests passed!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        import traceback
        traceback.print_exc()
