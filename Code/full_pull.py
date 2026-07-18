import requests
import numpy as np
import pandas as pd
import datetime
import os

def full_pull(): 
    '''
    Pulls the latest card set information from the YGOProDeck API and returns a DataFrame with the relevant data.
    '''
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?misc=yes"
    data = requests.get(url).json()["data"]

    rows = []
    for c in data:
        for s in c.get("card_sets", []) or []:
            # Extract card_prices (may be a list of dicts)
            card_prices = c.get("card_prices", [{}])[0] if c.get("card_prices") else {}
            
            # Extract banlist_info (may be None)
            banlist_info = c.get("banlist_info", {})

            # Extract misc_info (may be None)
            misc_info = c.get("misc_info", [{}])[0] if c.get("misc_info") else {}

            rows.append({
                "card_id": c.get("id"),
                "name": c.get("name"),
                "desc": c.get("desc"),
                "pend_desc": c.get("pend_desc"),
                "monster_desc": c.get("monster_desc"),
                "type": c.get("type"),
                "subtype": c.get("humanReadableCardType"),
                "frame": c.get("frameType"),
                "race": c.get("race"),
                "archetype": c.get("archetype"),
                "atk": c.get("atk"),
                "def": c.get("def"),
                "level": c.get("level"),
                "attribute": c.get("attribute"),
                "linkval": c.get("linkval"),
                "linkmarkers": c.get("linkmarkers"),
                "scale": c.get("scale"),
                "set_name": s.get("set_name"),
                "set_code": s.get("set_code"),
                "rarity": s.get("set_rarity"),
                "rarity_code": s.get("set_rarity_code"),
                "price": float(s.get("set_price")) if s.get("set_price") not in (None, "", "0.00") else None,

                # Card prices fields
                "tcgplayer_price": float(card_prices.get("tcgplayer_price", "0.00")) if card_prices.get("tcgplayer_price") not in (None, "", "0.00") else None,
                "ebay_price": float(card_prices.get("ebay_price", "0.00")) if card_prices.get("ebay_price") not in (None, "", "0.00") else None,
                "amazon_price": float(card_prices.get("amazon_price", "0.00")) if card_prices.get("amazon_price") not in (None, "", "0.00") else None,
                "coolstuffinc_price": float(card_prices.get("coolstuffinc_price", "0.00")) if card_prices.get("coolstuffinc_price") not in (None, "", "0.00") else None,

                # Banlist info fields
                "banlist_tcg": banlist_info.get("ban_tcg"),
                "banlist_ocg": banlist_info.get("ban_ocg"),
                "banlist_goat": banlist_info.get("ban_goat"),

                # Misc info fields
                "has_effect": misc_info.get("has_effect"),
                "views": misc_info.get("views"),
                "viewsweek": misc_info.get("viewsweek"),
                "upvotes": misc_info.get("upvotes"),
                "downvotes": misc_info.get("downvotes"),
                "formats": misc_info.get("formats"),
                "tcg_date": misc_info.get("tcg_date"),
                "ocg_date": misc_info.get("ocg_date"),
                "md_rarity": misc_info.get("md_rarity"),
                "konami_id": misc_info.get("konami_id"),
            })
    
    df = pd.DataFrame(rows)
    df['time_pulled'] = datetime.datetime.now()

    # Remove cards with neither a tcg_date or ocg_date
    df = df[df['tcg_date'].notna() | df['ocg_date'].notna()]

    # Save the first set_code for each card_id+set_name+rarity combination
    first_set_code = df.groupby(['card_id', 'set_name', 'rarity'])['set_code'].first().reset_index()

    # Remove the set_code column
    df_nosetcode = df.drop(columns=['set_code'])

    # Remove duplicate rows based on card_id, set_name, and rarity
    df_unique = df_nosetcode.drop_duplicates(subset=['card_id', 'set_name', 'rarity'])

    # Reattach the saved first set_code value
    df_final = df_unique.merge(first_set_code, on=['card_id', 'set_name', 'rarity'], how='left')

    # Calculate number of printings (card sets) for each card_id
    printings_per_card = df.groupby('card_id').size().rename('num_printings')

    # Calculate number of unique rarities for each card_id
    rarities_per_card = df.groupby('card_id')['rarity'].nunique().rename('num_rarities')

    # Attach these to the main DataFrame
    df_final = df_final.merge(printings_per_card, left_on='card_id', right_index=True)
    df_final = df_final.merge(rarities_per_card, left_on='card_id', right_index=True)
    
    return df_final

