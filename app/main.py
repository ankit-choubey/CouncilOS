import asyncio
from automation.browser_manager import BrowserManager
from automation.chatgpt_client import ChatGPTClient
from utils.logger import console  # Using our Rich logger for clean observability

async def main():
    # 1. Initialize the core infrastructure manager
    manager = BrowserManager()
    
    console.print("[yellow][INFO] Spinning up CouncilOS browser engine...[/yellow]")
    await manager.start()
    console.print("[green][SUCCESS] Persistent context active on chatgpt.com.[/green]")

    # 2. Instantiate the ChatGPT interface client by binding it to the active page state
    client = ChatGPTClient(manager.page)

    # 3. Accept your custom engineering prompt from the terminal interface
    print("") # Clean visual separation
    user_prompt = input("🚀 Enter prompt for CouncilOS: ")
    print("")

    if user_prompt.strip():
        console.print(f"[yellow][INFO] Injecting prompt into DOM execution target...[/yellow]")
        await client.send_prompt(user_prompt)
        
        console.print("[yellow][INFO] Polling DOM stream for token stabilization...[/yellow]")
        response = await client.wait_for_response()
        
        # Output the clean, extracted text payload to the terminal console
        console.print("\n[bold green]=== COUNCILOS EXTRACTION PIPELINE ===[/bold green]\n")
        print(response)
        console.print("\n[bold green]=====================================[/bold green]\n")
    else:
        console.print("[red][WARN] Empty prompt provided. Skipping execution loop.[/red]")

    # 4. Gracefully teardown browser primitives to prevent zombie Chromium threads
    input("👉 Execution completed. Press Enter to safely close the session...")
    console.print("[yellow][INFO] Shutting down infrastructure...[/yellow]")
    await manager.stop()
    console.print("[green][SUCCESS] CouncilOS environment safely offline.[/green]")

if __name__ == "__main__":
    # Launch the asynchronous loop runtime required by Playwright
    asyncio.run(main())