from main import main

def test_end_to_end_flow():
    try:
        main()
        assert True
    except Exception as e:
        assert False, str(e)