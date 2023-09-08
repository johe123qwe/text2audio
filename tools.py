"""
Basic example of edge_tts usage.
"""

# import asyncio

import edge_tts


def read_file(file) -> str:
    with open(file, "r") as f:
        return f.read()


async def amain(TEXT, VOICE, OUTPUT_FILE, RATE) -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE)
    await communicate.save(OUTPUT_FILE)


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop_policy().get_event_loop()
#     try:
#         loop.run_until_complete(amain(TEXT, VOICE, OUTPUT_FILE))
#     finally:
#         loop.close()
