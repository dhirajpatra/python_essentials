"""
Evaluation metrics for grounding and guardrails in RAG systems
"""
import numpy as np
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from guardrails import Guard
from guardrails.hub import ToxicLanguage, DetectJailbreak


# =====================================================================
# 1. INLINE GUARDRAIL POSE (Runtime Interception using Guardrails AI)
# =====================================================================
def apply_runtime_guardrails(user_prompt: str, generated_answer: str) -> str:
    """Validates prompt and answer at runtime before sending to the client."""
    # Initialize guard rail rules
    guard = Guard().use_many(
        ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail="exception"),
        DetectJailbreak(on_fail="exception")
    )

    try:
        # Validate generation output against toxic language and prompt injections
        guard.validate(generated_answer)
        return generated_answer
    except Exception as e:
        # Fallback response when a guardrail fails
        return "I'm sorry, but the generated response violated safety and policy guidelines."


# =====================================================================
# 2. DETERMINISTIC GROUNDING CHECK (Cosine Similarity Thresholding)
# =====================================================================
def check_vector_grounding(
        context_embedding: np.ndarray,
        answer_embedding: np.ndarray,
        threshold: float = 0.70
) -> bool:
    """Calculates cosine similarity to verify response distance from context."""
    dot_product = np.dot(context_embedding, answer_embedding)
    norm_ctx = np.linalg.norm(context_embedding)
    norm_ans = np.linalg.norm(answer_embedding)

    similarity = dot_product / (norm_ctx * norm_ans)
    return float(similarity) >= threshold


# =====================================================================
# 3. EVALUATION METRICS (RAG Triad using DeepEval)
# =====================================================================
def run_rag_evaluation(query: str, retrieved_context: list[str], generated_answer: str) -> dict:
    """Runs Faithfulness (Grounding) and Answer Relevancy metrics using DeepEval."""
    # Construct standard LLM Test Case
    test_case = LLMTestCase(
        input=query,
        actual_output=generated_answer,
        retrieval_context=retrieved_context
    )

    # 1. Faithfulness Metric: Measures if answer is strictly derived from retrieved context
    faithfulness_metric = FaithfulnessMetric(threshold=0.7, model="gpt-4o-mini")
    faithfulness_metric.measure(test_case)

    # 2. Answer Relevancy Metric: Measures if output directly answers user query
    relevancy_metric = AnswerRelevancyMetric(threshold=0.7, model="gpt-4o-mini")
    relevancy_metric.measure(test_case)

    return {
        "faithfulness_score": round(faithfulness_metric.score, 4),
        "faithfulness_passed": faithfulness_metric.is_successful(),
        "relevancy_score": round(relevancy_metric.score, 4),
        "relevancy_passed": relevancy_metric.is_successful(),
        "reasoning": faithfulness_metric.reason
    }


# =====================================================================
# Execution Demo
# =====================================================================
if __name__ == "__main__":
    user_query = "What is the policy for processing customer refunds?"
    retrieved_chunks = [
        "Refunds are processed within 30 days of receipt with proof of purchase.",
        "Custom items are non-refundable under any circumstance."
    ]
    raw_llm_answer = "You can get a full refund within 30 days if you have proof of purchase."

    # 1. Run Runtime Guardrail Pose
    safe_answer = apply_runtime_guardrails(user_query, raw_llm_answer)
    print(f"[Guardrail Passed Answer]: {safe_answer}\n")

    # 2. Run Offline Evaluation Suite (DeepEval)
    eval_results = run_rag_evaluation(user_query, retrieved_chunks, safe_answer)
    print(f"--- DeepEval RAG Evaluation Results ---")
    print(f"Faithfulness Score: {eval_results['faithfulness_score']} | Passed: {eval_results['faithfulness_passed']}")
    print(f"Answer Relevancy:   {eval_results['relevancy_score']} | Passed: {eval_results['relevancy_passed']}")