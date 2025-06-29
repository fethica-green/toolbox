# config.py

# ---------------------------------------------------
# Identifiants et rôles des utilisateurs
# ---------------------------------------------------
# Structure :
#   "USERNAME": {
#       "pwd": "MOT_DE_PASSE",
#       "role": "NOM_DU_ROLE"
#   }
CREDENTIALS = {
    "SLA": {"pwd": "SLA123",  "role": "Logistics"},
    "CFA": {"pwd": "CFA123",  "role": "AdminHR"},
    "SNA": {"pwd": "SNA123",  "role": "Manager"},
    "YKS": {"pwd": "YKS1213", "role": "Staff"},
    "MTR": {"pwd": "MTR38",   "role": "ProjectAdmin"}
}

# ---------------------------------------------------
# Droits d'accès : pour chaque rôle, liste des clés de modules
# ---------------------------------------------------
# Clés de modules :
#   "dashboard", "ta", "dsa", "expenses", "records",
#   "po", "meeting", "hdlog", "news"
ACCESS = {
    "Logistics":    ["dashboard", "ta", "dsa", "expenses", "records", "po", "meeting", "hdlog", "news"],
    "AdminHR":      ["dashboard", "ta", "dsa", "expenses", "records", "po", "meeting", "hdlog", "news"],
    "Manager":      ["dashboard", "ta", "dsa", "expenses", "records", "po", "meeting", "hdlog", "news"],
    "Staff":        ["ta", "dsa", "expenses"],
    "ProjectAdmin": ["dashboard", "ta", "dsa", "expenses", "records", "po", "meeting", "hdlog", "news"]
}
