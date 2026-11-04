"""NAPOR phase groups: the page lists war phases under era headings instead of one long grid of tiles.

A group is a heading plus the phase names under it, in time order. The page works out the years shown next to the
heading from the phase dates, so only the heading text lives here. Pure presentation: no risk number reads this file.

A phase that is not listed (the weekly agent added a new one) joins the group of the phase just before it, so the page
never breaks; add it here when you name the phase so it can start a new heading if it should.
"""

GROUPS = {
    "iran": [
        ("Revolution and proxy war", ["Hostage crisis", "Proxy war and Iran-Contra", "Tanker War"]),
        ("Quiet years and containment", ["Quiet years", "Embargo and containment", "Nuclear file opens"]),
        ("Sanctions and the nuclear deal", ["Sanctions build-up", "Nuclear deal years"]),
        ("Maximum pressure and shadow conflict", ["Maximum pressure begins", "Maximum-pressure crisis", "Shadow conflict"]),
        ("The 2025-26 war", ["Twelve-day war", "Pre-war standoff", "Open war", "Fragile ceasefire", "Low-intensity war", "Holding pattern"]),
    ],
    "houthis": [
        ("Takeover and the Saudi-led war", ["Houthi takeover and US pullout", "Saudi-led war; US backs it from the side",
                                            "Kuwait talks and the road to the Red Sea attacks", "First missile attacks"]),
        ("Quiet years", ["Quiet years: designations and arms seizures"]),
        ("Red Sea attacks and the US-UK strikes", ["Red Sea shipping attacks begin", "US-UK strikes and the shipping war", "End of the 2024 campaign"]),
        ("Gaza ceasefires and Rough Rider", ["Gaza-ceasefire pause", "Operation Rough Rider", "US-Houthi ceasefire, attacks on other ships", "Gaza-ceasefire lull"]),
        ("The Iran war", ["Iran war and Saudi-Houthi front"]),
    ],
    "northkorea": [
        ("Nuclear crisis and the Agreed Framework", ["NPT crisis and the Agreed Framework", "Framework years, Taepodong and Albright"]),
        ("Uranium crisis and talks", ["Axis of evil and the uranium crisis", "Six-party talks and first tests"]),
        ("Kim Jong Un and the nuclear tests", ["Cheonan, Yeonpyeong and the Kim Jong Un years", "Fourth to sixth test run-up", "Nuclear and ICBM tests"]),
        ("Summits and quiet", ["Summits and stalled talks", "Quiet and Biden review"]),
        ("Launch surge and the second Trump term", ["Record launch pace", "Strategic assets and trilateral drills", "Second Trump term"]),
    ],
    "china": [
        ("Crisis, engagement and incidents", ["Third Taiwan Strait Crisis", "Engagement and the embassy bombing", "EP-3 collision and the Bush years"]),
        ("Obama to the trade war", ["Obama: sales, summits and incidents at sea", "FONOPs begin and the Trump transition", "Trade war and the Decatur incident"]),
        ("Routine transits to the Pelosi crisis", ["Routine transits and FONOPs", "Visits, sales and sanctions on arms makers", "Pelosi crisis"]),
        ("Named drills and the second Trump term", ["Named drills after leader visits", "Trump second term"]),
    ],
    "venezuela": [
        ("Chavez years", ["Chavez's first term", "Coup attempt, strike and recall", "Bush years: oil threats, expulsions and arms ban"]),
        ("Obama thaw to Maduro", ["Obama years: thaw, Colombia bases and new frictions", "Maduro: expulsions and the first sanctions"]),
        ("Trump sanctions and deals", ["Trump: sanctions and the military option", "Sanctions and deals before the buildup"]),
        ("Naval buildup to Maduro's capture", ["Bounty, naval buildup and first boat strikes", "Carrier and Southern Spear", "Blockade and tanker seizures",
                                               "Maduro captured; interim government cooperates"]),
    ],
}


def tag(theater, phases):
    """Add a 'group' heading to each phase dict (time order). Unlisted phases join the group before them."""
    where = {n: g for g, names in GROUPS.get(theater, []) for n in names}
    prev = None
    for p in phases:
        p["group"] = where.get(p["name"], prev or "Phases")
        prev = p["group"]
    return phases
