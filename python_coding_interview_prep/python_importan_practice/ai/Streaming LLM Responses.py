"""
Key Features
Feature
Description
Real-time Output
Yields tokens as soon as they are generated
Sync & Async
Supports both requests (sync) and aiohttp (async)
Multi-Provider
Works with Ollama, OpenAI, Azure, Anthropic, etc.
Error Handling
Gracefully handles connection errors and JSON parsing issues
Performance Metrics
Calculates characters/second speed
Clean Interface
Unified StreamChunk dataclass for all providers
"""
import json
import time
from dataclasses import dataclass
from typing import Optional, Generator, AsyncGenerator

import aiohttp
import requests


@dataclass
class StreamChunk:
    """Represents a single chunk of streamed data"""
    content: str
    is_last: bool = False
    model: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0

    def __str__(self):
        return self.content


class StreamingLLMClient:
    """
    Client for streaming LLM responses.

    Supports:
    - Ollama (Local)
    - OpenAI / Azure / Any OpenAI-Compatible API
    - Sync and Async modes
    - Token counting (if provided by API)
    """

    def __init__(
            self,
            provider: str = "ollama",
            base_url: str = "http://localhost:11434",
            api_key: Optional[str] = None,
            model: str = "llama3.1"
    ):
        self.provider = provider.lower()
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    # ------------------------------------------------------------------
    # Synchronous Streaming (using requests)
    # ------------------------------------------------------------------

    def stream_sync(
            self,
            prompt: str,
            system_prompt: Optional[str] = None
    ) -> Generator[StreamChunk, None, None]:
        """
        Synchronous generator that yields chunks as they arrive.
        """
        if self.provider == "ollama":
            yield from self._stream_ollama_sync(prompt, system_prompt)
        else:
            yield from self._stream_openai_sync(prompt, system_prompt)

    def _stream_ollama_sync(
            self,
            prompt: str,
            system_prompt: Optional[str] = None
    ) -> Generator[StreamChunk, None, None]:
        """Stream from Ollama using requests"""
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            with requests.post(url, json=payload, stream=True) as resp:
                resp.raise_for_status()

                for line in resp.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            chunk_content = data.get("response", "")
                            is_last = data.get("done", False)

                            yield StreamChunk(
                                content=chunk_content,
                                is_last=is_last,
                                model=self.model
                            )
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            yield StreamChunk(content=f"\n[Error: {e}]", is_last=True)

    def _stream_openai_sync(
            self,
            prompt: str,
            system_prompt: Optional[str] = None
    ) -> Generator[StreamChunk, None, None]:
        """Stream from OpenAI-compatible API using requests"""
        url = f"{self.base_url}/v1/chat/completions"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            with requests.post(url, json=payload, headers=headers, stream=True) as resp:
                resp.raise_for_status()

                for line in resp.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith("data: "):
                            line_str = line_str[6:]  # Remove "data: " prefix

                        if line_str.strip() == "[DONE]":
                            yield StreamChunk(content="", is_last=True)
                            break

                        try:
                            data = json.loads(line_str)
                            choice = data["choices"][0]
                            delta = choice.get("delta", {})
                            content = delta.get("content", "")

                            # Check if it's the last chunk (finish_reason present)
                            is_last = choice.get("finish_reason") is not None

                            yield StreamChunk(
                                content=content,
                                is_last=is_last,
                                model=self.model
                            )
                        except (json.JSONDecodeError, KeyError):
                            continue

        except Exception as e:
            yield StreamChunk(content=f"\n[Error: {e}]", is_last=True)

    # ------------------------------------------------------------------
    # Asynchronous Streaming (using aiohttp)
    # ------------------------------------------------------------------

    async def stream_async(
            self,
            prompt: str,
            system_prompt: Optional[str] = None
    ) -> AsyncGenerator[StreamChunk, None]:
        """
        Async generator that yields chunks as they arrive.
        """
        if self.provider == "ollama":
            async for chunk in self._stream_ollama_async(prompt, system_prompt):
                yield chunk
        else:
            async for chunk in self._stream_openai_async(prompt, system_prompt):
                yield chunk

    async def _stream_ollama_async(
            self,
            prompt: str,
            system_prompt: Optional[str] = None
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream from Ollama using aiohttp"""
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        if system_prompt:
            payload["system"] = system_prompt

        connector = aiohttp.TCPConnector(limit=1)
        async with aiohttp.ClientSession(connector=connector) as session:
            try:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()

                    async for line in resp.content:
                        if line:
                            try:
                                data = json.loads(line.decode('utf-8'))
                                chunk_content = data.get("response", "")
                                is_last = data.get("done", False)

                                yield StreamChunk(
                                    content=chunk_content,
                                    is_last=is_last,
                                    model=self.model
                                )
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                yield StreamChunk(content=f"\n[Error: {e}]", is_last=True)

    async def _stream_openai_async(
            self,
            prompt: str,
            system_prompt: Optional[str] = None
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream from OpenAI-compatible API using aiohttp"""
        url = f"{self.base_url}/v1/chat/completions"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        connector = aiohttp.TCPConnector(limit=1)
        async with aiohttp.ClientSession(connector=connector) as session:
            try:
                async with session.post(url, json=payload, headers=headers) as resp:
                    resp.raise_for_status()

                    async for line in resp.content:
                        if line:
                            line_str = line.decode('utf-8')
                            if line_str.startswith("data: "):
                                line_str = line_str[6:]

                            if line_str.strip() == "[DONE]":
                                yield StreamChunk(content="", is_last=True)
                                break

                            try:
                                data = json.loads(line_str)
                                choice = data["choices"][0]
                                delta = choice.get("delta", {})
                                content = delta.get("content", "")
                                is_last = choice.get("finish_reason") is not None

                                yield StreamChunk(
                                    content=content,
                                    is_last=is_last,
                                    model=self.model
                                )
                            except (json.JSONDecodeError, KeyError):
                                continue
            except Exception as e:
                yield StreamChunk(content=f"\n[Error: {e}]", is_last=True)


def print_stream_sync(client: StreamingLLMClient, prompt: str):
    """Helper to print sync stream nicely"""
    print(f"\n🤖 Prompt: {prompt}")
    print("🗣️ Response: ", end="", flush=True)

    start_time = time.time()
    total_chars = 0

    for chunk in client.stream_sync(prompt):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            total_chars += len(chunk.content)
        if chunk.is_last:
            break

    elapsed = time.time() - start_time
    print(f"\n\n⏱️ Time: {elapsed:.2f}s | Speed: {total_chars / elapsed:.1f} chars/sec")


async def print_stream_async(client: StreamingLLMClient, prompt: str):
    """Helper to print async stream nicely"""
    print(f"\n🤖 Prompt: {prompt}")
    print("🗣️ Response: ", end="", flush=True)

    start_time = time.time()
    total_chars = 0

    async for chunk in client.stream_async(prompt):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            total_chars += len(chunk.content)
        if chunk.is_last:
            break

    elapsed = time.time() - start_time
    print(f"\n\n⏱️ Time: {elapsed:.2f}s | Speed: {total_chars / elapsed:.1f} chars/sec")


def main():
    """Demonstrate streaming capabilities"""

    print("=" * 70)
    print("STREAMING LLM DEMONSTRATION")
    print("=" * 70)

    # 1. Sync Streaming with Ollama
    print("\n--- 1. Synchronous Streaming (Ollama) ---")
    ollama_client = StreamingLLMClient(
        provider="ollama",
        model="llama3.1"
    )

    prompt = "Write a short poem about artificial intelligence."
    print_stream_sync(ollama_client, prompt)

    # 2. Async Streaming with Ollama
    print("\n--- 2. Asynchronous Streaming (Ollama) ---")
    import asyncio

    async def run_async_demo():
        await print_stream_async(ollama_client, "Explain quantum computing in 2 sentences.")

    asyncio.run(run_async_demo())

    # 3. Sync Streaming with OpenAI (Example)
    print("\n--- 3. Synchronous Streaming (OpenAI-Compatible) ---")
    # Note: Replace with your actual API key
    openai_client = StreamingLLMClient(
        provider="openai",
        base_url="https://api.openai.com",
        api_key="sk-your-key-here",  # Replace with real key
        model="gpt-3.5-turbo"
    )

    # Uncomment to test (requires valid API key)
    # print_stream_sync(openai_client, "What is the capital of France?")


if __name__ == "__main__":
    main()

    # simple streaming
    client = StreamingLLMClient(provider="ollama", model="llama3.1")

    for chunk in client.stream_sync("Tell me a joke"):
        print(chunk.content, end="", flush=True)

    # async streaming
    import asyncio

    client = StreamingLLMClient(provider="ollama", model="llama3.1")


    async def handle_request():
        async for chunk in client.stream_async("Write code"):
            # Send chunk to WebSocket or HTTP stream
            send_to_client(chunk.content)


    asyncio.run(handle_request())


    # collecting full response
    def get_full_response(client, prompt):
        full_text = ""
        for chunk in client.stream_sync(prompt):
            full_text += chunk.content
        return full_text
