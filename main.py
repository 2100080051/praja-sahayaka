import sys
import argparse
from services.voice_service import listen_mic, speak_telugu
from services.llm_service import planner_agent
from agents.executor import executor_agent, responder_agent
from services.memory_service import save_interaction
import colorama
from colorama import Fore, Style

colorama.init()

def run_voice_loop():
    print(Fore.GREEN + "Telugu Voice Agent initialized..." + Style.RESET_ALL)
    speak_telugu("నమస్కారం! నేను మీ ప్రభుత్వ పథకాల సహాయకుడిని. నేను మీకు ఎలా సహాయపడగలను?")
    
    while True:
        try:
            # 1. Listen
            user_text = listen_mic()
            if not user_text:
                continue
                
            if "నమస్తే" in user_text or "stop" in user_text.lower() or "ఆపు" in user_text:
                if "ఆపు" in user_text or "stop" in user_text.lower():
                    speak_telugu("ధన్యవాదాలు. శుభదినం!")
                    break

            # 2. Plan
            print(Fore.CYAN + "Planning..." + Style.RESET_ALL)
            plan = planner_agent(user_text)
            
            # 3. Execute
            print(Fore.YELLOW + "Executing..." + Style.RESET_ALL)
            result = executor_agent(plan)
            
            # 4. Respond
            print(Fore.MAGENTA + "Generating Response..." + Style.RESET_ALL)
            response_telugu = responder_agent(user_text, result)
            
            # 5. Speak
            speak_telugu(response_telugu)
            
            # 6. Save Memory
            save_interaction(user_text, response_telugu, plan)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(Fore.RED + f"Error occurred: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", action="store_true", help="Run in text-only mode for testing")
    args = parser.parse_args()
    
    if args.cli:
        print("Running in CLI Text Mode. Type 'exit' to quit.")
        while True:
            user_text = input("You (Telugu/English text): ")
            if user_text.lower() == "exit":
                break
            plan = planner_agent(user_text)
            result = executor_agent(plan)
            response = responder_agent(user_text, result)
            print(f"Agent: {response}")
            save_interaction(user_text, response, plan)
    else:
        run_voice_loop()
