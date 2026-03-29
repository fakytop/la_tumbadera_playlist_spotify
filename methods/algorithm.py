from datetime import datetime
import math

def calculate_score(track):
    popularity = float(track["popularity"])
    release_date_str = track["album"]["release_date"]
    precision = track["album"]["release_date_precision"]
    if precision == "year":
        release_date_str += "-01-01"
    elif precision == "month":
        release_date_str += "-01"
    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
    days = (datetime.now().date() - release_date).days
    if days <= 90:
        penalty_factor = 1.0
    else:
        penalty_factor = 1/(1+math.log10(days/60)) 

    score_base = popularity * penalty_factor

    boost = 0
    if days <= 10:
        if popularity > 2:
            boost = 40 * (1-(days/15))
    elif days <= 90:
        boost = 10 * (1-(days/90))

    final_score = score_base + boost
    return final_score
        