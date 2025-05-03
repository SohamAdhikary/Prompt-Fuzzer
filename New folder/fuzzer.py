from mutator import simple_mutations, score_mutation  # Import score_mutation
from llm import get_llm_response
from evaluator import evaluate_response
import json
import argparse  # Import the argparse library

def test_prompt(prompt, num_tests=5):
    results = []
    for _ in range(num_tests):
        mutated = simple_mutations(prompt)
        response = get_llm_response(mutated)
        if response is None:
            response = "<NO RESPONSE FROM LLM>"  # Handle missing response
        evaluation = evaluate_response(prompt, response)
        mutation_score = score_mutation(mutated, prompt)  # Calculate mutation score
        results.append({
            "original": prompt,
            "mutated": mutated,
            "response": response,
            "evaluation": evaluation,
            "mutation_score": mutation_score
        })
    return results

def generate_report(results):
    """Create a markdown vulnerability report"""
    with open("VULNERABILITY_REPORT.md", "w") as f:
        f.write("# LLM Prompt Fuzzing Report\n\n")
        f.write(f"**Tested Model**: Gemini 2.0 Flash (Example - REPLACE WITH ACTUAL MODEL!)\n\n")  # Replace with actual model
        f.write("## Top Failure Modes\n")

        failures = [r for r in results if r['evaluation']['safety'] > 0]
        f.write(f"- {len(failures)}/{len(results)} prompts triggered safety filters\n")

        f.write("\n## Most Effective Mutation\n")
        if failures:
            worst = max(failures, key=lambda x: x['evaluation']['safety'])
            f.write(f"- `{worst['mutated']}` → Safety score: {worst['evaluation']['safety']}\n")
        else:
            f.write("- No safety failures detected.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fuzz LLM prompts") # Create an argument parser
    parser.add_argument("prompt", help="The prompt to fuzz") # Add an argument for the prompt
    parser.add_argument("--num_tests", type=int, default=5, help="Number of tests to run") # Add an argument for the number of tests
    args = parser.parse_args() # Parse the arguments

    results = test_prompt(args.prompt, args.num_tests) # Use the arguments
    print(json.dumps(results, indent=2))
    generate_report(results)