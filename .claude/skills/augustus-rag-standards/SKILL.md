---
name: augustus-rag-standards
description: Define how RAG, prompts, retrieval, and citations work in Augustus. Apply whenever working with LangChain, loaders, embeddings, retrieval, prompts, or answer generation.
---

# Augustus RAG Standards

## Ingestion Rules
- Only load text-based files
- Skip binaries and large generated artifacts
- Respect ignore rules (`.augustusignore`, defaults)

## Chunking
- Use deterministic chunking
- Reasonable chunk size (not too small, not too large)
- Preserve file boundaries when possible
- Attach metadata:
  - file path
  - chunk index

## Retrieval
- Always retrieve before answering
- Top-k should be small and relevant
- Retrieval results are the **only allowed context**

## Prompting Rules (Critical)
All prompts must enforce:

- Answer **only** from retrieved context
- If the answer is not present, say you don’t know
- Never invent structure, technologies, or intent

Baseline instruction (must be preserved conceptually):
> You are analyzing the contents of a folder.  
> Answer only using the provided context.  
> If the information is not present, say you do not know.

## Citations
- Answers must reference where information came from
- Cite using file path and short snippet or line range
- No answer without evidence

## Forbidden
- Chain-of-thought leakage
- “Likely”, “probably”, or speculative language
- Mixing external knowledge with folder content

Accuracy > verbosity. Always.