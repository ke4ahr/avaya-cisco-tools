#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# autobuilderclaude v1.1.1
# Copyright (C) 2026 Kris Kirby
# https://github.com/ke4ahr/autobuilderclaude
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
"""
AT&T / Lucent / Avaya Definity port code generator

Usage:
  definity_labels_to_text.py
      Interactive mode – prompts for Cabinet (0‑99), Shelf (A‑E),
      Card start (0‑25) and Card end (0‑25).
      Empty answers use the following defaults:
          Card? -> 1
          To Card? => 21
      Prints one label per line in the format <cabinet><shelf>C<card>
      (e.g. 06AC01) to stdout.

  definity_labels_to_text.py --prefix "<text>"
      Same as above, but each output line is prefixed with the given
      text.  The text may be supplied in single or double quotes, e.g.
      --prefix "'" or --prefix="LABEL_".  If the quotes are omitted they
      are still accepted as part of the prefix.


  definity_labels_to_text.py --suffix "<text>"
      Same as above, but each output line is suffixed with the given
      text.  The text may be supplied in single or double quotes, e.g.
      --suffix "'" or --suffix="_END".  If the quotes are omitted they
      are still accepted as part of the suffix.

  definity_labels_to_text.py -p, --pair
      When this option is present the script will also prompt for
      "Pair? (0-25)" and "To Pair? (0-25)".  Empty answers use the
      following defaults: 
          Pair? -> 1
          To Pair? -> 25
      For every card in the card range and every pair in the pair range a
      label is printed: <cabinet><shelf><card><pair> (e.g. 06A0105).

  definity_labels_to_text.py -h
  definity_labels_to_text.py --help
      Show this usage information and exit.
"""

import sys


def get_int(prompt, low, high, default=None):
    """Prompt for an integer within [low, high] and return it.
    If the user just presses Enter and a *default* is supplied,
    that default is returned (after checking it lies in the range)."""
    while True:
        try:
            raw = input(prompt).strip()
            if raw == "" and default is not None:
                value = default
            else:
                value = int(raw)
        except Exception:
            # Invalid input – ask again
            print(f"  Please enter a number between {low} and {high}.")
            continue

        if low <= value <= high:
            return value
        print(f"  Please enter a number between {low} and {high}.")

def get_shelf():
    """Prompt for a shelf label (A‑E) and return the uppercase letter."""
    while True:
        shelf = input("  Shelf?  (A-E): ").strip().upper()
        if shelf in {"A", "B", "C", "D", "E"}:
            return shelf
        print("  Please enter a single letter from A to E.")

def print_usage():
    """Print the usage block from the module docstring."""
    print(__doc__.strip())


def main():
    if any(arg in ("-h", "--help") for arg in sys.argv[1:]):
        print_usage()
        return


    # Parse optional --prefix argument
    prefix = ""
    suffix = ""
    use_pair = False

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == "--prefix":
            if i + 1 < len(sys.argv):
                prefix = sys.argv[i + 1]
                i += 2
            else:
                print("Error: --prefix requires a value.")
                sys.exit(1)
        elif arg.startswith("--prefix="):
            prefix = arg.split("=", 1)[1]
            i += 1

        elif arg == "--suffix":
            if i + 1 < len(sys.argv):
                suffix = sys.argv[i + 1]
                i += 2
            else:
                print("Error: --suffix requires a value.")
                sys.exit(1)
        elif arg.startswith("--suffix="):
            suffix = arg.split("=", 1)[1]
            i += 1

        elif arg in ("-p", "--pair"):
            use_pair = True
            i += 1

        else:
            print(f"Error: unknown argument '{arg}'.")
            sys.exit(1)


    # Strip surrounding single or double quotes from prefix/suffix, if present
    def strip_quotes(s):
        if len(s) >= 2 and ((s[0] == s[-1] == "'") or (s[0] == s[-1] == '"')):
            return s[1:-1]
        return s

    prefix = strip_quotes(prefix)
    suffix = strip_quotes(suffix)


    # ------------------------------------------------------------------
    # Interactive prompts (with defaults for empty answers)
    # ------------------------------------------------------------------

    cabinet = get_int("Cabinet? (1-99): ", 1, 99)
    shelf = get_shelf()
    start_card = get_int("   Card? (1-25): ", 1, 25, default=1)
    end_card   = get_int("To card? (1-25): ", 1, 25, default=21)

    # Ensure we iterate from the smaller to the larger value
    card_lo, card_hi = (start_card, end_card) if start_card <= end_card else (end_card, start_card)

    if use_pair:
        start_pair = get_int("Pair? (1-25): ", 1, 25, default=1)
        end_pair   = get_int("To Pair? (1-25): ", 1, 25, default=25)
        pair_lo, pair_hi = (start_pair, end_pair) if start_pair <= end_pair else (end_pair, start_pair)

        for card in range(card_lo, card_hi + 1):
            for pair in range(pair_lo, pair_hi + 1):
                line = f"{prefix}{cabinet:02d}{shelf}{card:02d}{pair:02d}{suffix}"
                print(line)
    else:
        for card in range(card_lo, card_hi + 1):
            line = f"{prefix}{cabinet:02d}{shelf}{card:02d}{suffix}"
            print(line)

if __name__ == "__main__":
    main()

