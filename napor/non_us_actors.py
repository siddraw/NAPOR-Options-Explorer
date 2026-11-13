"""NAPOR: US cases whose actor is not the US (owner rule, 2026-11-12).

Sidd's decision: an action by Israel or another non-US government counts as a US case ONLY when the log's own sources
show a US link: a joint operation, US intelligence, refueling or air defense used in it, the US asked for, approved or
announced it, or the US acts within days as part of the same operation. Otherwise it is NOT a US case and must not be in
any US option. It stays in the event log as a context event (it can still be a trigger or a reply for other rows).

Two lists, both read by the build (tag_check.py fails when they are broken or when a counted case needs an entry):
  LINKS    {theater: {event id: dict(link="what the US link is, from the log's sources", sources="where in the log")}}
           a non-US actor kept as a US case. Needed for any counted case whose actor does not start with "US".
  EXCLUDED {theater: {event id: dict(reason=..., sources=...)}}
           a non-US actor taken OUT of every US option (page data, workbook, backtest, recount).
  REVIEW   {theater: {event id: "why it is a judgment call"}}
           kept, but listed for Sidd to decide. Never fails the build.
WEEKLY: for any new event whose actor is not the US, record the US link here (LINKS) or exclude it (EXCLUDED).
"""

LINKS = {
    "iran": {
        257: dict(link="Trump (the US) announced the Israel-Iran ceasefire himself, so the US is the actor of the logged move.",
                  sources="#257 title: 'Trump announces a ceasefire between Israel and Iran'"),
        86: dict(link="The US wrote the message: Qatari mediators only relay the US's feedback on Iran's plan, so the US is the actor of the logged move.",
                 sources="#86 title and note (Reuters, Sep 30)"),
        2: dict(link="Joint operation: the Pentagon announced Operation Epic Fury (1,000+ targets in 24 hours) with Israel. The US is a main actor.",
                sources="#2 title and note (Pentagon); actor 'US/Israel'"),
    },
    "houthis": {}, "northkorea": {},
    "china": {
        3037: dict(link="The US is the host: Taiwan's vice president stops in New York and San Francisco and US officials greet him (the transit is allowed by the US). Counted as a US high-level contact with Taiwan.",
                   sources="#3037 title (AP photo caption); option F"),
    },
    "venezuela": {},
}

EXCLUDED = {
    "iran": {
        44: dict(reason="Israeli strikes that killed Iranian air-defense crews on Jun 8 2026. The log's only source (AFP via Al Arabiya) reports "
                        "Iranian state media saying two personnel were killed in Israeli strikes. No source in the log shows a US link: no joint "
                        "operation, no US intelligence, refueling or air defense used, no US request, approval or announcement, and no US act "
                        "as part of the same operation. Iran then downed a US Apache (#45) and the US struck back (#46); those are logged "
                        "as their own events, but they follow the Israeli strike and do not make it a US act.",
                sources="#44 (AFP via Al Arabiya, 2026-06-09); census pair 10 (#44 -> #45)"),
    },
    "houthis": {}, "northkorea": {}, "china": {}, "venezuela": {},
}

REVIEW = {
    "iran": {
        43: "Kept for Sidd to decide. Actor is 'US/Iran' and the title says Iran agreed to halt attacks on Israel after the two traded fire on "
            "Jun 6-7. The log's source (NPR via KGOU) is about the Israel-Iran exchange; the log does not say the US mediated, asked for or "
            "announced this halt. The US-Iran memorandum was signed 9 days later (#50). Keep as a US diplomatic case, or exclude it?",
    },
}


def excluded(theater):
    """Event ids that are non-US actions kept out of every US option for this theater."""
    return set((EXCLUDED.get(theater) or {}).keys())