def feature_engineer(df):
    """
    Creates features from the DataFrame for model training.
    """
    # Count the number of formats per card
    df['num_formats'] = df['formats'].apply(lambda x: len(set(x)) if isinstance(x, list) else 0)

    # Create a binary 1/0 indicator for having an archetype
    df['has_archetype'] = df['archetype'].apply(lambda x: 1 if pd.notna(x) else 0)

    # For every Spell/Trap update their attribute to match their card type
    df.loc[df['frame'] == 'spell', 'attribute'] = 'Spell'
    df.loc[df['frame'] == 'trap', 'attribute'] = 'Trap'

    # Create the average price feature
    df['average_price'] = df[['tcgplayer_price', 'ebay_price', 'amazon_price', 'coolstuffinc_price']].mean(axis=1)

    # Create the max and min price
    df['max_price'] = df[['tcgplayer_price', 'ebay_price', 'amazon_price', 'coolstuffinc_price']].max(axis=1)
    df['min_price'] = df[['tcgplayer_price', 'ebay_price', 'amazon_price', 'coolstuffinc_price']].min(axis=1)

    # Create the price range feature
    df['price_range'] = df['max_price'] - df['min_price']

    # Create the price standard deviation feature
    df['price_stddev'] = df[['tcgplayer_price', 'ebay_price', 'amazon_price', 'coolstuffinc_price']].std(axis=1)

    # Identify cards as tcg or ocg exclusive based on if ocg_date/tcg_date is na
    df['is_tcg_exclusive'] = df['ocg_date'].isna().astype(int)
    df['is_ocg_exclusive'] = df['tcg_date'].isna().astype(int)

    # Make tcg_date and ocg_date date variables
    df['tcg_date'] = pd.to_datetime(df['tcg_date'], errors='coerce')
    df['ocg_date'] = pd.to_datetime(df['ocg_date'], errors='coerce')

    # Create a "days since release" feature for TCG and OCG based on the tcg_date and ocg_date
    df['days_since_tcg_release'] = (pd.Timestamp.now() - df['tcg_date']).dt.days
    df['days_since_ocg_release'] = (pd.Timestamp.now() - df['ocg_date']).dt.days

    # Create a "first_market" variable to identify whether the card was in the TCG or OCG first
    df['first_market'] = np.where(
        (df['tcg_date'] < df['ocg_date']) | df['ocg_date'].isna(), 'TCG',
        np.where((df['ocg_date'] < df['tcg_date']) | df['tcg_date'].isna(), 'OCG', 'Unknown')
    )

    # Create a "market delay" feature, which is the time between the tcg and ocg releases
    df['market_delay'] = (df['ocg_date'] - df['tcg_date']).dt.days.abs()

    # Create a desc_length variable that is the number of words used in the desc
    df['desc_length'] = df['desc'].apply(lambda x: len(x.split()) if isinstance(x, str) else 0)

    return df

