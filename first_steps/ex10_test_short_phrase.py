def test_short_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"The entered phrase '{phrase}' is longer than 15 characters"
    print(f"The length of the entered phrase is {len(phrase)} characters")
