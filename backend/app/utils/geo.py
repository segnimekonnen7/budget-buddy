US_STATE_TO_ABBR = {
 "alabama":"AL","alaska":"AK","arizona":"AZ","arkansas":"AR","california":"CA","colorado":"CO","connecticut":"CT","delaware":"DE",
 "florida":"FL","georgia":"GA","hawaii":"HI","idaho":"ID","illinois":"IL","indiana":"IN","iowa":"IA","kansas":"KS","kentucky":"KY",
 "louisiana":"LA","maine":"ME","maryland":"MD","massachusetts":"MA","michigan":"MI","minnesota":"MN","mississippi":"MS","missouri":"MO",
 "montana":"MT","nebraska":"NE","nevada":"NV","new hampshire":"NH","new jersey":"NJ","new mexico":"NM","new york":"NY","north carolina":"NC",
 "north dakota":"ND","ohio":"OH","oklahoma":"OK","oregon":"OR","pennsylvania":"PA","rhode island":"RI","south carolina":"SC",
 "south dakota":"SD","tennessee":"TN","texas":"TX","utah":"UT","vermont":"VT","virginia":"VA","washington":"WA","west virginia":"WV",
 "wisconsin":"WI","wyoming":"WY","district of columbia":"DC","washington dc":"DC","dc":"DC"
}

def expand_location_terms(raw: str) -> list[str]:
    """Expand comma/pipe-separated terms into SQL ILIKE patterns (with abbrs if state)."""
    if not raw: return []
    pats = []
    for chunk in raw.replace("|", ",").split(","):
        t = chunk.strip()
        if not t: continue
        pats.append(f"%{t}%")
        abbr = US_STATE_TO_ABBR.get(t.lower())
        if abbr:
            pats.append(f"%{abbr}%")
    return pats
