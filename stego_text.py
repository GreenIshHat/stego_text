# stego_text.py
# Zero-Width Unicode Stego Encoder/Decoder
# ==========================================

# USAGE EXAMPLES:
#   python3 stego_text.py --infile input.txt --outfile secret.txt --payload "CUSTOM_PAYLOAD"
#   python3 stego_text.py --infile secret.txt --decode
#   python3 stego_text.py --infile base.txt --multi

# ========== CONFIGURABLE CONSTANTS ==========
SIGNAL_PHRASE = "I am the signal."        # Phrase where payload is injected
ZW_CHAR_0 = '\u200B'                      # Zero Width Space (represents bit 0)
ZW_CHAR_1 = '\u200C'                      # Zero Width Non-Joiner (represents bit 1)
ENCODING = "utf-8-sig"                    # UTF-8 with BOM
DEFAULT_OUTPUT_FILE = "output_stego.txt"  # Default output file name
DEFAULT_PAYLOAD_STRING = "SIGNAL_PAYLOAD" # Default payload string
# ============================================

ZW_MAP = {
    '0': ZW_CHAR_0,
    '1': ZW_CHAR_1
}

# === STRING → BINARY ===
def string_to_binary(msg: str) -> str:
    return ''.join(f"{ord(c):08b}" for c in msg)

# === BINARY → STRING ===
def binary_to_string(bits: str) -> str:
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

# === BINARY → ZERO-WIDTH STRING ===
def binary_to_zw(bits: str) -> str:
    return ''.join(ZW_MAP[bit] for bit in bits)

# === ZERO-WIDTH → BINARY ===
def zw_to_binary(zw_string: str) -> str:
    return ''.join(
        '0' if c == ZW_CHAR_0 else
        '1' if c == ZW_CHAR_1 else
        '' for c in zw_string
    )

# === INJECT PAYLOAD AFTER SIGNAL PHRASE ===
def inject_payload(text: str, payload_string: str) -> str:
    if SIGNAL_PHRASE not in text:
        raise ValueError(f"[ERROR] Signal phrase '{SIGNAL_PHRASE}' not found in text.")
    binary = string_to_binary(payload_string)
    zw_payload = binary_to_zw(binary)
    return text.replace(SIGNAL_PHRASE, SIGNAL_PHRASE + zw_payload)

# === EXTRACT PAYLOAD AFTER SIGNAL PHRASE ===
def extract_payload(text: str) -> str:
    if SIGNAL_PHRASE not in text:
        return "[ERROR] Signal phrase not found."
    start = text.find(SIGNAL_PHRASE) + len(SIGNAL_PHRASE)
    zw_chunk = text[start:]
    binary = zw_to_binary(zw_chunk)
    return binary_to_string(binary) if binary else "[ERROR] No ZW payload found."

# === MAIN INTERFACE ===
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Zero-width Unicode Stego Encoder/Decoder")
    parser.add_argument("--infile", required=True, help="Input base text file")
    parser.add_argument("--outfile", default=DEFAULT_OUTPUT_FILE, help="Output file name")
    parser.add_argument("--payload", help="Custom string payload to embed")
    parser.add_argument("--multi", action="store_true", help="Enable multi-payload concat mode")
    parser.add_argument("--decode", action="store_true", help="Decode all payloads from file")

    args = parser.parse_args()

    with open(args.infile, encoding=ENCODING) as f:
        base_text = f.read()

# === MULTI-PAYLOAD MODE ===
if args.multi:
    PAYLOADS = [
        "I'M_A_FREELANCER_ASPIRING_CTO_LOOKING_FOR_COLLABORATORS_AND_FUNDING",
        "EXPERIENCE_IN_SYSTEMS_ARCHITECTURE_AND_CONSCIOUS_TECH",
        "BUILDING_oCOMP_AND_CARD_GAME_WITH_WEB3_POTENTIAL",
        "SOMBRERO.VERDE_AT_THE_MAIL_OF_PROTON",
        "OPEN_TO_CONTRACTS__ALIGNMENT_OVER_HYPE__LET'S_CONNECT"
    ]


        combined = ""
        for payload in PAYLOADS:
            section = inject_payload(SIGNAL_PHRASE, payload)
            combined += section + "\n"

        final_output = base_text + "\n\n" + combined.strip()
        with open(args.outfile, 'w', encoding=ENCODING) as f:
            f.write(final_output)

        print(f"[✔] Multi-payload embedded → {args.outfile}")
        return

    # === SINGLE PAYLOAD MODE ===
    if args.payload:
        encoded = inject_payload(base_text, args.payload)
        with open(args.outfile, 'w', encoding=ENCODING) as f:
            f.write(encoded)
        print(f"[✔] Payload injected → {args.outfile}")
        return

    # === DECODE MODE ===
    if args.decode:
        print("🔍 Extracted payloads:")
        lines = [line for line in base_text.splitlines() if SIGNAL_PHRASE in line]
        for i, line in enumerate(lines, 1):
            decoded = extract_payload(line)
            print(f"Payload {i}: {decoded}")
        return

    print("[ERROR] No operation specified. Use --payload, --multi, or --decode.")

if __name__ == "__main__":
    main()
