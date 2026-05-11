import requests
import os
from datetime import datetime

# Используем бесплатные публичные API — без ключей
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
BASESCAN_BASE = "https://api.basescan.org/api"
BASESCAN_KEY = os.getenv("BASESCAN_API_KEY", "")  # опционально, бесплатный ключ на basescan.org


def get_trending_tokens() -> str:
    """Получаем trending токены с CoinGecko — полностью бесплатно"""
    try:
        resp = requests.get(
            f"{COINGECKO_BASE}/search/trending",
            timeout=8
        )
        data = resp.json()
        coins = data.get("coins", [])[:5]

        result = []
        for item in coins:
            coin = item.get("item", {})
            name = coin.get("name", "?")
            symbol = coin.get("symbol", "?")
            rank = coin.get("market_cap_rank", "?")
            score = coin.get("score", 0)
            result.append(f"{symbol} ({name}) rank#{rank} score:{score}")

        return " | ".join(result) if result else "no data"

    except Exception as e:
        return f"error: {e}"


def get_base_activity() -> str:
    """Базовая статистика сети Base через публичный RPC"""
    try:
        # Запрашиваем последний блок через публичный Base RPC
        resp = requests.post(
            "https://mainnet.base.org",
            json={
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1
            },
            timeout=8
        )
        block_hex = resp.json().get("result", "0x0")
        block_number = int(block_hex, 16)

        # Получаем количество транзакций в последнем блоке
        resp2 = requests.post(
            "https://mainnet.base.org",
            json={
                "jsonrpc": "2.0",
                "method": "eth_getBlockByNumber",
                "params": [block_hex, False],
                "id": 2
            },
            timeout=8
        )
        block_data = resp2.json().get("result", {})
        tx_count = len(block_data.get("transactions", []))

        return f"block:{block_number} | txs_in_last_block:{tx_count} | checked:{datetime.utcnow().strftime('%H:%M UTC')}"

    except Exception as e:
        return f"error: {e}"


def get_defi_stats() -> str:
    """DeFi статистика через DeFiLlama — бесплатно"""
    try:
        resp = requests.get(
            "https://api.llama.fi/v2/chains",
            timeout=8
        )
        chains = resp.json()
        base = next((c for c in chains if c.get("name", "").lower() == "base"), None)

        if base:
            tvl = base.get("tvl", 0)
            return f"Base TVL: ${tvl/1e9:.2f}B"
        return "Base TVL: no data"

    except Exception as e:
        return f"error: {e}"
