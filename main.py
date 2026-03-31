import argparse
import json
from pathlib import Path

from transaction_builder import TransactionPayloadBuilder


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name("_payload_header.json")


def main():
    parser = argparse.ArgumentParser(
        description="Build payload from qilong _pos_data.json"
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to _pos_data.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output payload path (default: same folder/_payload_header.json)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else default_output_path(input_path)

    pos_data = load_json(input_path)

    builder = TransactionPayloadBuilder()
    payload = builder.build_dict(pos_data)

    if payload is None:
        print(f"No payload built. skip_reason={builder.skip_reason}")
        return

    write_json(output_path, payload)
    print(f"Payload written to {output_path}")


if __name__ == "__main__":
    main()