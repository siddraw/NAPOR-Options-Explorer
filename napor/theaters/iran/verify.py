"""Iran: thin entry point to the independent recount (verify_explorer.py writes explorer/verify.json)."""
def run():
    import verify_explorer
    return verify_explorer.run_iran()
