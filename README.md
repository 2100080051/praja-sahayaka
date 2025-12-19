# Telugu Voice-First Government Scheme Assistant

This is an end-to-end agentic AI system that operates in Telugu. It is designed to help users identify and apply for Telangana government schemes.

## Prerequisities
- Python 3.8+
- Active Internet Connection (for STT and LLM)
- Microphone and Speakers

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: On Windows, you might need to install PyAudio manually using pipwin if standard pip fails, but standard pip usually works for newer python versions.*

2. Setup `.env`:
   Ensure your `OPENROUTER_API_KEY` is set in the `.env` file.

## Running the Agent

### Voice Mode (Default)
Run the following command to start the voice interaction loop:
```bash
python main.py
```
- The agent will speak a greeting in Telugu.
- Speak into your microphone in Telugu.
- Wait for the agent to process and reply in Telugu.
- Say "ఆపు" (Aapu) or "Stop" to exit.

### Text/CLI Mode (Debug)
If you want to test the logic without speaking:
```bash
python main.py --cli
```

## Architecture
- **Voice Input**: SpeechRecognition (Google API) for high-accuracy Telugu STT.
- **LLM**: OpenRouter (Gemini Pro/Flash) for reasoning.
- **Planner**: Determines user intent (Eligibility, Explanation, Chit-chat).
- **Executor**: Calls local Python tools defined in `tools/definitions.py`.
- **Evaluator/Responder**: Synthesizes the final helpful Telugu response.
- **Voice Output**: gTTS (Google TTS) for natural sounding Telugu speech without GPU.

## Sample Queries
- "రైతు బంధు పథకం గురించి చెప్పండి" (Tell me about Rythu Bandhu)
- "నేను రైతుని, నాకు 5 ఎకరాల భూమి ఉంది. నేను రైతు బంధుకి అర్హుడినా?" (I am a farmer, I have 5 acres. Am I eligible for Rythu Bandhu?)
