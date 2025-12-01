import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
from tool import make_call

async def main():
    # Load environment variables
    load_dotenv(Path(__file__).parent / '.env')
    
    # Get phone number from user input
    phone_number = input("Enter phone number to call (include country code, e.g., +1234567890): ")
    
    # Make the call
    print(f"Initiating call to {phone_number}...")
    success = await make_call(phone_number)
    
    if success:
        print("Call initiated successfully! The agent will handle the call.")
        print("Press Ctrl+C to exit (this won't end the call).")
        try:
            # Keep the script running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nExiting test script. The call will continue.")
    else:
        print("Failed to initiate call. Check the logs for more information.")

if __name__ == "__main__":
    asyncio.run(main())
