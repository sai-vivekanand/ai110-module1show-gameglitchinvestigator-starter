# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, three bugs were present that made it unplayable.

**Bug 1: Hints were backwards**
I expected that when my guess was too high, the game would tell me to go lower, and vice versa. Instead, the hints were completely swapped — guessing too high showed "Go HIGHER!" and guessing too low showed "Go LOWER!" This was caused by the wrong messages being returned in `check_guess`: the "Too High" outcome was paired with the "Go HIGHER!" message instead of "Go LOWER!".

**Bug 2: Negative numbers (and out-of-range numbers) were accepted**
I expected the game to only accept numbers within the valid range (e.g., 1–100 on Normal difficulty). Instead, `parse_guess` had no range validation, so entering `-5` or `999` was treated as a valid guess. The fix was to add a bounds check in `parse_guess` after parsing the integer.

**Bug 3: Hints were unreliable on every other attempt**
I expected the hint to be consistently correct based on my guess. Instead, on even-numbered attempts the game secretly converted the secret number to a string before comparing. This caused Python's string comparison rules to apply (e.g., `"9" > "42"` is `True` alphabetically), producing wrong hints regardless of the actual guess. A `try/except TypeError` block was masking this broken comparison rather than fixing it.

---

## 2. How did you use AI as a teammate?

I used Claude (Claude Code / Sonnet 4.6) as my primary AI collaborator throughout this project.

**Correct AI suggestion — identifying the swapped hint messages:**
When I described the symptom ("it always shows Go Lower"), Claude read `check_guess` and immediately spotted that the messages were paired to the wrong outcomes: `"Too High"` was returning `"Go HIGHER!"` and `"Too Low"` was returning `"Go LOWER!"`. The fix was a one-line swap of the message strings. I verified it by playing the game manually — guessing above and below the secret now shows the correct direction — and confirmed it with the `test_too_high_message_says_go_lower` and `test_too_low_message_says_go_higher` pytest cases.

**Incorrect/misleading AI suggestion — removing the try/except before diagnosing the root cause:**
Claude initially suggested removing the `try/except TypeError` block in `check_guess` at the same time as fixing the hint messages, framing it as "no longer needed." This was misleading because the `try/except` was actually a symptom of a separate, deeper bug — the even-attempt string casting in `app.py`. If I had only removed the `try/except` without also removing the string cast, the game would have crashed on even-numbered attempts with an unhandled `TypeError` instead of giving wrong hints. I caught this by reading the `app.py` submit block carefully and tracing where `secret` was set before being passed to `check_guess`.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed only when both manual play and a corresponding pytest case confirmed the correct behavior — I did not consider a fix complete based on code review alone.

For Bug 1 (swapped hints), I ran `test_too_high_message_says_go_lower` and `test_too_low_message_says_go_higher`. These tests call `check_guess` directly with known inputs and assert that the word "LOWER" or "HIGHER" appears in the returned message, so there is no ambiguity about what the function is actually returning.

For Bug 3 (string comparison), I wrote `test_single_digit_vs_two_digit_high`, which passes `guess=9` and `secret=42`. Numerically `9 < 42` so the outcome must be `"Too Low"`, but alphabetically `"9" > "42"` so string comparison would return `"Too High"` instead. Running this test against the unfixed code would have failed, confirming the bug; after the fix it passed. Claude helped me design this specific test case by explaining why single-digit vs two-digit numbers expose the string comparison bug most clearly.

---

## 4. What did you learn about Streamlit and state?

Every time you click a button in Streamlit, the entire script reruns from the top. So in the original app, the line `secret = random.randint(low, high)` was just sitting at the top with no guard — meaning every single click picked a brand new number. The game was basically impossible to win because the target kept changing underneath you.

The way I'd explain it to a friend: imagine every button click refreshes the whole page, like hitting F5 in a browser. If your secret number lives in a regular variable, it gets wiped on every refresh. `st.session_state` is like a sticky note that survives those refreshes — you write to it once and it stays there until you deliberately clear it.

The fix was wrapping the secret generation in `if "secret" not in st.session_state:` so it only runs the first time the app loads, not on every rerun. Once that guard was in place the secret stayed locked in for the whole game.

---

## 5. Looking ahead: your developer habits

One habit I want to keep is writing a regression test right after fixing a bug, not after the whole project is done. On this project, writing `test_single_digit_vs_two_digit_high` immediately after fixing the string-casting bug made me way more confident the fix was real — not just "it looks right in the code." If that test existed before the fix, it would have caught the bug instantly.

Next time I work with AI I'd slow down before accepting a suggestion and ask "does this fix the symptom or the actual cause?" Claude told me to remove the `try/except` and I almost just did it without questioning why it was there in the first place. Taking 30 seconds to trace where `secret` was coming from is what led me to the real bug in `app.py`.

Honestly this project made me trust AI-generated code a lot less than I did before — not in a bad way, more in a healthy way. The bugs here weren't random typos, they were subtle logic mistakes that looked totally fine at first glance. AI can write code fast but it can also confidently write code that's wrong, so treating every output as "probably needs review" feels like the right default now.
