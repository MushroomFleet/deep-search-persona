"""
Example usage of the Deep Research Pipeline
"""
import os
from pipeline import ResearchPipeline
from config import Config


def example_basic_research():
    """Basic research example"""
    print("\n" + "="*60)
    print("Example 1: Basic Research")
    print("="*60)
    
    # Initialize pipeline (API key loaded from .env file)
    pipeline = ResearchPipeline()
    
    # Execute research
    query = "What are the main challenges in developing AGI?"
    results = pipeline.execute(query, max_iterations=5)
    
    print(f"\nResults saved to: {results['output_file']}")
    return results


def example_with_custom_model():
    """Example with custom model configuration"""
    print("\n" + "="*60)
    print("Example 2: Custom Model Configuration")
    print("="*60)
    
    # Use a different model from OpenRouter
    pipeline = ResearchPipeline(
        model="anthropic/claude-3.5-sonnet"  # Or any other model
    )
    
    query = "Compare different approaches to neural network compression"
    results = pipeline.execute(query, max_iterations=7)
    
    return results


def example_with_online_search():
    """Example using OpenRouter's :online web search feature"""
    print("\n" + "="*60)
    print("Example 3: With Native Web Search (:online)")
    print("="*60)
    
    # Use :online suffix to enable OpenRouter's native web search
    pipeline = ResearchPipeline(
        model="x-ai/grok-4-fast:online"  # :online enables web search & grounding
    )
    
    query = "Recent breakthroughs in renewable energy storage"
    results = pipeline.execute(query)
    
    return results


def example_custom_configuration():
    """Example with custom configuration"""
    print("\n" + "="*60)
    print("Example 4: Custom Configuration")
    print("="*60)
    
    # Modify configuration
    Config.MAX_RESEARCH_ITERATIONS = 15
    Config.SEARCH_RESULTS_PER_QUERY = 10
    Config.MODEL_TEMPERATURE = 0.8
    
    pipeline = ResearchPipeline()
    
    query = "How do transformer architectures work and what are their limitations?"
    results = pipeline.execute(query)
    
    return results


def example_step_by_step():
    """Example showing step-by-step control"""
    print("\n" + "="*60)
    print("Example 5: Step-by-Step Control")
    print("="*60)
    
    from llm_client import OpenRouterClient
    from research_agent import ResearchAgent
    
    # Initialize components separately
    llm = OpenRouterClient()
    agent = ResearchAgent(llm)
    
    # Create research plan
    query = "What is the environmental impact of large language models?"
    plan = agent.plan_research(query)
    
    print(f"\nResearch Plan ({len(plan)} steps):")
    for step in plan:
        print(f"  {step['step']}. {step['query']}")
        print(f"     Reasoning: {step['reasoning']}\n")
    
    # You can now execute steps manually or customize the flow
    return plan


def example_with_output_processing():
    """Example showing how to process outputs"""
    print("\n" + "="*60)
    print("Example 6: Output Processing")
    print("="*60)
    
    pipeline = ResearchPipeline()
    
    query = "What are the key principles of effective prompt engineering?"
    results = pipeline.execute(query, max_iterations=5)
    
    # Access different parts of the results
    print("\n--- Research Metadata ---")
    metadata = results['results']['metadata']
    print(f"Total steps: {metadata['total_steps']}")
    print(f"Average confidence: {metadata['avg_confidence']:.2f}")
    print(f"Phases: {', '.join(metadata['phases_completed'])}")
    
    print("\n--- Research Steps ---")
    for step in results['results']['research_steps']:
        print(f"Step {step['step_number']}: {step['query']}")
        print(f"  Confidence: {step['confidence']:.2f}")
        print(f"  Findings: {len(step['results'].get('key_findings', []))} key points\n")
    
    print("\n--- Final Report Preview ---")
    report = results['results']['final_report']
    print(report[:500] + "...\n")
    
    return results


if __name__ == "__main__":
    # Make sure to set your API key first by creating a .env file:
    # cp .env.example .env
    # Then edit .env and add your actual API key
    
    # Run examples (uncomment the one you want to try)
    
    # example_basic_research()
    # example_with_custom_model()
    # example_with_online_search()
    # example_custom_configuration()
    # example_step_by_step()
    example_with_output_processing()
