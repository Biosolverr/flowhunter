import os
from groq import Groq
from data import get_trending_tokens, get_base_activity
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are FlowHunter — an autonomous AI agent that monitors 
on-chain capital flows across the Base ecosystem.

Your personality:
- Direct and data-driven. No fluff.
- You speak like a market intelligence analyst, not a chatbot.
- You surface signals, not opinions.
- You use numbers when you have them.

Your capabilities:
- Detect trending tokens by volume and wallet activity on Base
- Identify unusual capital movements
- Score projects by momentum (mindshare + on-chain activity)
- Alert on early market shifts

When answering:
- Lead with the signal, then explain
- If you have data, use it. If not, say so clearly.
- Keep responses under 200 words — precision over length.
- Format key numbers clearly (e.g. "Volume: $2.4M | Wallets: 1,240 | Trend: UP")
"""


class FlowHunterAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.conversation_history = []

    def think(self, user_message: str) -> str:
        # Собираем контекст из on-chain данных
        context = self._build_context()

        # Добавляем сообщение пользователя в историю
        self.conversation_history.append({
            "role": "user",
            "content": f"{context}\n\nUser query: {user_message}"
        })

        # Ограничиваем историю последними 10 сообщениями
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *self.conversation_history
            ],
            temperature=0.3,   # низкая температура = более точные аналитические ответы
            max_tokens=400
        )

        assistant_message = response.choices[0].message.content

        # Сохраняем ответ в историю
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def _build_context(self) -> str:
        """Собираем живые данные и передаём агенту как контекст"""
        try:
            trending = get_trending_tokens()
            activity = get_base_activity()

            context = f"""[LIVE DATA - Base Ecosystem]
Trending tokens (last 24h): {trending}
Network activity: {activity}
"""
            return context
        except Exception as e:
            return f"[DATA UNAVAILABLE: {str(e)}]"
