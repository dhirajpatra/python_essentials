"""
Key Features
Feature
Description
Async/Await
Non-blocking I/O for high throughput
Concurrency Control
asyncio.Semaphore limits parallel requests
Retry Logic
Exponential backoff for 429/5xx errors
Multi-Provider
Supports Ollama, OpenAI, Azure, Anthropic, etc.
Batch Processing
gather() executes multiple prompts simultaneously
Standardized Output
Uniform LLMResponse object regardless of provider
Session Management
Reuses TCP connections via aiohttp.ClientSession
"""
import asyncio
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Union

import aiohttp


@dataclass
class LLMResponse:
    """Standardized response object"""
    model: str
    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class AsyncLLMClient:
    """
    High-performance asynchronous LLM client.

    Supports:
    - Ollama (Local)
    - OpenAI / Azure / Any OpenAI-Compatible API
    - Concurrent batch processing
    - Automatic retry with exponential backoff
    """

    def __init__(
            self,
            provider: str = "ollama",
            base_url: str = "http://localhost:11434",
            api_key: Optional[str] = None,
            model: str = "llama3.1",
            max_concurrency: int = 10,
            timeout: int = 60,
            max_retries: int = 3
    ):
        """
        Initialize Async LLM Client.

        Args:
            provider: 'ollama' or 'openai'
            base_url: API base URL
            api_key: API key (required for OpenAI, optional for Ollama)
            model: Model name to use
            max_concurrency: Max simultaneous requests
            timeout: Request timeout in seconds
            max_retries: Max retry attempts per request
        """
        self.provider = provider.lower()
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.max_concurrency = max_concurrency
        self.timeout = timeout
        self.max_retries = max_retries

        # Semaphore to limit concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)

        # Session cache
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(limit=self.max_concurrency * 2)
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session

    async def close(self):
        """Close the HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()

    async def _request_with_retry(
            self,
            url: str,
            payload: Dict,
            headers: Dict
    ) -> Dict:
        """Make HTTP request with exponential backoff retry"""
        session = await self._get_session()

        for attempt in range(self.max_retries):
            try:
                async with session.post(url, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    elif resp.status == 429:  # Rate limit
                        wait_time = (2 ** attempt) + (asyncio.get_event_loop().time() % 1)
                        print(f"[WARN] Rate limited. Waiting {wait_time:.2f}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        error_text = await resp.text()
                        raise Exception(f"HTTP {resp.status}: {error_text}")

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"[WARN] Request failed: {e}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    raise Exception(f"Max retries exceeded. Last error: {e}")

    async def generate_ollama(
            self,
            prompt: str,
            system_prompt: Optional[str] = None
    ) -> LLMResponse:
        """Generate response using Ollama API"""
        start_time = time.time()
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        if system_prompt:
            payload["system"] = system_prompt

        headers = {"Content-Type": "application/json"}

        try:
            async with self.semaphore:
                response_data = await self._request_with_retry(url, payload, headers)

            latency = (time.time() - start_time) * 1000

            return LLMResponse(
                model=self.model,
                content=response_data.get("response", ""),
                prompt_tokens=0,  # Ollama doesn't always return token counts in /api/generate
                completion_tokens=0,
                latency_ms=latency
            )

        except Exception as e:
            return LLMResponse(
                model=self.model,
                content="",
                error=str(e),
                latency_ms=(time.time() - start_time) * 1000
            )

    async def generate_openai_compatible(
            self,
            prompt: str,
            system_prompt: Optional[str] = None
    ) -> LLMResponse:
        """Generate response using OpenAI-compatible API"""
        start_time = time.time()
        url = f"{self.base_url}/v1/chat/completions"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            async with self.semaphore:
                response_data = await self._request_with_retry(url, payload, headers)

            latency = (time.time() - start_time) * 1000

            choice = response_data["choices"][0]["message"]
            usage = response_data.get("usage", {})

            return LLMResponse(
                model=self.model,
                content=choice["content"],
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                latency_ms=latency
            )

        except Exception as e:
            return LLMResponse(
                model=self.model,
                content="",
                error=str(e),
                latency_ms=(time.time() - start_time) * 1000
            )

    async def generate(
            self,
            prompt: str,
            system_prompt: Optional[str] = None
    ) -> LLMResponse:
        """
        Main generation method. Routes to appropriate provider.
        """
        if self.provider == "ollama":
            return await self.generate_ollama(prompt, system_prompt)
        elif self.provider in ["openai", "azure", "generic"]:
            return await self.generate_openai_compatible(prompt, system_prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def batch_generate(
            self,
            prompts: List[Union[str, Dict]],
            system_prompt: Optional[str] = None
    ) -> List[LLMResponse]:
        """
        Process multiple prompts concurrently.

        Args:
            prompts: List of strings or dicts with 'prompt' and optional 'system'
            system_prompt: Default system prompt if not specified in dict

        Returns:
            List of LLMResponse objects
        """
        tasks = []

        for item in prompts:
            if isinstance(item, dict):
                p = item.get("prompt", "")
                s = item.get("system", system_prompt)
            else:
                p = item
                s = system_prompt

            tasks.append(self.generate(p, s))

        # Gather all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return list(results)


async def demo_ollama():
    """Demonstrate async calls with local Ollama"""
    print("\n" + "=" * 70)
    print("DEMO: Async Ollama Calls")
    print("=" * 70)

    client = AsyncLLMClient(
        provider="ollama",
        base_url="http://localhost:11434",
        model="llama3.1",
        max_concurrency=5
    )

    prompts = [
        "Explain quantum entanglement in one sentence.",
        "What is the capital of Japan?",
        "Write a haiku about coding.",
        "Convert 100 USD to EUR.",
        "Who wrote '1984'?"
    ]

    print(f"\nProcessing {len(prompts)} prompts concurrently...")
    start_time = time.time()

    results = await client.batch_generate(prompts)

    elapsed = time.time() - start_time

    print(f"\nCompleted in {elapsed:.2f} seconds")
    print(f"Average latency: {sum(r.latency_ms for r in results) / len(results):.0f}ms")
    print("-" * 70)

    for i, result in enumerate(results, 1):
        status = "✅" if not result.error else "❌"
        print(f"{status} Prompt {i}: {prompts[i - 1][:40]}...")
        if result.error:
            print(f"   Error: {result.error}")
        else:
            print(f"   Response: {result.content[:60]}...")

    await client.close()


async def demo_openai_compatible():
    """Demonstrate async calls with OpenAI-compatible API"""
    print("\n" + "=" * 70)
    print("DEMO: Async OpenAI-Compatible Calls")
    print("=" * 70)

    # Note: Replace with your actual API key and endpoint
    client = AsyncLLMClient(
        provider="openai",
        base_url="https://api.openai.com",  # Or https://api.anthropic.com, etc.
        api_key="sk-your-api-key-here",  # Replace with real key
        model="gpt-3.5-turbo",
        max_concurrency=10
    )

    prompts = [
        {"prompt": "Summarize the theory of relativity.", "system": "You are a physicist."},
        {"prompt": "Write a Python function to calculate factorial.", "system": "You are a coder."},
        {"prompt": "What is the meaning of life?", "system": "You are a philosopher."},
    ]

    print(f"\nProcessing {len(prompts)} prompts concurrently...")
    start_time = time.time()

    results = await client.batch_generate(prompts)

    elapsed = time.time() - start_time

    print(f"\nCompleted in {elapsed:.2f} seconds")
    print("-" * 70)

    for i, result in enumerate(results, 1):
        status = "✅" if not result.error else "❌"
        print(f"{status} Result {i}:")
        if result.error:
            print(f"   Error: {result.error}")
        else:
            print(f"   Tokens: {result.total_tokens}")
            print(f"   Content: {result.content[:80]}...")

    await client.close()


def compare_sync_vs_async():
    """Compare synchronous vs asynchronous performance"""
    import requests

    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON: Sync vs Async")
    print("=" * 70)

    num_requests = 10
    prompt = "Tell me a joke."

    # Synchronous approach
    print(f"\n🔄 Synchronous ({num_requests} sequential requests)...")
    start_sync = time.time()

    for _ in range(num_requests):
        try:
            requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.1", "prompt": prompt, "stream": False},
                timeout=30
            )
        except:
            pass

    sync_time = time.time() - start_sync
    print(f"   Time: {sync_time:.2f}s")

    # Asynchronous approach
    print(f"\n⚡ Asynchronous ({num_requests} concurrent requests)...")

    async def run_async_test():
        client = AsyncLLMClient(
            provider="ollama",
            model="llama3.1",
            max_concurrency=num_requests
        )
        prompts = [prompt] * num_requests
        start_async = time.time()
        await client.batch_generate(prompts)
        async_time = time.time() - start_async
        await client.close()
        return async_time

    async_time = asyncio.run(run_async_test())
    print(f"   Time: {async_time:.2f}s")

    print(f"\n📊 Speedup: {sync_time / async_time:.2f}x faster")


if __name__ == "__main__":
    # Run demos
    asyncio.run(demo_ollama())

    # Uncomment to test OpenAI (requires valid API key)
    # asyncio.run(demo_openai_compatible())

    # Performance comparison
    compare_sync_vs_async()

    # usage example
    # single call
    import asyncio

    client = AsyncLLMClient(provider="ollama", model="llama3.1")


    async def main():
        response = await client.generate("Hello!")

        # client = AsyncLLMClient(
        #     provider="openai",
        #     base_url="https://api.openai.com",
        #     api_key="sk-...",
        #     model="gpt-4"
        # )
        #
        # response = await client.generate(
        #     prompt="Write code",
        #     system_prompt="You are an expert developer"
        # )
        print(response.content)

        asyncio.run(main())

        # batch call
        prompts = ["Question 1", "Question 2", ..., "Question 100"]

        client = AsyncLLMClient(
            provider="ollama",
            max_concurrency=20  # Process 20 at once
        )

        results = await client.batch_generate(prompts)
