# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:**
A number guessing game where the player tries to guess a randomly chosen secret number within a set number of attempts. The game gives "Go Higher" or "Go Lower" hints after each guess and tracks a score across attempts.

**Bugs found:**

1. **Swapped hint messages** — `check_guess` returned "Go HIGHER!" when the guess was too high and "Go LOWER!" when it was too low. The outcome labels ("Too High" / "Too Low") were correct, but the human-readable hint strings were paired to the wrong outcomes.

2. **No input range validation** — `parse_guess` accepted any integer, including negative numbers and values far above the valid range. Entering `-5` or `9999` was treated as a valid guess with no error shown to the player.

3. **Even-attempt string casting** — On every even-numbered attempt, `app.py` silently converted the secret number to a string before passing it to `check_guess`. This caused Python's alphabetical string comparison (`"9" > "42"` → `True`) instead of numeric comparison, producing wrong hints on every other guess. A `try/except TypeError` block was masking the crash this caused rather than fixing the root problem.
4. <img width="1020" height="156" alt="image" src="https://github.com/user-attachments/assets/9f54cd37-42e6-4b99-8a5c-66a0b3da130e" />


**Fixes applied:**

- Corrected the hint messages in `check_guess` in `logic_utils.py` so "Go LOWER!" is returned when the guess exceeds the secret and "Go HIGHER!" when it falls short.
- Added a bounds check in `parse_guess` that rejects any value outside `[low, high]` and returns a descriptive error message to the player.
- Removed the even-attempt `if/else` block in `app.py` that was casting the secret to a string, and removed the now-unnecessary `try/except TypeError` from `check_guess`.
- Moved all four logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` into `logic_utils.py` to separate game logic from UI code.
- Fixed and expanded the pytest suite in `tests/test_game_logic.py` with 7 regression tests, one per bug per scenario, all passing.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]
- [ ] <img width="1379" height="828" alt="image" src="https://github.com/user-attachments/assets/68c9fce4-3787-46bf-8f33-90885aa9108e" />


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
