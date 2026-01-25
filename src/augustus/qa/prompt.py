"""Prompt templates for Augustus.

This module defines prompt templates for the QA pipeline.
Future implementation will use LangChain prompt templates.
"""

from typing import List


def build_qa_prompt(query: str, context_chunks: List[dict]) -> str:
    """Build a QA prompt from query and context.
    
    Args:
        query: The user's question
        context_chunks: List of retrieved chunks with content and metadata
        
    Returns:
        Formatted prompt string
        
    Note:
        This is a placeholder. Future implementation will use proper templates.
    """
    # Placeholder template
    template = """Answer the following question using only the provided context.
If the answer is not present in the context, explicitly say "I don't know based on the files."

Context:
{context}

Question: {question}

Answer:"""
    
    # Format context from chunks
    context = "\n\n".join([
        f"[{chunk.get('source', 'unknown')}]\n{chunk.get('content', '')}"
        for chunk in context_chunks
    ])
    
    return template.format(context=context, question=query)


def build_system_prompt() -> str:
    """Build the system prompt for Augustus.
    
    Returns:
        System prompt string
        
    Note:
        This defines the core behavior: evidence-first, no hallucinations.
    """
    return """You are Augustus, a helpful assistant that answers questions about folder contents.

Core rules:
1. Answer ONLY using information from the provided context
2. If the answer is not in the context, say "I don't know based on the files"
3. Never guess or use outside knowledge
4. Cite specific files when providing information
5. Be concise and factual"""
