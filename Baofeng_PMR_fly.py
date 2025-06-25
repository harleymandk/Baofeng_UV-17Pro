import csv

filename = "radio_channels_complete.csv"

headers = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
    "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "Mode",
    "TStep", "Skip", "Comment", "URCALL", "RPT1CALL", "RPT2CALL"
]

# FRNET-kanaler (6 stk)
frnet_channels = [
    {"Name": "FRNET1", "Frequency": 149.025},
    {"Name": "FRNET2", "Frequency": 149.0375},
    {"Name": "FRNET3", "Frequency": 149.05},
    {"Name": "FRNET4", "Frequency": 149.0875},
    {"Name": "FRNET5", "Frequency": 149.1},
    {"Name": "FRNET6", "Frequency": 149.1125},
]

# PMR446: 32 kanaler, 6.25 kHz trin
pmr_start = 446.00625
pmr_step = 0.00625
pmr_channels = [
    {"Name": f"PMR446-{i+1}", "Frequency": pmr_start + i * pmr_step}
    for i in range(32)
]

# Flyfrekvenser: Kanal 900–999 = 100 stk, 8.33 kHz trin
fly_start = 118.000
fly_step = 0.00833
fly_channels = [
    {"Name": f"FLY-{i+1}", "Frequency": fly_start + i * fly_step, "Mode": "AM"}
    for i in range(100)
]

# Midterste kanaler (fra 446.2 MHz, 12.5 kHz trin) → Kanal 39 til 899 (861 stk)
# 899 - 38 = 861 kanaler
ext_start = 446.2
ext_step = 0.0125
ext_count = 899 - (len(frnet_channels) + len(pmr_channels))
ext_channels = [
    {"Name": f"EXT{i+1}", "Frequency": ext_start + i * ext_step}
    for i in range(ext_count)
]

# Saml og nummerér
all_channels = frnet_channels + pmr_channels + ext_channels + fly_channels

default_values = {
    "Duplex": "",
    "Offset": 0.0,
    "Tone": "",
    "rToneFreq": 88.5,
    "cToneFreq": 88.5,
    "DtcsCode": "023",
    "DtcsPolarity": "NN",
    "Mode": "NFM",  # Overskrives til "AM" for fly
    "TStep": 5.0,
    "Skip": "",
    "Comment": "",
    "URCALL": "",
    "RPT1CALL": "",
    "RPT2CALL": "",
}

with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()

    for idx, channel in enumerate(all_channels, start=1):
        row = default_values.copy()
        row.update(channel)
        row["Location"] = idx
        row["Frequency"] = f"{row['Frequency']:.6f}"
        row["Offset"] = f"{row['Offset']:.6f}"
        row["rToneFreq"] = f"{row['rToneFreq']:.1f}"
        row["cToneFreq"] = f"{row['cToneFreq']:.1f}"
        row["TStep"] = f"{row['TStep']:.2f}"
        writer.writerow(row)

print(f"CSV-fil med {len(all_channels)} kanaler gemt som: {filename}")
