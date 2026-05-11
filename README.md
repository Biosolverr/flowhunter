FlowHunter
An autonomous AI agent that monitors on-chain capital flows across the Base ecosystem and surfaces early market signals.
Built for Virtuals Protocol using Groq (Llama 3) as the reasoning engine.
What it does

Detects trending tokens and unusual capital movements on Base
Analyzes on-chain activity in real time
Responds to queries via Virtuals Protocol runtime (OpenClaw)
Scores projects by momentum using on-chain + social signals

Stack

FastAPI — HTTP server, OpenClaw-compatible endpoint
Groq / Llama 3 — AI reasoning layer
CoinGecko API — trending token data (free, no key required)
Base RPC — on-chain block and transaction data
DeFiLlama API — TVL and DeFi stats

Project structure
flowhunter/
├── main.py          # FastAPI server + Virtuals endpoints
├── agent.py         # Reasoning loop (Groq + Llama 3)
├── data.py          # On-chain data fetching
├── requirements.txt
└── .env.example
Environment variables
GROQ_API_KEY=your_key_here
Get a free Groq API key at console.groq.com — no credit card required.
API endpoints
MethodPathDescriptionGET/healthHealth checkGET/capabilitiesAgent capabilitiesPOST/inferenceMain inference endpoint (used by Virtuals)
License
MIT