def update_types(df):
    """
    Updates the data types for specific columns in the DataFrame.
    """
    # Make categorical variables
    df['card_id'] = df['card_id'].astype('category')
    df['name'] = df['name'].astype('category')
    df['attribute'] = df['attribute'].astype('category')
    df['type'] = df['type'].astype('category')
    df['subtype'] = df['subtype'].astype('category')
    df['frame'] = df['frame'].astype('category')
    df['race'] = df['race'].astype('category')
    df['archetype'] = df['archetype'].astype('category')
    df['rarity_code'] = df['rarity_code'].astype('category')
    df['md_rarity'] = df['md_rarity'].astype('category')
    df['konami_id'] = df['konami_id'].astype('category')
    df['first_market'] = df['first_market'].astype('category')

    # Make ordinal variables
    df['level'] = pd.Categorical(df['level'], categories=list(range(0, 14)), ordered=True) # max 13
    df['linkval'] = pd.Categorical(df['linkval'], categories=list(range(1, 7)), ordered=True) # max 6
    df['scale'] = pd.Categorical(df['scale'], categories=list(range(0, 14)), ordered=True) # max 13
    df['has_effect'] = pd.Categorical(df['has_effect'], categories=[0, 1], ordered=True) # 0 or 1
    df['has_archetype'] = pd.Categorical(df['has_archetype'], categories=[0, 1], ordered=True) # 0 or 1
    df['is_tcg_exclusive'] = pd.Categorical(df['is_tcg_exclusive'], categories=[0, 1], ordered=True) # 0 or 1
    df['is_ocg_exclusive'] = pd.Categorical(df['is_ocg_exclusive'], categories=[0, 1], ordered=True) # 0 or 1

    ban_levels = ["Not Banned", "Semi-Limited", "Limited", "Forbidden"]
    df['banlist_tcg'] = pd.Categorical(df['banlist_tcg'], categories=ban_levels, ordered=True) # max 2
    df['banlist_ocg'] = pd.Categorical(df['banlist_ocg'], categories=ban_levels, ordered=True) # max 2
    df['banlist_goat'] = pd.Categorical(df['banlist_goat'], categories=ban_levels, ordered=True) # max 2

    df['rarity'] = df['rarity'].astype('category')
    rarity_order = [
        "Common",
        "Short Print",
        "Super Short Print",
        "Rare",
        "Super Rare",
        "Ultra Rare",
        "Secret Rare",
        "Normal Parallel Rare",
        "Duel Terminal Normal Parallel Rare",
        "Duel Terminal Rare Parallel Rare",
        "Duel Terminal Super Parallel Rare",
        "Duel Terminal Ultra Parallel Rare",
        "Duel Terminal Normal Rare Parallel Rare",
        "Super Parallel Rare",
        "Ultra Parallel Rare",
        "Shatterfoil Rare",
        "Mosaic Rare",
        "Starfoil",
        "Starfoil Rare",
        "Gold Rare",
        "Premium Gold Rare",
        "Gold Secret Rare",
        "Platinum Rare",
        "Platinum Secret Rare",
        "Extra Secret Rare",
        "Extra Secret",
        "Ultra Secret Rare",
        "Prismatic Secret Rare",
        "Collector's Rare",
        "Ultimate Rare",
        "Ghost/Gold Rare",
        "Ghost Rare",
        "Starlight Rare",
        "Quarter Century Secret Rare",
        "10000 Secret Rare",
        "Ultra Rare (Pharaoh's Rare)",
        "European debut",
        "European & Oceanian debut",
        "Oceanian debut",
        "New",
        "Reprint",
        "2",
        "3",
        "Cr"
    ]

    # Convert the column
    df['rarity'] = pd.Categorical(df['rarity'], categories=rarity_order, ordered=True)
    
    return df

def fix_NAs(df):
    """
    Fixes NA values in the DataFrame.
    """
    # Ensure fill values are in the categories for categorical columns
    for col, fill_value in {
        'archetype': "None",
        "attribute": "None",
        'banlist_tcg': 'Not Banned',
        'banlist_ocg': 'Not Banned',
        'banlist_goat': 'Not Banned',
        'md_rarity': 'Unknown',
        'konami_id': 'Unknown',
    }.items():
        if col in df.columns and isinstance(df[col].dtype, pd.CategoricalDtype):
            if fill_value not in df[col].cat.categories:
                df[col] = df[col].cat.add_categories([fill_value])

    # Now fill NAs
    df = df.fillna({
        'archetype': "None",
        "attribute": "None",
        'banlist_tcg': 'Not Banned',
        'banlist_ocg': 'Not Banned',
        'banlist_goat': 'Not Banned',
        'tcg_date': 'Unknown',
        'ocg_date': 'Unknown',
        'md_rarity': 'Unknown',
        'konami_id': 'Unknown',
    })

    return df

def standardize_card_names(df):
    """
    For each card_id, use the most recent non-null name across all time periods.
    """
    # Only consider non-null names, sort by most recent pull
    most_recent_names = (
        df[df['name'].notna()]
        .sort_values('time_pulled', ascending=False)
        .drop_duplicates('card_id')
        .loc[:, ['card_id', 'name']]
        .rename(columns={'name': 'corrected_name'})
    )
    # Merge back and update names
    df = df.merge(most_recent_names, on='card_id', how='left')
    df['name'] = df['corrected_name'].combine_first(df['name'])
    df = df.drop(columns=['corrected_name'])
    return df

if __name__ == "__main__":
    print("Fetching and processing data from YGOPRODECK API...")
    df = full_pull()
    df = feature_engineer(df)
    df = update_types(df)
    df = fix_NAs(df)
    df = standardize_card_names(df)
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Resolve directory path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(script_dir, "..", "Data", "Full Pulls"))
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, f"ygo_full_daily_{current_time}.csv")
    df.to_csv(output_path, index=False)
    print(f"Data successfully pulled and saved to: {output_path}")
