def achievements_mapping(gamedata, profile):
    mapping = {item['id']: f"[{category['displayName']}] {item['name']} - {item['description']}" for category in gamedata['achievements'] for item in category['achievements']}
    return [mapping[i] for i in profile['completedAchievements']]


def detailed_mapping(gamedata, profile):
    heroes_map = {k: v['displayName'] for k, v in gamedata['heroesMap'].items()}
    # [TODO] Formatting
    stats_map = {k: v['name'] for k, v in gamedata['stats'].items()}
    return {
        i: {
            heroes_map[k_outer]: {
                stats_map[k_inner]: v_inner for k_inner, v_inner in v_outer.items()
            }
            for k_outer, v_outer in profile['careerStats'][i]['stats'].items()
        }
        for i in ['ranked', 'unranked']
    }


def hero_comparison_mapping(gamedata, profile):
    comparison_name_mapping = {i['id']: i['name'] for i in gamedata['heroComparison']}
    heroes_map = {k: v['displayName'] for k, v in gamedata['heroesMap'].items()}
    return {
        i: {
            comparison_name_mapping[k]: {
                heroes_map[item['hero']]: item['value'] for item in v
            }
            for k, v in profile['heroComparison'][i].items()
        }
        for i in ['ranked', 'unranked']
    }
