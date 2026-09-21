# What I checked, and what the agent got wrong

## What the agent got wrong

The km-to-miles conversion factor was inverted: the original code used 1.609 (which is
kilometres *per* mile) instead of 0.621371 (miles *per* kilometre). So every distance
reported to the UK partner garage was roughly 2.6× too large. The agent caught this and
flipped the constant to the correct value in `fleet_utils.py`.

The agent kept integer division (//) in wear_percent, which silently floored the wear to 
a multiple of 100. A car that had used 80 to 99 % of its service interval was reported as 
0 % wear, so the early warning never triggered. The agent even labeled it "kept the original 
behavior" instead of questioning it. I replaced // with / so the real percentage is returned 
directly, and verified it with verify.py.

## What I checked before I accepted its work

I ran `verify.py` after each change and watched the PASS/FAIL counts. For the wear fix I
confirmed by hand: a car at 14,900 km of a 15,000 km interval should report 99.3%, and
that is exactly what `wear_percent(14900, 15000)` now returns. For the 80% threshold and
the 15,000 km interval I checked `km_wachter.py` directly — `SERVICE_INTERVAL_KM = 15000`
and `WARN_AT_PERCENT = 80` are unchanged. I also ran the test suite to make sure no
existing test broke.

## What the data actually said

Total odometer mileage and age in years looked like the obvious predictors of breakdown,
but when I compared the two groups (broke_down = 0 vs 1) column by column, their means
were virtually identical: ~53,300 km vs ~53,400 km, and ~5.9 years vs ~5.9 years. They
carry almost no signal.

The real predictors are `km_since_service` (7,261 km average for healthy cars vs 11,678 km
for cars that later broke down — a 61% gap) and `load_factor` (0.506 vs 0.601). The risk
score in `analyze.py` is built from those two columns only, weighted 55/25 with a
20% contribution from `avg_daily_km` which showed a moderate gap as well.
