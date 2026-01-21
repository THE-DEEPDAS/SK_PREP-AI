
import asyncio
from app.services.scheduler_service import SchedulerService

async def main():
    """Start the background scheduler"""
    scheduler = SchedulerService()
    await scheduler.start()
    
    print("Scheduler is running. Press Ctrl+C to stop.")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down scheduler...")

if __name__ == "__main__":
    asyncio.run(main())
