def test_functions(functions):
    """Test all functions."""
    total = 0
    fail = 0
    ok = 0
    for func in functions:
        try:
            print(f"{func.__doc__.strip().split(chr(10))[0]}: ", end="")
            func()
            print("OK")
            ok += 1
        except AssertionError as e:
            print("\n\n# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #")
            print(f"FAIL - {e}")
            print("# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #\n")
            fail += 1
        total += 1
    print(f"Total tests: {total}, OK: {ok}, FAIL: {fail}")

    # print(f"Score: {ok/total*100:.2f}%")

    return {"total": total, "ok": ok, "fail": fail}
