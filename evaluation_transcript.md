# Sample Evaluation Transcript

**Scenario**: User checks eligibility for "Rythu Bandhu".

**User (Voice)**: "రైతు బంధు పథకం అంటే ఏమిటి?" (What is Rythu Bandhu scheme?)
**Agent (Internal Logic)**:
- **Planner**: Detects intent `explain_scheme` with param `rythu_bandhu`.
- **Executor**: Calls `get_scheme_details("rythu_bandhu")`. Returns scheme data.
- **Responder**: Synthesizes Telugu explanation.
**Agent (Voice Output)**: "రైతు బంధు అనేది తెలంగాణ ప్రభుత్వం రైతుల కోసం ప్రవేశపెట్టిన పథకం. ఇది వ్యవసాయ పెట్టుబడి కోసం ఎకరానికి రూ. 5000 ఆర్థిక సాయం అందిస్తుంది."

---

**Scenario**: Eligibility Check.

**User (Voice)**: "నాకు 5 ఎకరాల పొలం ఉంది, నేను రైతుని. నాకు ఈ పథకం వస్తుందా?" (I have 5 acres land, I am a farmer. Will I get this scheme?)
**Agent (Internal Logic)**:
- **Planner**: Detects intent `check_eligibility`. Extracts `user_data`: `{"occupation": "farmer", "land_ownership": true}`.
- **Executor**: Calls `check_eligibility("rythu_bandhu", user_data)`. Returns `{"eligible": True}`.
- **Responder**: Synthesizes congratulatory message.
**Agent (Voice Output)**: "అభినందనలు! మీరు రైతు బంధు పథకానికి అర్హులు. మీకు రైతుల జాబితాలో పేరు ఉంటే ఈ సాయం అందుతుంది."

---

**Scenario**: Missing Information.

**User (Voice)**: "నాకు కళ్యాణ లక్ష్మి వస్తుందా?" (Will I get Kalyana Lakshmi?)
**Agent (Internal Logic)**:
- **Planner**: Detects intent `check_eligibility` but sees missing `income` and `caste` info. Returns `ask_missing_info`.
- **Executor**: Returns request for missing fields.
- **Responder**: Asks user for income and caste.
**Agent (Voice Output)**: "కళ్యాణ లక్ష్మి పథకం కోసం దరఖాస్తు చేసుకోవడానికి, దయచేసి మీ వార్షిక ఆదాయం మరియు కుల వివరాలు తెలియజేయండి."
