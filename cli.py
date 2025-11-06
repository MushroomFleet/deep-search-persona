#!/usr/bin/env python3
"""
Command Line Interface for Deep Research Pipeline
"""
import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from pipeline import ResearchPipeline
from config import Config


def main():
    parser = argparse.ArgumentParser(
        description="Deep Research Agentic Pipeline - Autonomous AI Research Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic research
  python cli.py "What are the latest developments in quantum computing?"
  
  # With custom iterations
  python cli.py "AI safety research" --iterations 15
  
  # With custom model
  python cli.py "Climate change solutions" --model anthropic/claude-3.5-sonnet
  
  # With search API
  python cli.py "Recent AI breakthroughs" --search-key YOUR_API_KEY
  
  # Specify output directory
  python cli.py "Machine learning trends" --output ./my_research
        """
    )
    
    # Required arguments
    parser.add_argument(
        "query",
        type=str,
        help="Research question or topic to investigate"
    )
    
    # Optional arguments
    parser.add_argument(
        "-i", "--iterations",
        type=int,
        default=None,
        help=f"Maximum research iterations (default: {Config.MAX_RESEARCH_ITERATIONS})"
    )
    
    parser.add_argument(
        "-m", "--model",
        type=str,
        default=None,
        help=f"LLM model to use (default: {Config.DEFAULT_MODEL})"
    )
    
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=None,
        help=f"Model temperature (default: {Config.MODEL_TEMPERATURE})"
    )
    
    parser.add_argument(
        "-k", "--api-key",
        type=str,
        default=None,
        help="OpenRouter API key (or set OPENROUTER_API_KEY env var)"
    )
    
    parser.add_argument(
        "-s", "--search-key",
        type=str,
        default=None,
        help="Search API key (Brave or Serper)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help=f"Output directory (default: {Config.OUTPUT_DIR})"
    )
    
    parser.add_argument(
        "-r", "--results-per-query",
        type=int,
        default=None,
        help=f"Search results per query (default: {Config.SEARCH_RESULTS_PER_QUERY})"
    )
    
    parser.add_argument(
        "--no-intermediate",
        action="store_true",
        help="Don't save intermediate research steps"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Deep Research Pipeline v1.0.0"
    )
    
    args = parser.parse_args()
    
    # Apply configuration overrides
    if args.temperature is not None:
        Config.MODEL_TEMPERATURE = args.temperature
    
    if args.output is not None:
        Config.OUTPUT_DIR = args.output
    
    if args.results_per_query is not None:
        Config.SEARCH_RESULTS_PER_QUERY = args.results_per_query
    
    if args.no_intermediate:
        Config.SAVE_INTERMEDIATE_RESULTS = False
    
    # Setup verbose logging if requested
    if args.verbose:
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    # Validate API key
    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OpenRouter API key is required!", file=sys.stderr)
        print("Set OPENROUTER_API_KEY environment variable or use --api-key", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Initialize pipeline
        print(f"\n{'='*60}")
        print("Initializing Deep Research Pipeline")
        print(f"{'='*60}")
        print(f"Query: {args.query}")
        print(f"Model: {args.model or Config.DEFAULT_MODEL}")
        print(f"Max Iterations: {args.iterations or Config.MAX_RESEARCH_ITERATIONS}")
        print(f"{'='*60}\n")
        
        pipeline = ResearchPipeline(
            api_key=api_key,
            model=args.model,
            search_api_key=args.search_key
        )
        
        # Execute research
        results = pipeline.execute(
            query=args.query,
            max_iterations=args.iterations
        )
        
        # Display results
        print(f"\n{'='*60}")
        print("RESEARCH COMPLETE")
        print(f"{'='*60}")
        print(f"\nResults saved to:")
        print(f"  - JSON: {results['output_file']}")
        print(f"  - Report: {results['report_file']}")
        print(f"\nMetadata:")
        metadata = results['results']['metadata']
        print(f"  - Total Steps: {metadata['total_steps']}")
        print(f"  - Avg Confidence: {metadata['avg_confidence']:.2f}")
        print(f"  - Phases: {', '.join(metadata['phases_completed'])}")
        print(f"\n{'='*60}\n")
        
        # Show report preview
        if args.verbose:
            print("Final Report Preview:")
            print("-" * 60)
            print(results['results']['final_report'][:1000])
            if len(results['results']['final_report']) > 1000:
                print("\n... (truncated) ...")
            print("-" * 60)
        
    except KeyboardInterrupt:
        print("\n\nResearch interrupted by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
