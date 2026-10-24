import json
import pytest
from book_system.models import InvalidBookDataError
from book_system.exporters import export_to_json, import_from_csv

def test_export_to_json_tmp_path(tmp_path, sample_book_1):
    output_path = tmp_path / "catalog.json"
    export_to_json([sample_book_1], output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["title"] == "Kobzar"

def test_import_from_csv_malformed_record(tmp_path):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text(
        "id,title,author,year,pages\n"
        "1,Valid Title,Author,2020,100\n"
        "invalid_id,Title,Author,2020,100\n",
        encoding="utf-8"
    )

    with pytest.raises(InvalidBookDataError, match="Malformed CSV record"):
        import_from_csv(csv_file)