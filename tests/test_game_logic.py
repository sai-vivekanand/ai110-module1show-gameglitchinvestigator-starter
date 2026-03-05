from logic_utils import check_guess, parse_guess


# --- existing tests (fixed to unpack the (outcome, message) tuple) ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug 1: hints were swapped ---
# check_guess used to return "Go HIGHER!" when guess > secret and "Go LOWER!" when guess < secret.

def test_too_high_message_says_go_lower():
    # Guess is above secret → player must go lower, not higher
    _, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message}"

def test_too_low_message_says_go_higher():
    # Guess is below secret → player must go higher, not lower
    _, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message}"


# --- Bug 2: negative and out-of-range numbers were accepted ---
# parse_guess had no bounds check, so -5 or 999 were treated as valid guesses.

def test_negative_number_rejected():
    ok, value, err = parse_guess("-5", low=1, high=100)
    assert not ok
    assert value is None
    assert err is not None

def test_number_above_range_rejected():
    ok, value, err = parse_guess("999", low=1, high=100)
    assert not ok
    assert value is None
    assert err is not None

def test_valid_number_accepted():
    ok, value, err = parse_guess("42", low=1, high=100)
    assert ok
    assert value == 42
    assert err is None


# --- Bug 3: even-attempt string casting broke comparisons ---
# On even attempts, secret was cast to str, so "9" > "42" evaluated True (alphabetical order).
# The fix was to always compare int to int. These tests confirm check_guess works correctly
# for numbers whose string ordering differs from numeric ordering.

def test_single_digit_vs_two_digit_high():
    # 9 < 42 numerically, but "9" > "42" alphabetically — must use numeric comparison
    outcome, message = check_guess(9, 42)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_single_digit_vs_two_digit_low():
    # 42 > 9 numerically, but this confirms the reverse is also handled correctly
    outcome, message = check_guess(42, 9)
    assert outcome == "Too High"
    assert "LOWER" in message
