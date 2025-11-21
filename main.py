#!/usr/bin/env python3
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.bot import CorrectFlowBot

async def main():
    """Main entry point"""
    bot = CorrectFlowBot()
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Bot interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")