# Copyright (c) Microsoft. All rights reserved.

import os
from dotenv import load_dotenv
from pytest_agent_evals import (
    EvaluatorResults,
    evals,
    AzureOpenAIModelConfig,
    FoundryAgentConfig,
    BuiltInEvaluatorConfig,
    CustomPromptEvaluatorConfig,
    CustomCodeEvaluatorConfig
)

load_dotenv()

# Configuration for the Evaluator (Judge)
# We use standard AOAI environment variables for the evaluator
EVAL_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
EVAL_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Configuration for the Agent
# The endpoint for the Foundry Project where the agent is hosted
PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT")



# --- Tests ---

# The Test Class is the main entry point for defining your evaluation suite.
# We use decorators to configure the agent, dataset, and judge model.

@evals.dataset("data.jsonl")  # Specifies the input dataset file (JSONL format)
@evals.judge_model(AzureOpenAIModelConfig(deployment_name=EVAL_DEPLOYMENT, endpoint=EVAL_ENDPOINT)) # Configures the LLM used for "Judge" evaluators
@evals.agent(FoundryAgentConfig(agent_name="okla", project_endpoint=PROJECT_ENDPOINT)) # Links this test class to the Foundry agent
class Test_okla:
    """
    Test class for the Agent: okla.
    Each method represents a specific evaluation criteria (e.g., Relevance, Coherence).
    """
    @evals.evaluator(BuiltInEvaluatorConfig("tool_call_accuracy"))
    def test_tool_call_accuracy(self, evaluator_results: EvaluatorResults):
        """
        Tests the 'tool_call_accuracy' of the agent's response.
        The evaluator is automatically run and the results are populated to evaluator_results.<evaluator_name>
        """
        # Assert that the result is pass
        assert evaluator_results.tool_call_accuracy.result == "pass"



