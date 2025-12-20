# Implementation Plan - Robustness and Segregation Improvements

## Goal Description
Fix the "Repetitive Output" loop issue permanently, improve the fuzzy matching for schemes (e.g., matching "Aarogyasri" to "YSR Aarogyasri"), and ensure the agent explicitly mentions the State/Central category of the scheme.

## User Review Required
> [!IMPORTANT]
> I am adding a stronger check in `app.py` to prevent the agent from replying to the same audio input twice. This relies on `st.session_state`.

## Proposed Changes

### `app.py`
#### [MODIFY] [app.py](file:///c:/Users/nabhi/Downloads/voice%20agent/app.py)
- Move the `last_processed_audio` check **inside** the audio handling block to ensure we *never* send a request to the backend if the audio bytes haven't changed.
- Add a "Clear" mechanism if needed, but primarily rely on byte comparison.

### `tools/definitions.py`
#### [MODIFY] [tools/definitions.py](file:///c:/Users/nabhi/Downloads/voice%20agent/tools/definitions.py)
- Update `get_scheme_details` to be more robust.
- Instead of checking if `query in id`, checks if `id in query` OR `query in id`, and splits query into words to match partials (e.g., if query is "Aarogyasri Scheme", it should find "YSR Aarogyasri").

### `agents/executor.py`
#### [MODIFY] [agents/executor.py](file:///c:/Users/nabhi/Downloads/voice%20agent/agents/executor.py)
- In `executor_agent`: When a scheme is found from the local DB, explicitly wrap the result to include `state` in a way the Responder can't miss (e.g., inject `"segregation_info": "This is a STATE scheme"`).
- Currently, the `state` field exists in JSON, but I will make sure it's passed clearly.

## Verification Plan

### Manual Verification
1.  **Loop Test**: Speak once. Wait for reply. Wait 10 seconds. Ensure it doesn't reply again.
2.  **Fuzzy Match Test**: Say "Tell me about Aarogyasri" (which isn't exact match for `ysr_aarogyasri`). Verify it finds it.
3.  **Segregation Test**: Ask about "Rythu Bandhu". Verify response starts with "Telangana government scheme...".
