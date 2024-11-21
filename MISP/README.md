# Goal

The purpose of the script is to uncheck the IDS flag for all attributes belonging to a warning list.

# Description

The script will:
- Process all attributes from event which creation date is within the search timeframe (--last argument)\
- Fetch all events
- Verify all attributes if they have IDS flag set AND belong to a warning list
- If that is the case, uncheck the IDS flag and re-push the attribute

# Usage

```
options:
  -h, --help   show this help message and exit
  --last LAST  Filter events by the last X days (e.g., '1d', '30d').
```

## Examples
### Check all events
```
python3 misp_ids_checker.py
```

### Check events created in the last 7 days
```
python3 misp_ids_checker.py --last 7d
```

### Get help
```
python3 misp_ids_checker.py --help
```

# Improvements
- [ ] Add arg to specifiy warning list to ignore
- [ ] Add mode for unchecking flag based on decay score
- [ ] Push updates per event instead of per attribute
- [ ] Republis the event at the end of the processing
