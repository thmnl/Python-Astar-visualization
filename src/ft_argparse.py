import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mazefile", nargs="*")
    parser.add_argument(
        "-dd", "--disable-diagonal", action="store_true", help="Only allow up, down, left and right movements",
    )
    parser.add_argument(
        "--random-maze", action="store_true", help="Randomize a maze of a random size",
    )
    parser.add_argument(
        "--maze-size", nargs="+", type=int, help="Change the maze size by value x y, default 30 30"
    )
    parser.add_argument(
        "--save-maze", action="store_true", help="Save the maze in a json",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file",
    )
    return parser.parse_args()
