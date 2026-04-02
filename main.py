import argparse
import json
from pathlib import Path

from transaction_builder import TransactionPayloadBuilder

from pos_extract import is_shift_batch, PosKeys
from shift_summary_builder import ShiftSummaryPayloadBuilder

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def default_output_path(input_path: Path, *, shift: bool) -> Path:
    if shift:
        return input_path.with_name("_payload_shift_batch.json")
    return input_path.with_name("_payload_transaction.json")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Build CSU payload from qilong extract: "
            "_payload_transaction.json (single txn) or "
            "_payload_shift_batch.json (shift batch)."
        )
    )
    parser.add_argument("-i", "--input", required=True, help="Path to JSON extract")
    parser.add_argument("-o", "--output", default=None, help="Output path")
    args = parser.parse_args()

    input_path = Path(args.input)
    
    pos_data = load_json(input_path)

    shift = is_shift_batch(pos_data) and len(pos_data.get(PosKeys.TRANSACTIONS) or []) > 0
    output_path = (
        Path(args.output) if args.output else default_output_path(input_path, shift=shift)
    )

    if shift:
        builder = ShiftSummaryPayloadBuilder()
        payload = builder.build_dict(pos_data)
        if payload is None:
            print(f"No batch payload. skip_reason={builder.skip_reason}")
            return
    else:
        builder = TransactionPayloadBuilder()
        payload = builder.build_dict(pos_data)
        if payload is None:
            print(f"No payload built. skip_reason={builder.skip_reason}")
            return

    write_json(output_path, payload)
    print(f"Payload written to {output_path}")


if __name__ == "__main__":
    main()