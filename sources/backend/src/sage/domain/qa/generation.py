"""Generation step of the RAG pipeline: build the grounded prompt, call the LLM."""

import asyncio
import logging
from functools import lru_cache
from pathlib import Path

from google.cloud import storage

from sage.config import get_app_config
from sage.domain.qa.models import Chunk
from sage.integrations.llm.generate import generate_text

log = logging.getLogger(__name__)

_PROMPT_TEMPLATE = (Path(__file__).parent / "prompts" / "answer_prompt.txt").read_text(
    encoding="utf-8"
)
_NO_DOCUMENTS_CONTEXT = (
    "Nessun documento disponibile (base di conoscenza non ancora popolata o non configurata)."
)


@lru_cache
def _get_storage_client() -> storage.Client:
    config = get_app_config()
    return storage.Client(project=config.project_id)


def _load_instructions() -> str:
    config = get_app_config()
    try:
        client = _get_storage_client()
        blob = client.bucket(config.instructions_bucket).blob(config.instructions_blob)
        return blob.download_as_text(encoding="utf-8").strip()
    except Exception as exc:
        log.warning(
            "Impossibile leggere gs://%s/%s: %s",
            config.instructions_bucket,
            config.instructions_blob,
            exc,
        )
        return ""


def build_prompt(question: str, chunks: list[Chunk], instructions: str = "") -> str:
    context = (
        "\n\n".join(f"[{chunk.source}] {chunk.text}" for chunk in chunks)
        if chunks
        else _NO_DOCUMENTS_CONTEXT
    )
    extra = f"\n{instructions}\n" if instructions else ""
    return _PROMPT_TEMPLATE.format(instructions=extra, context=context, question=question)


async def generate_answer(question: str, chunks: list[Chunk]) -> str:
    instructions = await asyncio.to_thread(_load_instructions)
    prompt = build_prompt(question, chunks, instructions=instructions)
    return await generate_text(prompt)