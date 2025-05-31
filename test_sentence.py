from modules.team_module import build_team

# Test cases
description1 = "i want 2 supporter and 4 attacker"
team1 = build_team(description1)
print("Test 1 Team:")
for pokemon in team1:
    print(f"- {pokemon['name'].title()}: {pokemon['types']} (Role: {pokemon['role']})")

# Role distribution check karo
role_count = {}
for pokemon in team1:
    role = pokemon['role']
    role_count[role] = role_count.get(role, 0) + 1

print(f"\nRole Distribution: {role_count}")
print(f"Total team size: {len(team1)}")
    


